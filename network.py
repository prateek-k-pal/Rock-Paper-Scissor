import socket
import pickle
import game

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "didactic-orbit-59qjpx9jp7vcpx6r-43735.app.github.dev"
        self.port  = 43735
        self.addr = (self.server, self.port)
        self.p = self.connect()
        
    def getP(self):
        return self.p
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
            pass
        
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
