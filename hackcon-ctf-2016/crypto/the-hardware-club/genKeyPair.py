from Cryptodome.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Cryptodome.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode
from genLargePrimes import generateLargePrime

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

p = 169530237952573748368189799955682467382981190128045440195079928264906866742107349991159212259885000722467900686913850878305620267449769263730115304350546079431887015026437175510788840243478206301763434168031512699332213142859495368291002844907298298139858769109574355617458546385307241287393358156444715347793
q = 152588087402514219857833878620153666945304685640627758617917943381504393210558706803164637632719012980584990911366861074062265597247464995913960044489757238590130973545737766726863067136702127127671612008426543868375658445766104812898282701044498346675255344027978615813725491513556318640569390490700167272861

phi_n = (p - 1)*(q - 1)

e2 = generateLargePrime(256)
while 'Failure' in str(e2)[:len('Failure')]:
    e2 = generateLargePrime(256)
d2 = modinv(e2, phi_n)

key2 = RSA.construct((p*q, e2, d2, p, q))

print "Private Key:\n"
print key2.exportKey('PEM')

print "Public Key:\n"
print key2.publickey().exportKey('PEM')
