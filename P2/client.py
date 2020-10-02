from socket import *
import threading

DEST_IP = "localhost"
DEST_PORT = 5402


sock = socket(AF_INET, SOCK_DGRAM)
while True:
    msg = input("Message to send:")
    sock.sendto(msg.encode(), (DEST_IP, DEST_PORT))
    if msg[0] == '4':
        break
    if msg[0] == '2' or msg[0] == '3' or msg[0] == '5':
        while True:
            msg, info = sock.recvfrom(2048)
            msg = str(msg, "utf-8")
            if msg == "e":
                break
            else:
                print(msg)
