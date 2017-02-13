# 33c3 CTF : feuerfuchs-600

**Category:** Pwn
**Points:** 600
**Solves:** 4
**Description:**

I need a calculator but only have a webrowser... Can you help me?

Your token for this challenge: ...

> > nc 78.46.224.85 $((0xf1f0))
> Welcome!
> 
> In this challenge you are asked to pwn a modified firefox and pop calc (xcalc to be specific). You can get the patch, as well as all other relevant files from here: [feuerfuchs-f23f889382ed13a0e185fe48132c56eebf2b87f3.tar.xz](ihttps://archive.aachen.ccc.de/33c3ctf.ccc.ac/uploads/feuerfuchs-f23f889382ed13a0e185fe48132c56eebf2b87f3.tar.xz)
> 
> This challenge will work as follows:
> 
> 1. I'll ask you for your token
> 
> 2. I'll ask you for a URL to your exploit
> 
> 3. I'll start up a container, and within that open Firefox with your URL
> 
> 4. I'll see if there is a calculator process (xcalc) running inside the container, in which case I'll send you the flag. You have 30 seconds to pop calc.
> 
> 5. I'll destroy the container
> 
> Enjoy!
> ~saelo

##Hints:

* Beware that the IFUNC mechanism (https://sourceware.org/glibc/wiki/GNU_IFUNC) can cause the same function to be resolved to different implementations at runtime, thus potentially causing a locally working exploit to fail on the server. If in doubt, contact saelo in IRC ;)

## Write-up

(TODO)

## Other write-ups and resources

* none yet
