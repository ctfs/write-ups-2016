# 33c3 CTF : read-eval-pwn-loop-525

**Category:** Pwn
**Points:** 525
**Solves:** 2
**Description:**

We want more people to use Lua so we've set up an interactive demo. We've disabled every unsafe API we know of and added some compile time hardenings (including a hardened musl-libc!) for extra security. Can you still read the flag from /flag?

	nc 78.46.224.72 1337

Get the compiled binary and libc as well as the changes to lua-5.3.3 and musl-1.1.15 [here](repl.tar.xz).

Note: yes, there are no changes apart from some disabled modules and compile time hardenings.

## Write-up

(TODO)

## Other write-ups and resources

* none yet
