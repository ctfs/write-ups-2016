# Cyber Security Challenge 2016: Mindblown 

**Category:** Reverse Engineering  
**Points:** 50  
**Challenge designer:** Mathy Vanhoef  
**Description:**  
> [This binary](challenge-source-files/mindblown64) is running on the server at 52.50.58.101:1337. Try and get the flag!

## Write-up
Let's run the program
```bash
» ./mindblown64
Failed to open flag file (null): Bad address
```
Looks like the program expects a file which hold the flag.  
Lets create an empty file and give it to the program
```bash
» touch flagfile
» ./mindblown64 flagfile
Failed to read 20-character flag from flagfile: Success
```
Now we know the flag is a 20 character string.  
Enter 20 characters into the file and run the program once again.
```bash
» echo '01234567890123456789' > flagfile
» ./mindblown64 flagfile
Alarm clock
```
The program does nothing and then exit after 2-3 seconds.

Investigating the binary in a debugger reveals that it's a "brainfuck" binary that expects "CSCBE16" as encoded input in order to retrieve the flag. The following python snippet generates this:

```python
#!/usr/bin/env python2
print ">".join(["+" * ord(c) for c in "CSCBE16"])
```

```bash
» python solution.py
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>+++++++++++++++++++++++++++++++++++++++++++++++++>++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

Sending this input to the server IP address and port 1337 reveals the flag:

```bash
» python solution.py | nc 52.50.58.101 1337
You win, the flag is letmeblowyourmindddd
```
