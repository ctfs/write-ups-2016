#!/usr/bin/env python2.7

import zipfile
import string
import random

flag = 'flag{th3_vi11i4n_w3_n33d_#freeleffen}'
flag += '\xAA' * (16 - len(flag) % 4) # pad with AA's


def generate_file():
    # just mash together a bunch of printable characters. It'll look like nonsense. Perhaps it'll red-herring them into spending time on nothing?
    # we could *really* red herring them if we put a constant header on the files ;)
    return ''.join([random.choice(string.printable) for _ in xrange(random.randint(100, 1000))])

def generate_filename():
    return ''.join(random.choice(string.lowercase + string.digits) for _ in range(10))

def zip(dst):
    src = "dir"
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    for x in range(len(flag)/4):
        arcname = 'out/' + generate_filename() # let's be nice and stick stuff in an out directory
        content = generate_file()
        zf.writestr(arcname, content, compress_type=random.choice([0,8]))
    curr_flag_pos = 0
    for info in zf.infolist():
        flag_chunk = flag[curr_flag_pos:curr_flag_pos+4]
        hexenc_flag = ''.join([hex(ord(x))[2:] for x in flag_chunk])
        fake_crc = int(hexenc_flag, 16)
        info.CRC = fake_crc

        # now just fuck with some attributes to confuse them
        info.file_size=0x133700f4ee13ff34 #1337 freeleffen
        info.create_version ^= random.randint(0,0xff)
        info.create_system ^= random.randint(0,0x0f)
        info.extract_version ^= random.randint(0,0xff)
        info.compress_type ^= random.randint(0x1,0xff)
        info.date_time = (1980, 10, 1, 6, 1, 5)
        curr_flag_pos += 4
    zf.close()

zip("evidence")
