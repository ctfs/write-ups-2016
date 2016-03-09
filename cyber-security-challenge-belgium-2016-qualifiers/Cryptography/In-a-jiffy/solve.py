# Gif file specification:
# http://giflib.sourceforge.net/whatsinagif/bits_and_bytes.html
# https://en.wikipedia.org/wiki/GIF#Example_GIF_file

# Looking at the structure of a GIF file we learn that the first 6 bytes of a GIF file are GIF87a or GIF89a 
# followed by 2 bytes indicating the width and 2 bytes indicating the height of the file.

# The flag file name hints that it is a 800 by 600 pixel image. Because of this we know the first 10 bytes and can derive the key used to encrypt the file

import struct

def expand_key(key, length):
	return (length / len(key)) * key + key[0:(length % len(key))]

def xor(s1, s2):
	assert len(s1) == len(s2)
	return ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(s1, s2)])


f = open('flag_800x400px.gif.enc')
enc = f.read()
f.close()

# We derive the two possible keys depending on the GIF version used

header = "GIF87a" + struct.pack("HH", 800, 400)
key1 = xor(header, enc[0:10])
key1 = expand_key(key1, len(enc))

header = "GIF89a" + struct.pack("HH", 800, 400)
key2 = xor(header, enc[0:10])
key2 = expand_key(key2, len(enc))

open("gif87.gif", "w").write( xor(key1, enc) )
open("gif89.gif", "w").write( xor(key2, enc) )