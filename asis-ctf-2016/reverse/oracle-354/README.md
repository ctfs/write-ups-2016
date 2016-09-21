# ASIS CTF Finals 2016 : oracle-354

**Category:** Reverse
**Points:** 354
**Solves:** 0
**Description:**

The resident oracle of our temple has risen his prices too high. If only we could understand his [inner workings](oracle.txz), we could get our answers for free.

Hint: [Burrows–Wheeler transform](https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform)

## Write-up

by [0xf4b](https://github.com/0xf4b)

The task has been solved after the end of the CTF.

The binary is a static 64-bits ELF.

```
$ file oracle
oracle: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 2.6.32, BuildID[sha1]=b986a272dac0f10f199e3114a358c03aef13f458, stripped
```

### main

The main function asks for the flag, and uses the last character as the number of rounds.

Here is the algorithm used:
```
for i in xrange(rounds):
	flag = burrows_wheeler_bits(flag)
	flag = xor(flag, 0x8f ^ i)
```

The Burrows-wheeler transform is not directly performed on the flag, but on its binary representation (string composed of "0" and "1" characters).

```
burrows_wheeler_bits("x}") == burrows_wheeler("111100001111101") == "100101111111100"
```

The final flag is hex-encoded and compared to:
```
8f02030966689a88a70e46d87260834943327b43956802b72ef9937f94e34c6bceac062454f1
```


### Inversion

The main problem is to invert the Burrows-wheeler transform without having a terminating character in the input string.

Inverting the matrix is a simple problem, however finding which row is the input is not possible without any knowledge on the input.

We know two conditions:
- the input for each round has its leading character set to "1" (because the transform strips leading 0's)
- the input for each round (except first) is a Burrows-Wheeler output from previous round, xored with the round-key (0x8f^round_index), so its trailing character should be "0" xored with the previous round key

These two conditions gives us 4 times less rows as candidates.

The remaing rows should each be tested as candidates of a Burrows-Wheeler output, until the inversion fails (yes, inversion can fail!).

A fail can be detected if all the rows of the matrix are not rotations of the first row.

All these conditions allow to perform a bruteforce, which retrieves the flag after ~2150s using pypy on a single core.

```
$ time pypy invert_oracle.py 8f02030966689a88a70e46d87260834943327b43956802b72ef9937f94e34c6bceac062454f1
FLAG ASIS{0b9323e43f1b0888e8bb7d270434113a}
pypy invert_oracle.py   2155,71s user 1,19s system 99% cpu 35:58,71 total
```

Script :
```
#!/usr/bin/python

import sys

fu = sys.argv[1].decode("hex")
xz = len(fu)

start = ord('}')-1

def rol(s,j):
    return s[j:] + s[:j]

def invert_burrows(my_input, i):

    xored = "".join(chr( ord(x) ^ 0x8f ^ i) for x in my_input)
    xored_int = int(xored.encode("hex"),16)
    xored_bin = bin(xored_int)[2:]

    str_len = len(xored_bin)

    ### Retrieve matrix
    final_col = [ x for x in xored_bin ]
    first_col = [ x for x in xored_bin ]
    first_col.sort()

    tmp_matrix = first_col[:]
    for j in xrange(1, str_len, 1):
        bigrams=[]
        for k in xrange(len(final_col)):
            bigrams.append(final_col[k]+tmp_matrix[k])
        bigrams.sort()
        tmp_matrix = bigrams[:]

    ### Check if matrix is ok
    matrix_ok = True

    #compute permutations of bigrams[0]
    perms=[]
    for k in xrange(len(bigrams)):
        rotation=rol(bigrams[0],k)
        perms.append(rotation)
    
    for k in bigrams:
        if k not in perms:
            matrix_ok = False
            break

    ### Recursive Burrows-Wheeler, or stop if last round
    if matrix_ok:
        if i == 0:
            # Last round
            if len(bigrams[0]) == (xz*8-1): # Leading bit should be 0 (printable char)
                for row in bigrams:
                    if row.startswith("1000001010100110100100101010011"): # ASIS
                        print "FLAG",hex(int(row,2))[2:-1].decode("hex")
                        sys.exit(0)
        else:
            # Go for previous round
            for k in bigrams:
                if k.startswith("1"): # Filter only leading "1"
                    if (k.endswith("0") and ( ((i-1)^0x8f) & 0x1) == 0) or (k.endswith("1") and ( ((i-1)^0x8f) & 0x1) == 1): # Filter only trailing "0"
                        
                        new_input = "%x" % int(k,2)
                        if len(new_input)%2 != 0:
                            new_input = "0"+new_input
                        new_input = new_input.decode("hex")
                    
                        invert_burrows(new_input,i-1)



invert_burrows(fu,start)

```

## Other write-ups and resources

* https://github.com/ctfs/write-ups-2016/tree/master/asis-ctf-2016/reverse/oracle-354
