from Crypto.Cipher import AES
import threading
import socket
import sys
import os


class ClientThread(threading.Thread):

    def __init__(self,ip,port,socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.flag = "xxxxx"
        self.count = -1
        print "[+] New thread started for "+ip+":"+str(port)

    def makeBlocks(self, data):
        return [data[i:i+16] for i in range(0, len(data), 16)]

    def encrypt(self, plain, IV, key):
        self.count += 1
        CTR = bin((self.count) % 16)[2:].zfill(4)
        feed = IV + CTR
        cipher = AES.new(key, AES.MODE_ECB)
        keystream = cipher.encrypt(feed)
        return self.xor(keystream, plain)

    def xor(self, keystream, data):
        out = []
        for idx, ch in enumerate(data):
            out.append(chr(ord(ch) ^ ord(keystream[idx % 16])))
        return ''.join(out)

    def run(self):
        print "Connection from : "+ip+":"+str(port)
        key = os.urandom(16)
        IV = os.urandom(12)
        outputBuffer = []
        blocks = self.makeBlocks(self.flag)
        for block in blocks:
            outputBuffer.append(self.encrypt(block, IV, key))

        while True:
            data = self.socket.recv(1024).strip('\n')
            if data == "stop":
                self.socket.send(str(outputBuffer) + "\n")
                self.socket.close()
                sys.exit(0)
            if len(data) % 16 != 0:
                self.socket.send("Invalid: {0}".format(data) + "\n")
                continue
            blocks = self.makeBlocks(data)
            for block in blocks:
                outputBuffer.append(self.encrypt(data, IV, key))

        print "Client disconnected..."
       	self.socket.close()

host = "0.0.0.0"
port = 5968

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))
threads = []

while True:
    tcpsock.listen(4)
    print "\nListening for incoming connections..."
    (clientsock, (ip, port)) = tcpsock.accept()

    # Let's use a new thread for each incoming connection
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()