import socket
import socks
import sys
import os
import encryptionlib
from thread import start_new_thread

class Client():
    def __init__(self,username,addr,port):
        self.rsa = encryptionlib.RSA()
        self.pubk, self.prvk = self.rsa.generate_keypair()
        self.username = username
        os.system("tor")
        self.members = []
        socks.set_default_proxy("socks5","127.0.0.1",9050)
        self.sock = socks.socksocket()
        self.sock.connect((addr,port))
        self.sock.send(self.username)
        self.sock.send(self.pubk)
        self.GetUsers()
        start_new_thread(self.listen,())
        start_new_thread(self.send,())

    def GetUsers(self):
        data = self.sock.recv(1024)
        data = repr(data)
        for users in data.split(' '):
            self.members.append((users.split(':')[0],users.split(':')[1]))

    def listen(self):
        while 1:
            data = self.sock.recv(1024)
            data = repr(data)
            if data == "pubkey?":
                self.sock.send(self.pubk)
                continue

            print self.rsa.decrypt(self.prvk,data)

    def send(self):
        while 1:
            message = raw_input("enter message/> ")
            for usr in self.members:
                self.sock.send(usr[0] + ": " + self.rsa.encrypt(usr[1],message))

class utils:
    def GetUser(username,users):
        for usr in users:
            if usr.username == username:
                return usr        

class user:
    def __init__(self,username,addr,conn):
        self.username = username
        self.addr = addr
        self.conn = conn   

class Server:
    def __init__(self,port):
        self.clients = []
        self.port = port

    def broadcast(self,usr,data):            
        for users in self.clients:            
            users.conn.send(usr.username + ":" + data)

    def send(self,usr,data):
        usr.conn.send(data)

    def handler(self,usr):
        while 1:
            data = usr.conn.recv(1024)
            data = repr(data)
            self.send(utils.GetUser(data.split(' ')[0]),data.split(' ')[1])

    def sendlst(self):
        data = ""
        for usr in self.clients:
            usr.conn.send("pubkey?")
            data += usr.username + ":" + usr.conn.recv(1024)
        return data

    def Run(self):
        sock = socket.socket()
        sock.bind(('0.0.0.0',self.port))
        sock.listen(5)
        while 1:
            conn , addr = sock.accept()
            username = conn.recv(1024)
            pubk = conn.recv(1024)                        
            usr = user(username,addr[0],conn)
            self.broadcast(usr,pubk)
            conn.send(self.sendlst())
            self.clients.append(usr)
            start_new_thread(self.handler,(usr,None))



def startup(opts):
    if opts[1] == '-s':
        Server(int(opts[2])).Run()
    else:
        usrname = raw_input('enter username: ')
        Client(usrname,opts[2],int(opts[3]))


print "welcome to Tor Chan Chat (:"
print "use -s port to start a server"
print "or -c with addr and port to start as a client"
print "good luck and have fun (: "
startup(sys.argv)