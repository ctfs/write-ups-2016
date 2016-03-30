# Boston Key Party CTF 2016 : More Like ZKP

**Category:** Crypto
**Points:** 4 
**Description:** 

> We've made a zero-knowledge proof protocol for graph 3-coloring. 
Here are prover (52.86.232.163:32795) and verifier (52.86.232.163:32794) 
servers. 
Convince the verifier that you know the prover's graph-coloring! 
https://s3.amazonaws.com/bostonkeyparty/2016/48cdc8756b6a9a5052c6da2d061b9bd61d13a1fa.tgz

## Write-up

**by [LosFuzzys](https://hack.more.systems)**

The proof is based on a three-colored graph, where the graph was given,
but the colors not.

graph.txt:

```
# 683
129 495
129 613
1 2
2 489
2 507
3 507
3 495
495 613
215 489
215 613
...
```

In the proving step, the colors (AES encrypted) have to be sent to the 
verifier. The verifier selects one random edge, asks for the keys,
and checks if the vertices on the edge have the same color. 
If not, the process is repeated 1000 times. A successful proof is
rewarded with the flag.

```go
func handle_connection(conn net.Conn) {
    defer func() {
        e := recover()
        if e != nil {
            if uerr, ok := e.(UserError); ok {
                conn.Write([]byte(uerr.Error()))
            }
        }
        conn.Close()
    }()

    successes := 0
    for {
        // Get the colors
        ciphers := get_colors(conn)
        // Send a challenge (pair of vertices)
        v1, v2 := gen_challenge()
        send_challenge(conn, Edge{v1, v2})
        // Get the AES keys
        k1, k2 := get_keys(conn)
        if decrypt(ciphers[v1], k1) == decrypt(ciphers[v2], k2) {
            // Colors don't match!
            panic(UserError{"Those are the same color!"})
            return;
        }
        successes += 1
        if successes == THRESHOLD {
            // Okay, I believe you
            conn.Write([]byte("BKPCTF{" + flag + "}"));
            conn.Close()
            return
        }
    }
}
```

Our first try was to connect the prover and verifier with netcat:

```
mkfifo backpipe
nc 52.86.232.163 32794 0<backpipe | nc 52.86.232.163 32795 1>backpipe
```

But the prover sets some bytes, that the verifier doesn't accept. But
worse, the prover answers with random colors! So a complete new attempt
must be found.

Thanks to @meisterluk, we found out, that a SAT solver is useful for
graph three-coloring. There are two conditions, that have to be
satisfied:

* Every vertex has one of the three colors.
* Not the same color on one edge.

The SAT solver runs for less than a second until the colors are found.
All colors are encrypted with a static key (```MASTER_KEY```) and
then sent to the verifier. The step took some minutes, since several
megabytes have to be transmitted. The reason is, because the colors
have to be sent 1000 times.

Attack script:

```python
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
```

Output:

```
0: (77, 355)
1: (548, 578)
2: (429, 624)
3: (138, 406)
...
996: (195, 661)
997: (385, 596)
998: (283, 411)
999: (7, 193)
BKPCTF{4c3b35aaade7843c8c97}
```
