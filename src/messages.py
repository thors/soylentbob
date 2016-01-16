import socket

class OutMessage:
    def __init__(self, msg, countdown):
        self.message = msg
        self.countdown = countdown

class OutMessages:
    def __init__(self, sock):
        self.messages = []
        self.sock = sock
    def add(self, msg, countdown):
        
        self.messages.append(OutMessage(msg,countdown))        
    def tick(self):
        i = 0
        while i < len(self.messages):
            if self.messages[i].countdown > 0:
                self.messages[i].countdown = self.messages[i].countdown - 1
                i = i + 1
            else:
                self.sock.send(self.messages[i].message)
                del self.messages[i] 
            

