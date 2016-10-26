from utils import SECRET # Flag format ECTF{[a-z]{27}}
import utils
import threading
import socket
import sys
import os
import json
import yaml

host = "0.0.0.0"
port = 9999

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))
threads = []
class ClientThread(threading.Thread):

    def __init__(self,ip,port,socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.msg = {}
        self.msg["uniqueId"] = ip
        self.msg["SECRET"] = SECRET
        print "[+] New thread started for "+ip+":"+str(port)

    def run(self):
        try:
            print "Connection from : "+self.ip+":"+str(self.port)
            welcome = """
Welcome to e3 storage interface. This is a beta version so bare with us :)
Storage costs are as cheap as Rs.1 per byte ;).
Note:
* The bytes used are calculated after zlib compression.
* The storage used by the metadata is also charged
"""
            menu = """
Choose option
1) Upload (Max of 1024 bytes)
2) Download
3) Exit
"""
            self.socket.send(welcome)
            while True:
                self.socket.send(menu)
                option = self.socket.recv(5).strip()
                if option == "1":
                    self.socket.send("Input data..\n")
                    data = self.socket.recv(1024).strip()
                    self.msg["msg"] = data
                    data = json.dumps(self.msg)
                    cost = utils.upload_data(data)
                    self.socket.send("Cost:" + str(cost) + "\n")
                elif option == "2":
                    self.socket.send("Ooops. Download not implemented yet in beta version\n")
                else:
                    self.socket.send("Bye\n")
                    self.socket.close()
                    return
        except Exception as e:
            print e
            return


while True:
    tcpsock.listen(4)
    print "\nListening for incoming connections..."
    (clientsock, (ip, port)) = tcpsock.accept()

    # Let's use a new thread for each incoming connection
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()
