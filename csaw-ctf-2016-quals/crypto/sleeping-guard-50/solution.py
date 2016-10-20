import struct
def get_bytes_from_file(filename):  
    return open(filename, "rb").read()  

# ME ENCRYPTING THE FILE
test = get_bytes_from_file("./magic.png")
print len(test)

key = "WoAh_A_Key!?"
enc = []
index = 0
for b in test:
    enc.append(ord(b) ^ ord(key[index % len(key)]))
    index += 1

# get base64 from server
# write bytes to file
# decode as follows taking advantage of the PNG MAGIC HEADER
f = open('solution.png', 'wb')
f.write(''.join([struct.pack("B",x) for x in enc]))
f.close()

# test to recover key
test = open('sleeping.png', 'rb').read()
PNG_HEADER = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0d]
flag = ""
index = 0
for b in PNG_HEADER:
    flag += chr(ord(test[index]) ^ b)
    index += 1
print flag
