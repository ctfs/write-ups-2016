# SECCON CTF Quals 2016 : microcomputer-500

**Category:** Binary
**Points:** 500
**Solves:** 13
**Description:**

Remote debugging of a micro computer.
The server is running on GDB simulator with special patch.

* Connect to the server.
     
    $ telnet micro.pwn.seccon.jp 10000
    $ echo '+$g#67+' | nc micro.pwn.seccon.jp 10000
    
    A long connection is disconnected automatically.
     
* Read "flag.txt" on current directory.

Reference:

* Assembly samples for many architectures
     
 cross-20130826.zip
 ref: <http://kozos.jp/books/asm/cross-20130826.zip>
     
 See the assembly samples.
     
    $ unzip cross-20130826.zip
    $ cd cross/sample
    $ ls *.d

 See the sample programs running on GDB simulator.

    $ cd cross/exec
    $ ls *.d

## Write-up

(TODO)

## Other write-ups and resources

* https://github.com/q3k/ctf/tree/master/SECCON2016Quals/microcomputer
