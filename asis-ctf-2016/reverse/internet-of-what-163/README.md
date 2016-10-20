# ASIS CTF Finals 2016 : internet-of-what-163

**Category:** Reverse
**Points:** 163
**Solves:** 4
**Description:**

We have found a weird module in our office that is being powered using a coin cell battery, and it seems to be trying to communicate with a server on the internet over WiFi network. [This file](Internet_Of_What.txz) is the firmware dump from the device. Can you access the server page in question?

## Write-up

by [0xf4b](https://github.com/0xf4b)

The task has been solved after the end of the CTF.

The binary has an unknown format.

Strings gives some hints:

```
Wait for WiFi... 
WiFi connected
IP address: 
connecting to 
138.68.152.88
Start Knocking
sequence step 1
sequence step 2
sequence step 3
sequence step 4
Sesame did not open!
Send this data
open sesame
...
/home/factoreal/.arduino15/packages/esp8266/hardware/esp8266/2.3.0/cores/esp8266/core_esp8266_main.cpp

```

Looks like port knocking on address 138.68.152.88. Also, the firmware seems design for ESP8266.

According to google, it uses an xtensa core. A processor module for IDA Pro is available on [github](https://github.com/themadinventor/ida-xtensa).

The firmware structure is also described in [this blogpost](http://developers-club.com/posts/255135/). It does not exactly match our file, but is sufficient to understand the structure.

## IDA Loader

We need a basic loader to analyze the firmware in IDA Pro:

```
#!/usr/bin/python

from struct import unpack_from
from idaapi import *

def accept_file(li, n):

        retval = 0
        if n == 0:
                li.seek(0)
                
                if li.read(4) == "e9010240".decode("hex"): # dirty but works
                        retval = "ESP8266 firmware"

        return retval

def load_file(li, neflags, format):

        li.seek(0)
        magic = li.read(4)
        v1, v2, v3 = unpack_from("<3L",li.read(12))

        print "Entry: %x" % v1
        print "Base: %x" % v2
        print "Size: %x" % v3

        li.file2base(16, v2, v2+v3, True)
        add_segm(0, v2, v2+v3, ".seg__1", "CODE")


        li.seek(0x1000, 0)
        

        magic = unpack_from("<4B",li.read(4))
        v1, = unpack_from("<L",li.read(4))
        segnum=2
        print "Entry: %x" % v1
        for k in xrange(magic[1]):
                v2, v3 = unpack_from("<2L",li.read(8))
    
                print "Base: %x" % v2
                print "Size: %x" % v3
                foffset = li.tell()
                li.file2base(foffset, v2, v2+v3, True)
                add_segm(0, v2, v2+v3, ".seg%3d"%segnum, "CODE")
                segnum += 1
                li.seek(foffset+v3,0)

        return 1

```

## Analysis

Once loaded in IDA Pro, we can find the function printing the "sequence step X" strings, and find a list of 4 values: 4025 10619 31337 22207.

Finally, a function call is performed with integer value 80 as argument, which should be the final port to connect to.

```
$ ./knock.sh 138.68.152.88 4025 10619 31337 22207; wget -O - 138.68.152.88
...
<h1>Flag:</h1>
<h1>ASIS{The_first_person_to_prove_that_cow_milk_is_drinkable_was_very_very_thirsty}</h1>
...
```

## Other write-ups and resources

* https://github.com/ctfs/write-ups-2016/tree/master/asis-ctf-2016/reverse/internet-of-what-163
