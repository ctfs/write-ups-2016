import random
import socket, threading
import os
from subprocess import Popen, PIPE
import time
import fcntl

def non_block_read(output):
    fd = output.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    try:
        return output.read()
    except:
        return ""

class workingThread(threading.Thread):
	def __init__(self, client, ip, port):
		threading.Thread.__init__(self)
		self.client = client
		self.ip = ip
		self.port = port

	def run(self):
		client.sendall("Welcome to Sheldon Cooper presents \"Fun with Bins\"\n")
		client.sendall("In the second episode, we're going to have fun pwning simple binaries\n")
		client.sendall("I will send you a random binary. To pass the stage, you'll need to give me the input that runs the \"cat flag\" shellcode on the system\n" )
		client.sendall("Lets get started\n\n")

		bins = ['283', '375', '324', '297', '190', '411', '435', '351', '484', '150', '189', '242', '189', '268', '205', '156', '359', '450', '400', '278', '374', '189', '318', '226', '305', '439', '180', '303', '189', '399', '445', '154', '216', '392', '218', '346', '320', '260', '298', '329', '492', '363', '160', '174', '310', '178', '332', '222', '495', '407', '265', '442', '157', '462', '302', '258', '414', '453', '437', '229', '209', '307', '466', '385', '269', '461', '248', '173', '220', '309', '358', '495', '438', '295', '419', '386', '486', '339', '262', '268', '182', '493', '357', '340', '371', '381', '236', '430', '372', '479', '175', '189', '467', '352', '366', '370', '494', '396', '234', '458']
		failed = 0
		for a in range(1, 32):
			b = random.randint(0, 99)
			client.sendall("-> Round %d\n" % (a,))
			binary_name = bins[b]
			print binary_name
			fp = open('abc/' + binary_name, 'rb')
			client.sendall(fp.read())
			
			client.sendall("\nI am running this binary for you in chroot\n")
			#ad = Popen(['./a.out'], stdin=PIPE, stdout=PIPE)
			ad = Popen(['./chroot-empty','third_empty-chroot',binary_name], stdin=PIPE, stdout=PIPE)
			ad.stdout.flush()
			ad.stdin.flush()
			time.sleep(1)
			initial_output = non_block_read(ad.stdout)
			print initial_output
			client.sendall('\n%s\n' % (initial_output,))
			client.sendall('\nYou got the pwn? ')

			client.settimeout(5.0)
			data = client.recv(600)

			# we have the payload, lets try it
			output = ad.communicate(input=data)[0]
			if "HACKCON{LEVEL_FLAG}" not in output:
				failed = 1
				break

		if not failed:
			client.sendall("Flag is HACKCON{IjustInventedAToolOfMassDestruction}\n")

		else:
			client.sendall("HAHAHAHAHA! You amuse me.\n")
			client.close()

tcpsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsocket.bind(("0.0.0.0",9092))
tcpsocket.listen(50)
#print "heey"
while 1:
	(client,(ip,port))=tcpsocket.accept()
	print client, ip, port
	newthread= workingThread(client,ip,port)
	newthread.start()
