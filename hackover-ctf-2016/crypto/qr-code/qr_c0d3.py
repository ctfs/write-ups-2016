
import math
import time
import gmpy2
import numpy as np
from libnum.sqrtmod import jacobi
import numpy
rs = gmpy2.random_state(int(time.time()))


def unpack_bits(bites, n):
    s = ''.join('{:08b}'.format(B) for B in bites)[:n]
    return list(int(c) for c in s)


def read_file(f):
    line = f.readline()
    assert line == b'P4\n'
    rows, cols = (int(i) for i in f.readline().split())
    data = np.ndarray((rows, cols), dtype=int)
    for i in range(rows):
        n_bytes = math.ceil(cols / 8)
        bits = unpack_bits(f.read(n_bytes), cols)
        for j in range(cols):
            data[i, j] = bits[j]
    return data


def keygen(size):
    rs = gmpy2.random_state(int(time.time()))
    p = gmpy2.next_prime(gmpy2.mpz_urandomb(rs, size))
    while p % 4 != 3:
        p = gmpy2.next_prime(p)
    q = gmpy2.next_prime(p)
    while q % 4 != 3:
        q = gmpy2.next_prime(q)
    n = p*q
    x = n-1
    return (x, n), (p, q)


def break_keygen(n):
    
    start_val = 1475784906
    while True:
        rs = gmpy2.random_state(start_val)
        p = gmpy2.next_prime(gmpy2.mpz_urandomb(rs, 2048))
        while p % 4 != 3:
            p = gmpy2.next_prime(p)
    
        if n % p == 0:
            print p
            break
        start_val -= 1



def encrypt(pub, plaintext):

    def randg(n):
        y = gmpy2.mpz_random(rs, n)
        while gmpy2.gcd(y, n) != 1:
            y = gmpy2.mpz_random(rs, n)
        return y

    x, n = pub
    ciphertext = [(randg(n)**2 * x**b) % n
                  for b in plaintext]
    return ciphertext


def main():
    with open('flag.pbm', 'rb') as f:
        data = read_file(f)

    pub, _ = keygen(2048)
    with open('flag.pbm.enc', 'w') as f:
        x, n = pub
        f.write('x = {}\n'.format(x))
        f.write('n = {}\n'.format(n))
        f.write('rows = {}\n'.format(data.shape[0]))
        f.write('cols = {}\n\n'.format(data.shape[1]))
        for c in encrypt(pub, data.flat):
            f.write('{}\n'.format(c))


if __name__ == '__main__':
    f = open('flag.pbm.enc', 'r')
    x = f.readline().split()
    n = f.readline().split()
    n = int(n[-1])
    #break_keygen(n)
    p = 22250306827784715733283062128193677290021836024300489570709599202115926462302919976104520475770620608163557273901249985850005137090439882327585236665684669394670465240878675379943769961383455883823553180768037439715655143722265675380059231411902916425879836917950398675033311091214755225333868591298970375872242585296609513792539237228378437137800519388754607571027221647878664443668547789406536838722872829498112769424741955285673756857212860339558767970041783444629359810777280525857414547435135414691954819332038557708029354617237786225851984032666165772457515709803023490987886473030798730615844852872155726221247
    q = 22250306827784715733283062128193677290021836024300489570709599202115926462302919976104520475770620608163557273901249985850005137090439882327585236665684669394670465240878675379943769961383455883823553180768037439715655143722265675380059231411902916425879836917950398675033311091214755225333868591298970375872242585296609513792539237228378437137800519388754607571027221647878664443668547789406536838722872829498112769424741955285673756857212860339558767970041783444629359810777280525857414547435135414691954819332038557708029354617237786225851984032666165772457515709803023490987886473030798730615844852872155726222747
    
    
    
    print p-q
    print f.readline()
    print f.readline()
    print f.readline()
    
    import scipy.misc, numpy
    from libnum.sqrtmod import jacobi
    
    
    
    A = []
    
    for i in range(0, 37):
        b = []
        for j in range(0, 37):
            s = int(f.readline())
            if jacobi(s,p) == 1:
                b.append(0)
            else:
                b.append(1)
        A.append(b)
    scipy.misc.imsave('outfile.jpg', numpy.array(A))
    
    

