# ABCTF 2016 : hide-and-seek-50

**Category:** Pwn
**Points:** 50
**Solves:** 176
**Description:**

There is a flag hidden somewhere in this binary. Good luck!

## Write-up

The binary is in Mach-O format and we didn't had a Mac around to let it run.
So we used radare2 in order to do a emulated.

1. Load the binary and start analysis
  * r2 -A haha1

2. Enumeration
  * afl:

    ```
    [0x100000ef0]> afl
    0x100000e00    4 105          sym._decrypt
    0x100000e70    3 121          sym._totallyNotTheFlag
    0x100000ef0    3 69           entry0
    0x100000f36    1 6            sym.imp.__stack_chk_fail
    0x100000f3c    1 6            sym.imp.printf
    0x100000f42    1 6            sym.imp.strlen
    ```

  * V @ entry0

    ```
    0x100000ef8      c745fc000000.  mov dword [rbp - local_4h], 0                                                                                                                                         
    0x100000eff      c745f8070000.  mov dword [rbp - local_8h], 7                                                                                                                                         
    0x100000f06      8b45f8         mov eax, dword [rbp - local_8h]                                                                                                                                       
    0x100000f09      83e804         sub eax, 4                                                                                                                                                            
    0x100000f0c      83f800         cmp eax, 0                                                                                                                                                            
    0x100000f0f      0f8505000000   jne 0x100000f1a            ;[1]                                                                                                                                       
    0x100000f15      e856ffffff     call sym._totallyNotTheFlag ;[2]
    ```
   * V @ sym.\_totallyNotTheFlag

     ```
     0x100000eb0      e84bffffff     call sym._decrypt          ;[2]                                                                                                                                       
     0x100000eb5      488d3ddc0000.  lea rdi, qword [rip + 0xdc] ;[3] ; 0x100000f98 ; "%s."                                                                                                                
     0x100000ebc      488d75e0       lea rsi, qword [rbp - local_20h] ;[1]                                                                                                                                 
     0x100000ec0      b000           mov al, 0                                                                                                                                                             
     0x100000ec2      e875000000     call sym.imp.printf
     ```

 3. Conclusion
  * We made a little guess here: We have an opaque predicate at 0x100000f0c, which will
 always result into false. If it would be evaluated as true, totallyNotTheFlag would be called.
 This decrypts a string in the binary and print on stdout, which might be our flag.

4. Options
  * We could either reverse the encryption algorithm and decrypt the flag ourselves or use
 radare2 ESIL ('Evaluable Strings Intermediate Language') functionality to emulate the algorithm.


5. Solution
  * We went with the second option
  * Start the ESIL-engine
    * aei
    * aeim
    * aeip
  * Set breakpoint to compare @ 0x100000f0c
    * aesu 0x100000f0c
  * Change eax value to 0 in order skip the jump
    * aer eax = 0
    * ar
    ```
        rax = 0x00000000
        ...
        rip = 0x100000f0c
        ...
    ```
  * Step to see that jump was not taken:
    * aes
    * aes
    * ar
    ```
        ...
        rip = 0x100000f15 -> sym._totallyNotTheFlag
        ...
    ```

  * Set breakpoint to printf after decrypt @ 0x100000ec2
    * aesu 0x100000ec2
  * Check parameters for printf
    * ps @ rdi

    ```
        %s
    ```
    * ps @ rsi

    ```
        CTF{w0w_b1NarY_1s_h@rd}
    ```

Here we go!:)
Sadly this was the only real binary challenge in ABCTF. Given that it was beginner CTF this seems
reasonable. However in my opinion only practice makes perfect, so don't be afraid to spread some mor
if you're ever hosting a beginner CTF,  or a CTF in general!

More about ESIL can be found [here](https://radare.gitbooks.io/radare2book/content/esil.html)


## Other write-ups and resources

* none yet
