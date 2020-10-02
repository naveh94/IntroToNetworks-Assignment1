from socket import *

sock = socket(AF_INET, SOCK_DGRAM)
dest_ip = "localhost"
dest_port = 5402

msg = input("Message to send:")

while not msg == "quit":
    sock.send(msg, (dest_ip, dest_port))
    data, sender_info = sock.recvfrom(2048)
    print("Server sent: ", data)
    msg = input("Message to send:")

sock.close()
