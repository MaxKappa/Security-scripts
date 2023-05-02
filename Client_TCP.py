import socket

target_host = "127.0.0.1"
target_port = 9999

# crea un oggetto socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connettiti al client
client.connect((target_host, target_port))

# invia dei dati
while True:
    data = input("Invia: ")
    client.send(data.encode())
# riceve dei dati
    response = client.recv(4096)
    print(response.decode())
