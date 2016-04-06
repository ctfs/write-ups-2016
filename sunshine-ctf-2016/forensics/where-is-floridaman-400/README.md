# Sunshine CTF 2016 : Where is florida man

**Category:** Forensics
**Points:** 400
**Solves:** ?
**Description:**

> Description: 
> 

## Write-up

Unzipping the file we're given and running file:
```bash
[fagrant@ctf ~]$ file whereisfloridaman 
whereisfloridaman: DOS/MBR boot sector MS-MBR Windows 7 english at offset 0x163 "Invalid partition table" at offset 0x17b "Error loading operating system" at offset 0x19a "Missing operating system", disk signature 0x4030201
```

After some manual looking around in a hexdump tool, I decided to retrieve all MFT entries:
```
$ vol.py -f whereisfloridaman mftparser --output-file=huehue.txt 
```

Between all the entries, we get the following two:
```
MFT entry found at offset 0x3d619908
Attribute: In Use & File
Record Number: 35
Link count: 2

$STANDARD_INFORMATION
Creation                       Modified                       MFT Altered                    Access Date                    Type
------------------------------ ------------------------------ ------------------------------ ------------------------------ ----
2016-03-11 01:52:26 UTC+0000 2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   Archive

$FILE_NAME
Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
2016-03-11 01:52:26 UTC+0000 2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   FL<E9><97><9A>RID~1.7Z

$FILE_NAME
Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
2016-03-11 01:52:26 UTC+0000 2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   floridadump.7z

$DATA

$OBJECT_ID
Object ID: 40000000-0000-0000-0050-110500000000
Birth Volume ID: 00000000-0000-0000-0000-000000000000
Birth Object ID: 2215512d-0a00-ffff-ffff-ffff82794711
Birth Domain ID: 5b0f8000-0000-0000-160f-800000000000

***************************************************************************
***************************************************************************
MFT entry found at offset 0x40092c00
Attribute: In Use & File
Record Number: 35
Link count: 2

$STANDARD_INFORMATION
Creation                       Modified                       MFT Altered                    Access Date                    Type
------------------------------ ------------------------------ ------------------------------ ------------------------------ ----
2016-03-11 01:52:26 UTC+0000 2016-03-11 01:29:41 UTC+0000   2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   Archive

$FILE_NAME
Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
2016-03-11 01:52:26 UTC+0000 2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   FLORID~1.7Z

$FILE_NAME
Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
2016-03-11 01:52:26 UTC+0000 2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   2016-03-11 01:52:26 UTC+0000   floridadump.7z

$DATA

$OBJECT_ID
Object ID: 40000000-0000-0000-0050-110500000000
Birth Volume ID: db401105-0000-0000-db40-110500000000
Birth Object ID: 2215512d-0a00-ffff-ffff-ffff82794711
Birth Domain ID: 00000000-0000-0000-0000-000000000000

***************************************************************************
***************************************************************************
```

So, we probably should extract this archive. I carved it out using foremost.

Trying to extract the archive prompts us for a password:
```
[fagrant@ctf ~]$ 7z e 00021944.7z

7-Zip [64] 9.38 beta  Copyright (c) 1999-2014 Igor Pavlov  2015-01-03
p7zip Version 9.38.1 (locale=C,Utf16=off,HugeFiles=on,1 CPU,ASM)

Processing archive: 00021944.7z

Enter password (will not be echoed) :

Error: Can not open encrypted archive. Wrong password?

Can't open as archive: 1
Files: 0
Size:       0
Compressed: 0
```

We also notice some text files named 001.txt, ..., 007.txt:
```
***************************************************************************
MFT entry found at offset 0x40093400
Attribute: In Use & File
Record Number: 37
Link count: 1


$STANDARD_INFORMATION
Creation                       Modified                       MFT Altered                    Access Date                    Type
------------------------------ ------------------------------ ------------------------------ ------------------------------ ----
2016-03-11 01:52:38 UTC+0000 2016-03-11 01:16:22 UTC+0000   2016-03-11 01:52:38 UTC+0000   2016-03-11 01:52:38 UTC+0000   Archive

$FILE_NAME
Creation                       Modified                       MFT Altered                    Access Date                    Name/Path
------------------------------ ------------------------------ ------------------------------ ------------------------------ ---------
2016-03-11 01:52:38 UTC+0000 2016-03-11 01:52:38 UTC+0000   2016-03-11 01:52:38 UTC+0000   2016-03-11 01:52:38 UTC+0000   007.txt

$DATA


$OBJECT_ID
Object ID: 40000000-0000-0000-00a0-020000000000
Birth Volume ID: 99960200-0000-0000-9996-020000000000
Birth Object ID: 312af3f6-0300-ffff-8000-000058000000
Birth Domain ID: 000f1800-0000-0300-1a00-000038000000

***************************************************************************

```

