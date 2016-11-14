# CSAW CTF 2016 Quals: Fuzyll

**Category:** Recon
**Points:** 200
**Solves:**
**Description:**

All files are lowercase with no spaces. Start here: http://fuzyll.com/files/csaw2016/start

## Write-up
* Step 0: Go to http://fuzyll.com/files/csaw2016/start as directed.
* Step 1: Go to http://fuzyll.com/files/csaw2016/deuteranomaly as directed.
* Step 2: After seeing my message in the alpha channel of the image, go to http://fuzyll.com/files/csaw2016/tomato as directed.
* Step 3: After decoding my EBCDIC message, go to http://fuzyll.com/files/csaw2016/elmrik as directed.
* Step 4: After decoding my base52 message, go to http://fuzyll.com/files/csaw2016/jade as directed.
* Step 5: After unzipping the file and finding my message in EXIF go to http://fuzyll.com/files/csaw2016/winaywayna as directed.
* Step 6: You win! Take the flag and submit it.

The code to decode part 4's message should do something like this:

```
def decode(input)
    i = 0
    output = 0
    input.split(//).reverse.each do |c|
        output += CHARS.index(c) * (52 ** i)
        i += 1
    end
    return output.to_s(16).scan(/../).map { |x| x.hex.chr }.join
end
```

## Flag
`flag{WH4T_4_L0NG_4ND_STR4NG3_TRIP_IT_H45_B33N}`

## Other write-ups and resources

* https://utdcsg.github.io/csaw-quals16/recon/fuzyll.html
* http://rotimiakinyele.com/csaw-ctf-quals-2016-writeups.jsp
* https://github.com/xPowerz/CTF-Writeups/tree/master/2016/CSAW/Fuzyll
* [Jhin Su](https://github.com/JhinSu/CSAW-2016-Write-Ups/tree/master/Recon/Fuzyll)
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-09-16-csaw/fuzyll)
