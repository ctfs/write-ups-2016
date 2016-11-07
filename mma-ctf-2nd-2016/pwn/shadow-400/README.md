# MMA CTF 2nd 2016 : shadow-400

**Category:** Pwn
**Points:** 400
**Solves:** 29
**Description:**

> Host : pwn2.chal.ctf.westerns.tokyo
>
> Port : 18294
>
>
> [[shadow](./shadow)]([shadow](./shadow))


## Write-up

using negative values in message length provide us buffer overflow. due to task approach on protecting ret addrs,
we can use
tls_dtors_list to achieve code execution and run system("/bin/sh");

cookie is our problem so we need leaking it.

leaking libc addr can be done by overwriting message function args (break 0x0804890f)

for overwriting tls_dtors i need +1 step, this can be achieved by overwriting max steps(3) on stack with (0x4)

finally we overwrite tls_dtor with address of [system_addr, bin_sh_addr] which i used tls_dtor+0x10, stack addr cannot be used to reliable exploitation

## Other write-ups and resources

* https://github.com/ispoleet/ctf-writeups/tree/master/mma_ctf_2016/shadow
* [Amrita University bi0s](https://amritabi0s.wordpress.com/2016/09/09/mmactf-2nd-shadow-write-up/)
* http://hamidx9.ir/solutions/2016/tw_mma_ctf/shadow/sol.py
* http://uaf.io/exploitation/2016/09/05/TokyoWesterns-MMA-shadow.html
