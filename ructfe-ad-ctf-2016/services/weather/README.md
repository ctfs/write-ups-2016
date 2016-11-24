# RuCTFE CTF 2016 : weather

**Category:** Pwn
**Points:** 
**Solves:** 
**Description:**

This service was giving you current weather information when visiting it's
webservice via weather.teamX.ructfe.org or connection to the ctrl-interface
via teamX.ructfe.org:16761.
## Write-up

There is basic buffer overflow which reads `read(fd, buf, 0x1400)`
in a 0x400 byte sized buffer on the heap. Behind this buffer was another one
containing the format string for printing the weather info on the ctrl-interface.
So we can basically control this format string and have a classic fmtstr vuln.
The fmtstr is finally copied to the stack with `sprintf(stack_buf, fmtstr_buf, args...)`.

Here is a list of things the exploit has to perform:
* Get the fd, for our socket
* Find the elf-base address (ASLR)
* Find the libc-base address
* Write rop-chain to the heap (Null-bytes)
* Perform GOT-hijacking to call system (Not really necessary, could call libc-addresses directly)
* Pivot esp from stack to rop-chain on the heap
* Clean-up fmstr
* Return back to the original code so the service won't die
* Call system

This is just a really short write-up, but I added a lot of comments to the exploit,
which help to understand what's going on.

## Other write-ups and resources

* none yet
