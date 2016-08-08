# OpenCTF : ultra_encryption

**Category:** Tasks
**Points:** 
**Solves:** 
**Description:**

> {'solve_count': 6, 'description': u"We've intrecepted these messages, but they look like they're encrypted. We need the plaintext.\n172.31.0.10/ultra_encryption_9045e45dca4945586028c6a74588d9ce.txt", 'total_scored': 600, 'challenge_name': u'ultra_encryption', 'point_value': 100, 'open': 1}

> file: [172.31.0.10/ultra_encryption_9045e45dca4945586028c6a74588d9ce.txt](ultra_encryption_9045e45dca4945586028c6a74588d9ce.txt)

## Write-up

### Shortcut Write-up

Exact same stuff as in my [Olympic CTF "Find da Key"](https://github.com/ctfs/write-ups-2014/tree/master/olympic-ctf-2014/find-da-key) task :-)

Let's for example run [the solving script](delimitry_solve.py) from Delimitry's write-up:

    root@kali:/mnt/hgfs/f# ./delimitry_solve.py 
    5uck_my_sh4rk_1m_4_tr0ll

Awesome! Flag: `5uck_my_sh4rk_1m_4_tr0ll`


### Long Explanation

Base64 encodes bitstream by arranging its bits in groups of 6. Each group of six bits has its own assigned char from `A..Z a..z 0..9 + /`  
So, if we encode `o_O` (`01101111 01011111 01001111`), it gets rearranged as `011011 110101 111101 001111`, and encoded as `b19P`

Sometimes the input bitstream can't be represented by whole number of 6-bit groups — that happens when input length isn't a multiple of 3. In those cases padding is added:

* Encoding `:D` (`00111010 01000100`), rearranged as `001110 100100 0100`, padded with zeros to `001110 100100 0100=00`, encoded as `OkQ=`
* Encoding `!` (`00100001`) → `001000 01` → `001000 01=0000` → `IQ==`

Note that the missing bits in input bitstream get padded by zeros. In case when `len(input) % 3 == 2`, two bits are added (and one `=` is appended to base64 output); in case of `len(input) % 3 == 1`, four zero bits are added. When decoding base64, those extra padding bits are just ignored: `un64("OkQ=") == un64("OkR=") == un64("OkS=") == un64("OkT=") == ":D"`. So they can be used to smuggle some covert bits: 2 bits for a `=`-padded base64 string, 4 bits for a `==`-padded one.

To encapsulate hidden bits in the base64ed string without manually implementing the bit work, we can shift the last char before `=` by several positions forward along the base64 alphabet.  
For example, if we want to encapsulate `0010` into `IQ==`, we shift Q by two positions → `IS==`

Similarly, if we want to extract the hidden bits without doing the bit stuff, we can decode and re-encode the base64 and look at how much the last char has been shifted:  
`b64(un64("IS==")) == "IQ=="    'S' - 'Q' == 2    2 == 0010`

In this task, every chunk has a `==` padding (four hidden bits). Extracting all of those and stacking them up into a single bitstream, we get the flag.

## Other write-ups and resources

* none yet
