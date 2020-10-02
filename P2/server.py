import threading
from socket import *

SOURCE_IP = "localhost"
SOURCE_PORT = 5402


class ChatUser:
    """
    A class defining a chat user, containing methods for changing the username,
     receiving messages, and sending all pending messages.
    """
    def __init__(self, info, name):
        self.client_info = info
        self.name = name
        self.pending_messages = []

    def get_name(self):
        return self.name

    def change_name(self, name):
        self.name = name

    def pend_message(self, message):
        self.pending_messages.append(message)

    def send_pending_messages(self, sock):
        for msg in self.pending_messages:
            sock.sendto(msg.encode(), self.client_info)
        sock.sendto("e".encode(), self.client_info)
        self.pending_messages.clear()


class Chat (threading.Thread):
    """
    a class defining a Chat using an UDP server.
    contain a list of clients, when broadcasting messages recieved, will send message to all clients.
    """
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.is_running = False
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.users = {}
        self.operations = {
            '1': self.join_chat,
            '2': self.send_message,
            '3': self.name_change,
            '4': self.leave_chat,
            '5': self.send_pending
        }

    def run(self):
        self.is_running = True
        while self.is_running:
            self.recv_msg()

    def recv_msg(self):
        msg, sender_info = self.sock.recvfrom(2048)
        msg = str(msg, "utf-8")
        op = msg[0]
        msg = msg[2:]
        func = self.operations.get(op)
        if func:
            func(sender_info, msg)
        else:
            msg = "Illegal request"
            self.sock.sendto(msg.encode(), sender_info)

    def broadcast_msg(self, msg):
        print(msg)
        for client in self.users:
            self.users[client].pend_message(msg)

    def join_chat(self, info, name):
        msg = name + " has joined"
        self.users[info] = ChatUser(info, name)
        self.broadcast_msg(msg)

    def send_message(self, info, msg):
        if self.users.get(info) is not None:
            msg = self.users[info].get_name() + ": " + msg
            self.broadcast_msg(msg)
            self.users.get(info).send_pending_messages(self.sock)

    def name_change(self, info, name):
        if self.users.get(info) is not None:
            msg = self.users[info].get_name() + " changed his name to " + name
            self.users[info].change_name(name)
            self.broadcast_msg(msg)
            self.users[info].send_pending_messages(self.sock)

    def leave_chat(self, info, msg):
        if self.users.get(info) is not None:
            msg = self.users[info].get_name() + " has left the group."
            self.users.pop(info)
            self.broadcast_msg(msg)

    def send_pending(self, info, msg):
        if self.users.get(info) is not None:
            self.users.get(info).send_pending_messages(self.sock)

    def stop(self):
        self.is_running = False
        self.sock.close()


chat = Chat(SOURCE_IP, SOURCE_PORT)
chat.start()
q = input("Type 'q' to stop the server:")
while not q == 'q':
    q = input("Type 'q' to stop the server:")
chat.stop()
