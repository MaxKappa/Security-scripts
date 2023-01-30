import socket
import threading

bind_ip = "127.0.0.1"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print("[*] Listening on %s:%d" % (bind_ip, bind_port))

# thread di gestione del client
def handle_client(client_socket):
    # stampa ciò che spedisce il client
    requests = client_socket.recv(1024)
    print("[*] Recived %s" % (requests.decode()))
    # manda un pacchetto indietro
    data = "ACK!"
    client_socket.send(data.encode())
    client_socket.close()


while True:
    client,addr = server.accept()
    print("[*] Accepted connection from %s:%d" % (addr[0], addr[1]))
    # avvia il thread che gestisce i dati in arrivo dal client
    client_handler = threading.Thread(
        target = handle_client,
        args = (client,))
    client_handler.start()


