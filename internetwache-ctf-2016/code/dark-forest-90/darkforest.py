from __future__ import print_function
from pwnlib.tubes.remote import remote
from pwnlib import context
import ast
 
class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
 
    def print_tree(self):
        if self.right:
            self.right.print_tree()
        print(self.data,)
        if self.left:
            self.left.print_tree()
 
    def gettree(self, tree):
        tree.append(self.data)
        if self.right:
            self.right.gettree(tree)
        if self.left:
            self.left.gettree(tree)
        return tree
 
    def insert(self, data):
        if self.data:
            if data <= self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data
 
def buildtree(mylist):
    root = Node(mylist.pop(0))
    for i in mylist:
        root.insert(i)
    ouput = []
    return root.gettree(ouput)
 
r = remote('188.166.133.53', 11491)
print(r.recvline())
while True:
    graph = r.recvline()
    print(graph)
    graph = graph.split('[')[1].split(']')[0]
    graph = '[' + graph + ']'
    print(graph)
    mylist = ast.literal_eval(graph)
    answer = repr(buildtree(mylist))
    print(answer)
    print(r.sendlinethen('\n',answer))