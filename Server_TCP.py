import socket
import threading

bind_ip = "127.0.0.1"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)
print("[*] Listening on %s:%d" % (bind_ip, bind_port))

def handle_client(client_socket):
    # stampa ciò che spedisce il client
    requests = client_socket.recv(1024)
    print("[*] Recived %s" % (requests.decode()))
    # manda un pacchetto indietro
    data = "ACK!"
    client_socket.send(data.encode())



try:
    while True:
        client,addr = server.accept()
        print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
        # avvia un thread per gestire il client
        client_handler = threading.Thread(
            target = handle_client,
            args = (client,))
        client_handler.start()
except KeyboardInterrupt:
    print("Server interrotto")
    server.close()
    sys.exit(0)



