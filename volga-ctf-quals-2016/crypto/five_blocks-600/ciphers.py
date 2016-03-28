import array
import struct



"""
    bc1
"""

def list_xor(l1, l2):
    return array.array('B', map(lambda x: x[0]^x[1], zip(l1,l2)))

def rot(x):
    return ((x<<4) | (x>>4)) & 0xff

def g_box(a, b, mode):
    return rot((a + b + mode) & 0xff)

def f_box(x):
    t0 = (x[2] ^ x[3])
    y1 = g_box(x[0] ^ x[1], t0, 1)
    y0 = g_box(x[0], y1, 0)
    y2 = g_box(y1, t0, 0)
    y3 = g_box(y2, x[3], 1)
    return array.array('B', [y0, y1, y2, y3])


class bc1(object):

    def __init__(self, key_data):
        assert (len(key_data) == 6*4)
        self.subkeys = []
        for i in xrange(0, 6*4, 4):
            self.subkeys.append(array.array('B', key_data[i:i+4]))

    def encrypt_block(self, plaintext):
        plaintext = array.array('B', plaintext)
        pleft = plaintext[0:4]
        pright = plaintext[4:]

        left = list_xor(pleft, self.subkeys[4])
        right = list_xor(pright, self.subkeys[5])
        R2L = list_xor(left, right)
        R2R = list_xor(left, f_box(list_xor(R2L, self.subkeys[0])))
        R3L = R2R
        R3R = list_xor(R2L, f_box(list_xor(R2R, self.subkeys[1])))
        R4L = R3R
        R4R = list_xor(R3L, f_box(list_xor(R3R, self.subkeys[2])))

        cipherLeft = list_xor(R4L, f_box(list_xor(R4R, self.subkeys[3])))
        cipherRight = list_xor(cipherLeft, R4R)
        return ''.join(map(chr, cipherLeft + cipherRight))

    def decrypt_block(self, ciphertext):
        ciphertext = array.array('B', ciphertext)
        cipherLeft = ciphertext[0:4]
        cipherRight = ciphertext[4:]

        R4R = list_xor(cipherLeft,cipherRight)
        R4L = list_xor(cipherLeft, f_box(list_xor(R4R, self.subkeys[3])))
        R3R = R4L
        R3L = list_xor(R4R, f_box(list_xor(R3R, self.subkeys[2])))
        R2R = R3L
        R2L = list_xor(R3R, f_box(list_xor(R2R, self.subkeys[1])))
        left = list_xor(R2R, f_box(list_xor(R2L, self.subkeys[0])))
        right = list_xor(left, R2L)

        pleft = list_xor(left, self.subkeys[4])
        pright = list_xor(right, self.subkeys[5])
        return ''.join(map(chr, pleft + pright))



"""
    bc2
"""

def split_int(m):
    return ((m>>16) & 0xFFFF, m & 0xFFFF)

def join_int(l, r):
    return (l<<16) | r

def orth(m):
    (l, r) = split_int(m)
    return join_int(r, l ^ r)

def inv_orth(m):
    (l, r) = split_int(m)
    return join_int(l ^ r, l)

def F(m, subkey):
    (l, r) = split_int(m)
    (k_l, k_r) = split_int(subkey)
    (mul_l, mul_r) = split_int(l * r)
    l = ((mul_l + r) * k_l) & 0xFFFFFFFF
    r = ((mul_r * l) + k_r) & 0xFFFFFFFF
    l = ((l<<7) | (l>>25)) & 0xFFFFFFFF
    r = ((r<<18) | (r>>14)) & 0xFFFFFFFF
    return r ^ l


def M(L, R, subkey):
    A = F((L - R) & 0xFFFFFFFF, subkey)
    CL = orth((L + A) & 0xFFFFFFFF)
    CR = (R + A) & 0xFFFFFFFF
    return (CL, CR)

def inv_M(L, R, subkey):
    L = inv_orth(L)
    A = F((L - R) & 0xFFFFFFFF, subkey)
    PL = (L - A) & 0xFFFFFFFF
    PR = (R - A) & 0xFFFFFFFF
    return (PL, PR)


