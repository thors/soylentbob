import argparse, socket, re, random, os, time
from users import *
from messages import *
from picker import *
            
        

class sockpuppet:
    def __init__(self):
        random.seed()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.out_queue = OutMessages(self.sock)
        self.users = Users()
        self.args = self.get_args()
        self.connect(self.args.server)
        self.register()
        self.active_channels=[]
        self.greet_users=self.load_file("data/greet_users.txt")
        self.annoy_users=self.load_file("data/annoy_users.txt")
        self.handler = {}
        #self.handler[re.compile("^PRIVMSG " + self.args.nick + " :annoy (..*)")] = self.annoy
        #self.handler[re.compile("^PRIVMSG " + self.args.nick + " :greet (..*)")] = self.greet
        self.handler[re.compile("^PRIVMSG .*")] = self.activity
        self.handler[re.compile("^PRIVMSG " + self.args.nick + " :reflect (..*)")] = self.reflect
        self.handler[re.compile("^PING (.*)")] = self.ping
        self.handler[re.compile("^PRIVMSG " + self.args.nick + " :join (..*)")] = self.join
        self.handler[re.compile("^PRIVMSG ([#!&]..*) :([^ ]*)\+\+.*")] = self.see_karma
        self.main_loop()
    
    def get_args(self):
        parser = argparse.ArgumentParser(description='Helper to build a socket army in IRC chats')
        #parser.add_argument('--server', default='chat.soylentnews.org:6667', help='domain-name/port of IRC server')
        #parser.add_argument('--server', default='localhost:6667', help='domain-name/port of IRC server')
        parser.add_argument('--server', default='nsa:6667', help='domain-name/port of IRC server')
        parser.add_argument('--host', default='0', help='desired hostname')
        parser.add_argument('--client_server', default='*', help='desired client server name')
        parser.add_argument('--user', default='soylentbob', help='desired username in channel')
        parser.add_argument('--nick', default='SoylentBob', help='desired username in channel')
        parser.add_argument('--password', default='', help='password (if required for this server)')
        parser.add_argument('--realname', default='Puppet Master', help='"Real Name" of the script')
        args = parser.parse_args()
        return args

    def load_file(self,filename):
        lines=[]
        if os.path.exists(filename):
            f = open(filename,"r")
            lines = f.readlines()
            for i in range(0,len(lines)-1):
                lines[i]=lines[i].strip()
        return lines
        
    def activity(self, message, m):
        self.users.activity(message.nick)
    
    def ping(self, message, m):
        self.send("PONG " + m.group(1))

    def see_karma(self, message, m):
        i = random.randint(0,100)
        print m.group(2)+ " " + str(i)
        (te,ti) = pick_random_delayed("data/" + m.group(2) + ".txt", message)
        if len(te) > 0:
            self.enqueue("PRIVMSG " + m.group(1) + " :" + te, ti)

    def reflect(self, message, m):
        self.send(m.group(1))

    def join(self, msg, m):
        self.send("JOIN " + m.group(1))

    def connect(self,server):
        host = server[:server.find(":")]
        port = int(server[server.find(":")+1:])
        print host + " " + str(port)
        self.sock.connect((host, port))

    def register(self):
        if len(self.args.password) > 0:
            self.sock.send("PASS " + self.args.password + "\n")
        self.sock.send("NICK " + self.args.nick + "\n")
        self.sock.send("USER " + self.args.nick + " " + self.args.host + " " + self.args.client_server + " :" + self.args.realname + "\n")

    def enqueue(self, msg, countdown):
        if msg[-1:] != "\n":
            msg = msg + "\n"
        self.out_queue.add(msg,countdown)

    def send(self,msg):
        print msg
        if msg[-1:] != "\n":
            msg = msg + "\n"
        self.sock.send(msg)

    def handle(self, msg):
        message = Message(msg)
        for k in self.handler.keys():
            m = k.match(message.message)
            if None != m:
                self.handler[k](message, m)
        
    def main_loop(self):
        msg = ""
        msg_new = ""
        self.sock.setblocking(0)
        while True:
            try:
                msg_new = self.sock.recv(100)
            except:
                time.sleep(1)
                self.out_queue.tick()
                continue
            
            if len(msg_new) == 0:
                continue
            
            msg = msg + msg_new
            npos = msg.find("\n")
            while  npos > 0:
                self.handle(msg[:npos])
                msg = msg[npos+1:]
                npos = msg.find("\n")


sock = sockpuppet()
