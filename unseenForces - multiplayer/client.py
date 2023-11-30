import threading
import socket
import time

class Client(object):
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.message = "start:connected"
        self.networkCommands = {"start":lambda mes:print(mes)}

    def addNetworkCommand(self, name, func):
        self.networkCommands[name] = func

    def processMessage(self):
        p = self.message.split(":")
        self.networkCommands[p[0]](p[1])

    def __del__(self):
        self.client.close()

    def sendMessage(self, message):
        if self.client:
            self.client.send(message.encode('utf-8'))

    def getMessage(self, defult):
        if self.message == "":
            return defult
        return self.message

    def listenToServer(self):
        while True:
            try:
                data = self.client.recv(1024)
                if data:
                    # Set the response to echo back the recieved data 
                    self.message = data.decode()
                    print(data.decode('utf-8'))
                else:
                    print('Server disconnected')
                    #self.message = None
                    break
            except:
                self.client.close()
                return False
            
    def startThread(self):
        dameaon = threading.Thread(target = self.listenToServer, daemon=True)
        dameaon.start()

# c = Client('127.0.0.1', 9999)
# c.startThread()

# while True:
#     c.sendMessage("hi from client")
#     time.sleep(5)