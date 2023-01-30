import socket
import sys
from termcolor import colored

def client_handler(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    count = 0
    try:
        sock.connect((ip, port))
        print(colored("[*] Port %d is open" % port, 'green'))
    except:
        count += 1
    return count

def iterator(n, ip):
    print(colored("[*] Processing port scan on %s" % ip, 'green'))
    count = 0
    for i in range(1,n):
        count += client_handler(ip, i)
    return count

def usage():
    print("Usage: python3 portscanner.py [target] [range]")

def main():
    if len(sys.argv[1:]) != 2:
        usage()
        sys.exit(0)
    ip = sys.argv[1]
    r = int(sys.argv[2])
    count = iterator(r, ip)
    print(colored("[*] Processed %d ports close." % count, 'red'))

main()