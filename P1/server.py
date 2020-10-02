from socket import *

sock = socket(AF_INET, SOCK_DGRAM)
source_ip = "localhost"
source_port = 5402

sock.bind((source_ip, source_port))

while True:
    data, sender_info = sock.recvfrom(2048)
    print("Message: ", data, "from: ", sender_info)
    sock.sendto(data.upper(), sender_info)