class bc2(object):

    def __init__(self, key):
        (k0, k1, k2, k3) = struct.unpack('>HHHH', key)
        K0 = pow(k0, 2)
        K1 = pow(k1, 2)
        K2 = pow(k2, 2)
        K3 = pow(k2, 2)
        self.subkeys = [K0, K1, K2, K3]

    def encrypt_block(self, plaintext):
        (L0, R0) = struct.unpack('>II', plaintext)
        (L1, R1) = M(L0, R0, self.subkeys[0])
        (L2, R2) = M(L1, R1, self.subkeys[1])
        (L3, R3) = M(L2, R2, self.subkeys[2])
        (CL, CR) = M(L3, R3, self.subkeys[3])
        return struct.pack('>II', CL, CR)

    def decrypt_block(self, ciphertext):
        (L0, R0) = struct.unpack('>II', ciphertext)
        (L1, R1) = inv_M(L0, R0, self.subkeys[3])
        (L2, R2) = inv_M(L1, R1, self.subkeys[2])
        (L3, R3) = inv_M(L2, R2, self.subkeys[1])
        (PL, PR) = inv_M(L3, R3, self.subkeys[0])
        return struct.pack('>II', PL, PR)



"""
    bcs
"""

def block_xor(b1, b2):
    return ''.join([chr(ord(a) ^ ord(b))  for a,b in zip(b1, b2)])

def pad(data, bs=8):
    r = len(data) % bs
    add_len = bs - r if r != 0 else bs
    add = '\x80' + '\x00'*(add_len-1)
    return data + add

def unpad(data, bs=8):
    i = 1
    while data[-i] == '\x00': i += 1
    return data[:-i]


class bcs(object):

    def __init__(self, key_bc1, key_bc2):
        self.bc1 = bc1(key_bc1)
        self.bc2 = bc2(key_bc2)

    def encrypt(self, data, iv):
        ciphertext = ''
        data = pad(data)
        C = iv
        for i in xrange(0, len(data), 8):
            A1 = self.bc1.encrypt_block(array.array('B', data[i:i+8]))
            A2 = self.bc2.decrypt_block(A1)
            ciphertext += block_xor(A2, C)
            C = A1
        return ciphertext

    def decrypt(self, data, iv):
        plaintext = ''
        C = iv
        for i in xrange(0, len(data), 8):
            A2 = block_xor(data[i:i+8], C)
            A1 = self.bc2.encrypt_block(A2)
            plaintext += self.bc1.decrypt_block(array.array('B', A1))
            C = A1
        return unpad(plaintext)


"""
    checks
"""

def check_all():
    import os
    import random
    checks_number = 500
    # padding
    for n in xrange(0, checks_number, 1):
        data = os.urandom(n)
        data_padded = pad(data)
        assert (len(data_padded) % 8 == 0)
        data_unpadded = unpad(data_padded)
        assert (data == data_unpadded)
    # bc1
    for i in xrange(checks_number):
        cryptor = bc1(os.urandom(4*6))
        for j in xrange(checks_number):
            plaintext = os.urandom(8)
            ciphertext = cryptor.encrypt_block(plaintext)
            decrypted = cryptor.decrypt_block(ciphertext)
            assert (decrypted == plaintext)
    # bc2
    for i in xrange(checks_number):
        cryptor = bc2(os.urandom(8))
        for j in xrange(checks_number):
            plaintext = os.urandom(8)
            ciphertext = cryptor.encrypt_block(plaintext)
            decrypted = cryptor.decrypt_block(ciphertext)
            assert (decrypted == plaintext)
    # bcs
    for i in xrange(checks_number):
        cryptor = bcs(os.urandom(4*6), os.urandom(8))
        l = random.randrange(100, 801)
        plaintext = os.urandom(l)
        iv = os.urandom(8)
        ciphertext = cryptor.encrypt(plaintext, iv)
        decrypted = cryptor.decrypt(ciphertext, iv)
        assert (decrypted == plaintext)



if __name__ == '__main__':
    check_all()
