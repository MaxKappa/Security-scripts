import sys
import paramiko

def ssh_command(ip, user, password, port):
    print("[*] Connected on %s:%d as %s" % (ip, port, user))
    while True:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=user, password=password, port=port)
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            command = input("$ ")
            if command == "exit()":
                print("[*] Connection close")
                ssh_session.close()
                sys.exit(0)
            ssh_session.exec_command(command)
            print(ssh_session.recv(1024).decode('utf-8'))

def usage():
    print("Usage python3 bg_sshcmd.py [target] [port] [username] [password]")
    print("Example: python3 bg_sshcmd.py 192.168.1.111 22 admin root")

def main():
    if len(sys.argv[1:]) != 4:
        usage()
        sys.exit(0)
    ip = sys.argv[1]
    port = int(sys.argv[2])
    user = sys.argv[3]
    password = sys.argv[4]
    ssh_command(ip, user, password, port)

main()