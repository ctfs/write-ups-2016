# SECCON CTF Quals 2016 : vigenere-100

**Category:** Crypto
**Points:** 100
**Solves:** 777
**Description:**

    k: ????????????
    p: SECCON{???????????????????????????????????}
    c: LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ
    
    k=key, p=plain, c=cipher, md5(p)=f528a6ab914c1ecf856a1d93103948fe
    
     |ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
    -+----------------------------
    A|ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
    B|BCDEFGHIJKLMNOPQRSTUVWXYZ{}A
    C|CDEFGHIJKLMNOPQRSTUVWXYZ{}AB
    D|DEFGHIJKLMNOPQRSTUVWXYZ{}ABC
    E|EFGHIJKLMNOPQRSTUVWXYZ{}ABCD
    F|FGHIJKLMNOPQRSTUVWXYZ{}ABCDE
    G|GHIJKLMNOPQRSTUVWXYZ{}ABCDEF
    H|HIJKLMNOPQRSTUVWXYZ{}ABCDEFG
    I|IJKLMNOPQRSTUVWXYZ{}ABCDEFGH
    J|JKLMNOPQRSTUVWXYZ{}ABCDEFGHI
    K|KLMNOPQRSTUVWXYZ{}ABCDEFGHIJ
    L|LMNOPQRSTUVWXYZ{}ABCDEFGHIJK
    M|MNOPQRSTUVWXYZ{}ABCDEFGHIJKL
    N|NOPQRSTUVWXYZ{}ABCDEFGHIJKLM
    O|OPQRSTUVWXYZ{}ABCDEFGHIJKLMN
    P|PQRSTUVWXYZ{}ABCDEFGHIJKLMNO
    Q|QRSTUVWXYZ{}ABCDEFGHIJKLMNOP
    R|RSTUVWXYZ{}ABCDEFGHIJKLMNOPQ
    S|STUVWXYZ{}ABCDEFGHIJKLMNOPQR
    T|TUVWXYZ{}ABCDEFGHIJKLMNOPQRS
    U|UVWXYZ{}ABCDEFGHIJKLMNOPQRST
    V|VWXYZ{}ABCDEFGHIJKLMNOPQRSTU
    W|WXYZ{}ABCDEFGHIJKLMNOPQRSTUV
    X|XYZ{}ABCDEFGHIJKLMNOPQRSTUVW
    Y|YZ{}ABCDEFGHIJKLMNOPQRSTUVWX
    Z|Z{}ABCDEFGHIJKLMNOPQRSTUVWXY
    {|{}ABCDEFGHIJKLMNOPQRSTUVWXYZ
    }|}ABCDEFGHIJKLMNOPQRSTUVWXYZ{

Vigenere cipher
https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher

## Write-up

(TODO)

## Other write-ups and resources

* http://aukezwaan.nl/write-ups/seccon-2016-online-ctf-vigenere-100-points/
* https://github.com/p4-team/ctf/tree/master/2016-12-10-seccon-2016-quals/vigenere
* https://github.com/pogTeam/writeups/blob/master/2016/seccon/Vigenere/README.md
* https://nacayoshi00.wordpress.com/2016/12/12/seccon-2016-online-writeup/
* https://0xd13a.github.io/ctfs/seccon2016/vigenere
* https://ctftime.org/writeup/4982
* https://ctftime.org/writeup/4980
* https://github.com/Inndy/ctf-writeup/tree/master/2016-seccon/vigenere
* https://www.youtube.com/watch?v=OJ65pbaG84M
* https://j-kruse.de/2016/12/11/100-vigenere/
* https://github.com/pr0v3rbs/CTF/blob/master/2016/SECCON/Vigenere/decode.py
