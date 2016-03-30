#!/usr/bin/env python2
from __future__ import print_function
from satispy import Variable, Cnf
from satispy.solver import Minisat
import socket
import struct
from Crypto.Cipher import AES

VERTICES = 683

def readGraphFile():
    graph_file = open('graph.txt', 'r')
    graph = []
    for line in graph_file:
        if line[0] != '#':
            nums = list(map(int, line[:-1].split(' ')))
            graph.append(nums)

    graph_file.close()
    return graph

graph = readGraphFile()

exp = Cnf()
c1 = dict()
c2 = dict()
c3 = dict()

# one of the three colors for a vertex
for vertex in range(VERTICES):
    c1[vertex] = Variable('edge%dhasColor1' % vertex)
    c2[vertex] = Variable('edge%dhasColor2' % vertex)
    c3[vertex] = Variable('edge%dhasColor3' % vertex)
    
    # one of three
    exp &= c1[vertex] | c2[vertex] | c3[vertex]
    exp &= c1[vertex] | -c2[vertex] | -c3[vertex]
    exp &= -c1[vertex] | c2[vertex] | -c3[vertex]
    exp &= -c1[vertex] | -c2[vertex] | c3[vertex]
    
# not same color on one edge
for edge in graph:
    begin = edge[0]
    end = edge[1]
    exp &= -c1[begin] | -c1[end]
    exp &= -c2[begin] | -c2[end]
    exp &= -c3[begin] | -c3[end]

# solve it
solver = Minisat()
solution = solver.solve(exp)

colors = [0] * VERTICES
if solution.success:
    print("Found a solution:")
    for vertex in range(VERTICES):
        if solution[c1[vertex]]:
            colors[vertex] = 1
        if solution[c2[vertex]]:
            colors[vertex] = 2
        if solution[c3[vertex]]:
            colors[vertex] = 3
    print(colors)
else:
    print("The expression cannot be satisfied")
    
    
# CHECK FOR ERRORS -----------------------------------------------------
error_detected = False
for edge in graph:
    if colors[edge[0]] == colors[edge[1]]:
        print(str(edge))
        error_detected = True
if error_detected == False:
    print("ok")
else:
    print("ERROR")


# CREATE ENCRYPTED COLORS ----------------------------------------------
MASTER_KEY = "0123456789ABCDEF"

colors_enc = []
for color in colors:
    cipher = AES.new(MASTER_KEY, AES.MODE_ECB, '')
    color = struct.pack("IIII", color, 0, 0, 0)
    colors_enc.append(cipher.encrypt(color))


# TCP TO VERIFIER ------------------------------------------------------
TCP_IP = '52.86.232.163'
TCP_PORT = 32794 # verifier
BLOCK_SIZE = 16
VERTICES = 683
FLAGSTART = "BKPCTF{"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.settimeout(60.0)

for i in range(1000):
    s.send("".join(colors_enc))
    challange = s.recv(8)
    cx = struct.unpack(">II", challange)
    print("%d: " % i, end="")
    print(cx)
    s.sendall(MASTER_KEY)
    s.sendall(MASTER_KEY)

resp = s.recv(50)
print(resp)
s.close()
