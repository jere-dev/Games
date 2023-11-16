import socket
import threading
import time

class Server(object):
    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', self.port))
        #socket.gethostbyname(socket.gethostname())
        self.clients = []

    def __del__(self):
        self.sock.close()

    def sendMessage(self, message, sender):
        for client in self.clients:
            if client != sender:
                client[0].send(message.encode('utf-8'))

    def listen(self):
        self.sock.listen(2)
        while True:
            self.clients.append(self.sock.accept())
            #self.client.settimeout(60)
            threading.Thread(target = self.listenToClient, args=(self.clients[-1],), daemon=True ).start()
            

    def listenToClient(self, client):
        while True:
            try:
                data = client[0].recv(1024)
                if data:
                    msg = data.decode('utf-8')
                    self.sendMessage(msg, client)
                    print(msg)
                else:
                    print('Client disconnected')
                    break
            except:
                client[0].close()
                return False
            
    def startThread(self):
        dameaon = threading.Thread(target = self.listen, daemon=True )
        dameaon.start()

server = Server(9999)
# server.startThread()

while True:
    server.listen()
