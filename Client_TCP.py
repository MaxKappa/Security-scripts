import socket

target_host = "www.google.com"
target_port = 80

# crea un oggetto socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connettiti al client
client.connect((target_host, target_port))

# invia dei dati
data = "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
client.send(data.encode())

# riceve dei dati
response = client.recv(4096)

print(response.decode())