```perl
use strict;
use warnings;

open(F, '<', 'whereisfloridaman');
seek(F, 0x40093400, 0);
my $i = 0;
while($i < 500) {
    my $line;
    read(F, $line, 1000);
    print $line;
    $i++;
}
close(F);
```

Looking through the output I find the following interesting MFT entry:
```
00000c00: 4649 4c45 3000 0300 d01c 8000 0000 0000 0100 0100 3800 0100 0002 0000 0004 0000  FILE0...............8...........
00000c20: 0000 0000 0000 0000 0500 0000 2800 0000 0700 4711 0000 0000 1000 0000 6000 0000  ............(.....G.........`...
00000c40: 0000 0000 0000 0000 4800 0000 1800 0000 3e74 edb0 387b d101 2fa9 61bb 357b d101  ........H.......>t..8{../.a.5{..
00000c60: 5f98 f4b0 387b d101 3e74 edb0 387b d101 2000 0000 0000 0000 0000 0000 0000 0000  _...8{..>t..8{.. ...............
00000c80: 0000 0000 0501 0000 0000 0000 0000 0000 0000 0000 0000 0000 3000 0000 6800 0000  ........................0...h...
00000ca0: 0000 0000 0000 0200 5000 0000 1800 0100 0500 0000 0000 0500 3e74 edb0 387b d101  ........P...............>t..8{..
00000cc0: 3e74 edb0 387b d101 3e74 edb0 387b d101 3e74 edb0 387b d101 0000 0100 0000 0000  >t..8{..>t..8{..>t..8{..........
00000ce0: 0000 0000 0000 0000 2000 0000 0000 0000 0703 3000 3000 3300 2e00 7400 7800 7400  ........ .........0.0.3...t.x.t.
00000d00: 8000 0000 4800 0000 0100 0000 0000 0100 0000 0000 0000 0000 0f00 0000 0000 0000  ....H...........................
00000d20: 4000 0000 0000 0000 0000 0100 0000 0000 05f2 0000 0000 0000 05f2 0000 0000 0000  @...............................
00000d40: 3110 c2f7 0300 ffff 8000 0000 5800 0000 0008 1800 0000 0300 2d00 0000 2800 0000  1...........X...........-...(...
00000d60: 6300 6e00 6600 6600 6a00 6200 6500 7100 224e 325a 4457 5734 3758 4b59 3858 3654  c.n.f.f.j.b.e.q."N2ZDWW47XKY8X6T
00000d80: 4c55 5450 5236 5134 4437 3652 4855 3745 4e56 4350 4138 4356 4b22 200d 0a00 0000  LUTPR6Q4D76RHU7ENVCPA8CVK" .....
00000da0: 8000 0000 5800 0000 000f 1800 0000 0400 1a00 0000 3800 0000 5a00 6f00 6e00 6500  ....X...............8...Z.o.n.e.
00000dc0: 2e00 4900 6400 6500 6e00 7400 6900 6600 6900 6500 7200 0000 5b5a 6f6e 6554 7261  ..I.d.e.n.t.i.f.i.e.r...[ZoneTra
00000de0: 6e73 6665 725d 0d0a 5a6f 6e65 4964 3d33 0d0a 0000 0000 0000 ffff ffff 8279 0700  nsfer]..ZoneId=3.............y..
```

Note that I knew that small files have their contents in the MFT, which gave me some interest in the MFT entries. 

Trying the string N2ZDWW47XKY8X6TLUTPR6Q4D76RHU7ENVCPA8CVK" for the 7z password worked. We now have the file `floridadump`.
```
[fagrant@ctf ~]$ ls -alh floridadump 
-r--r--r-- 1 fagrant admin 512M Mar  6 04:05 floridadump
[fagrant@ctf ~]$ file floridadump 
floridadump: data
[fagrant@ctf ~]$ xxd -c32 floridadump | head
00000000: 454d 694c 0100 0000 0010 0000 0000 0000 fffb 0900 0000 0000 0000 0000 0000 0000  EMiL............................
00000020: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000  ................................
00000040: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000  ................................
00000060: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000  ................................
00000080: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000  ................................
000000a0: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000  ................................
000000c0: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000  ................................
000000e0: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000  ................................
00000100: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000  ................................
00000120: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000  ................................
```

Looking online for the magic bytes EMiL, I found the following: https://github.com/504ensicsLabs/LiME

But it appeared to not really be relevant to this case. The only thing we need to know is that we're dealing with a memdump.

Looking for interesting strings, I searched for 'florida' and found strings related to a user 'floridaman'. Dumping all "shell commands" with a dump regex:
```
[fagrant@ctf ~]$ strings -n10 floridadump | grep 'floridaman@' | sort | uniq       
[Kfloridaman@floridaman: ~/LiME/src
]0;floridaman@floridaman: /usr/share
]0;floridaman@floridaman: ~
]0;floridaman@floridaman: ~/LiME
]0;floridaman@floridaman: ~/LiME/src
floridaman@floridaman: ~
floridaman@floridaman: ~/LiME
floridaman@floridaman: ~/LiME/src
floridaman@floridaman:/$ cd usr
floridaman@floridaman:/usr/share$ ls
floridaman@floridaman:~$ 
floridaman@floridaman:~$ cd LiME
floridaman@floridaman:~$ ls
floridaman@floridaman:~$ ls -al
floridaman@floridaman:~$ nano .bash_history
floridaman@floridaman:~$ t.rvm.io | bash -s stable --ruby
floridaman@floridaman:~/LiME$ cd src
floridaman@floridaman:~/LiME$ ls
floridaman@floridaman:~/LiME/src$ 
floridaman@floridaman:~/LiME/src$   
floridaman@floridaman:~/LiME/src$ .order    tcp.c
floridaman@floridaman:~/LiME/src$ l
floridaman@floridaman:~/LiME/src$ ls
floridaman@floridaman:~/LiME/src$ s.order    tcp.ce.symvers  tcp.o
floridaman@floridaman:~/LiME/src$ sudo insmod ./lime-3.19.0-25-gena
floridaman@floridaman:~/LiME/src$ sudo insmod ./lime-3.19.0-25-generic.ko "path=/home/floridaman/floridadump.lime format=lime
floridaman@floridaman:~/LiME/src$ sudo insmod ./lime-3.19.0-25-generic.ko "path=/home/floridaman/floridadump.lime format=lime"
```

Looking for sudo commands doesn't seem like a bad idea either:
```
[fagrant@ctf ~]$ strings -n10 floridadump | grep -E '.+sudo ' | sort | uniq
    ${SUDO_USER:+sudo }${rvm_gpg_command##*/} --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
    command curl -sSL https://rvm.io/mpapis.asc | ${SUDO_USER:+sudo }${rvm_gpg_command##*/} --import -
 package using apt-get.  This feature requires apt and sudo to work.
# Allow members of group sudo to execute any command
# Finally, please note that using the visudo command is the recommended way
# See the man page for visudo for more information.
# This will cause sudo to read and parse any files in the /etc/sudoers.d 
%s is not allowed to run sudo on %s.  This incident will be reported.
Allow sudo to prompt for a password even if it would be visible
Always send mail when sudo is run
File containing the sudo lecture: %s
If sudo is invoked with no arguments, start a shell
Only allow the user to run sudo if they have a tty
Please run ibus-daemon with login user! Do not run ibus-daemon with sudo or su.
Sorry, user %s may not run sudo on %s.
Use `sudo ./%s' if this is the `%s' you wish to run.
User %s is not allowed to run sudo on %s.
Visudo will honor the EDITOR environment variable
[11;1Hsudo pip install peewee
[12dsudo useradd -p $(openssl passwd -1 $THING) floridawoman
[16dsudo apt-get update
[17dsudo rm -rf /var/lib/apt/lists/*
[18dsudo apt-get install htop
[18dsudo apt-get update
command_to_run=(__rvm_sudo -p "%p password required for '$*': " "${command_to_run[@]}")
effective uid is not %d, is sudo installed setuid root?
floridaman@floridaman:~/LiME/src$ sudo insmod ./lime-3.19.0-25-gena
floridaman@floridaman:~/LiME/src$ sudo insmod ./lime-3.19.0-25-generic.ko "path=/home/floridaman/floridadump.lime format=lime
floridaman@floridaman:~/LiME/src$ sudo insmod ./lime-3.19.0-25-generic.ko "path=/home/floridaman/floridadump.lime format=lime"
```

Between the commands we see an openssl command with an environment variable:
```
[fagrant@ctf ~]$ strings -n10 floridadump | grep -E 'THING' | sort | uniq
!g_type_info_is_pointer (type_info) || transfer == GI_TRANSFER_NOTHING
(%lu) NOTHING
(?) NOTHING
-   5   5   1396975204  A   -   -   gz  How to write mib2c.conf files to do ANYTHING based on MIB input.
EVERYTHING
[11;1Hexport THING="c3Vue0YhTjRMTFlfQzRVR0hUX0ZMMFIhRDRNNE59"
[12dsudo useradd -p $(openssl passwd -1 $THING) floridawoman
arg_cache->transfer == GI_TRANSFER_NOTHING
export THING="c3Vue0YhTjRMTFlfQzRVR0hUX0ZMMFIhRDRNNE59"
g_type_is_a (g_type, G_TYPE_VARIANT) || !is_pointer || transfer == GI_TRANSFER_NOTHING
sudo useradd -p $(openssl passwd -1 $THING) floridawoman
transfer == GI_TRANSFER_NOTHING
```

Base64 decode of the contents:
```
[fagrant@ctf ~]$ echo "c3Vue0YhTjRMTFlfQzRVR0hUX0ZMMFIhRDRNNE59" | base64 --decode
sun{F!N4LLY_C4UGHT_FL0R!D4M4N}
```


## Other write-ups and resources
* <https://ctftime.org/writeup/2834>
