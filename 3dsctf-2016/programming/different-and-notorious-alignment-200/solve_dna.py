"""
different_and_notorious_alignment
[PT-BR]
Acesse o servidor em 54.175.35.248:8001 
RTFM[ChOkO]
"""

#coding:utf-8
import socket

def countDiff(x,y):
    diffz = 0
    tamX = len(x)
    tamY = len(y)

    for i in xrange(tamX):
        if (x[i] == 'A' and y[i] == 'T') or (x[i] == 'G' and y[i] == 'C'):
            pass
        else:
            print '\t[%s] != [%s]' % (x[i],y[i])
            diffz+=1
    return diffz

host="54.175.35.248"
port=8001

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

r = s.recv(4096)

#print '[DEBUG]\n%s\n' % r
x = r.split(' ')[-2].replace(':','')
s.send(x+"\n")
print '[<] %s\n[>] %s' % (x,x)

print '-------------------------------'


for i in xrange(100):
    print '[ ROUND #%s ]' % i
    r = ''
    r = s.recv(1024)
    print '[<] %s' % r

    x = r.split('Stage')[1].split(' ')[5]
    y = r.split('Stage')[1].split(' ')[9]

    ans = str(countDiff(x,y))

    s.send(ans+"\n")
    print '[>] %s' % ans

    print '-----------------------------'

s.close()
