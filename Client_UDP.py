import socket

target_host = "8.8.8.8"
target_port = 80

# crea un oggetto socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# invio dei dati
data = "AAABBBCCC"
client.sendto(data.encode(), (target_host, target_port))

# ricevo dei dati
data, addr = client.recvfrom(4096)

print(data.decode())
