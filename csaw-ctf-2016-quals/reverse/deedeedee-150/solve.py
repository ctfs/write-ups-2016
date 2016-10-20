from itertools import cycle
import subprocess

def xor(s1, s2, enc_add):
    return ''.join(chr(ord(a) ^ ord(b) ^ enc_add) for a,b in zip(cycle(s1), s2))

keys = [str(x)*3 for x in range(1, 500)]

# pull the encoded stuff out of the program's output
out, _ = subprocess.Popen(['./deedeedee'], stdout=subprocess.PIPE).communicate()
hex_enc = out.split('\n')[0].split()[-1]
enc = hex_enc.decode('hex')

for key in keys:
    enc_add = len(enc) & 0xFF;
    enc = xor(key, enc, enc_add)

print enc
