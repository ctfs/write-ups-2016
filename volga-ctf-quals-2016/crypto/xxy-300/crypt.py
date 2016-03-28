#!/usr/bin/env sage
from sage.all import *


hRR = RealField(10000)


def read_mat(name):
    with open(name, 'r') as f:
        data = f.read()
        data = [map(int, s.split(' '))  for s in data.split('\n')]
        n = len(data)
        M = MatrixSpace(ZZ, n, n)(data)
        return M

def read_ciphertext(ciphertext_file_name):
    with open(ciphertext_file_name, 'r') as f:
        data = f.read()
        e = vector(map(int, data.split(' ')))
        return e


def encrypt(plain_block, W, delta=151):
    n = W.ncols()
    m = vector([ord(ch)  for ch in plain_block])
    r = random_vector(ZZ, n, x=-delta+1, y=delta)
    e = m * W + r
    return e

def decrypt(e, V, W):
    n = V.ncols()
    VV = MatrixSpace(hRR, n, n)(V)
    t = vector([int(round(i))  for i in VV.solve_left(e)])
    v = t * V
    m = W.solve_left(v)
    ciphertext_block = ''.join([chr(i)  for i in m])
    return ciphertext_block


if __name__ == '__main__':
    V = read_mat('key.private')
    W = read_mat('key.public')
    e = read_ciphertext('ciphertext')
    print decrypt(e, V, W)
