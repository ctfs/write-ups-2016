# Nowadays in the times of cyber warfare it is important that code provided by
# attackers is executed in a safe way. Our shellcode prevention technology,
# dubbed "stone soup", has provided us with years of sekjurity.
# You'll find this service to be running on the interwebz.

import ctypes
import keystone
import mmap
import struct
import sys

def xs128p(state0, state1):
    # https://blog.securityevaluators.com/hacking-the-javascript-lottery-80cc437e3b7f
    s1 = state0 & ((1 << 64) - 1)
    s0 = state1 & ((1 << 64) - 1)

    s1 ^= (s1 << 23) & ((1 << 64) - 1)
    s1 ^= (s1 >> 17) & ((1 << 64) - 1)
    s1 ^= s0 & ((1 << 64) - 1)
    s1 ^= (s0 >> 26) & ((1 << 64) - 1)

    state0 = state1 & ((1 << 64) - 1)
    state1 = s1 & ((1 << 64) - 1)

    generated = (state0 + state1) & ((1 << 64) - 1)
    return state0, state1, generated

def prng():
    state0, state1 = struct.unpack("QQ", "HACKINTHEBOX2016")
    while True:
        state0, state1, value = xs128p(state0, state1)
        yield value

ks = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
p = prng()

buf = sys.stdin.read(0x10000).replace(";", "\n")

regs = [
    "rax", "rbx", "rcx", "rdx", "rbp", "rsi", "rdi",
    "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15",
]

insns = []

for x in xrange(15):
    insns.append("mov %s, 0x%x" % (regs[x], next(p)))

for insn in buf.split("\n"):
    if not insn.strip():
        continue

    insns.append(insn.strip())

    for x in xrange(8):
        insns.append("mov %s, 0x%x" % (regs[next(p) % 15], next(p)))

insns.append("int 3")
encoding, count = ks.asm("\n".join(insns))

mem = mmap.mmap(
    -1, len(encoding), mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS,
    mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC
)

mem.write("".join(map(chr, encoding)))

# I mean, why would the mmap module expose a way to obtain the address
# of the mmap()'d page(s)?
addr = struct.unpack("Q", ctypes.string_at(id(mem) + 16, 8))[0]

ctypes.CFUNCTYPE(None)(addr)()
