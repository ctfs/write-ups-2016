# angstromCTF 2016 : shakespeare-60

**Category:** Crypto
**Points:**
**Solves:**
**Description:**

> We have uncovered a Shakespearean-era transmission that seems perfectly ordinary. Can you help us find the hidden message in this Hamlet soliloquy?
> Hint: Who do some claim wrote the plays normally attributed to Shakespeare? The flag will be a lower-case string with no spaces.



## Write-up

We are given a single Word Document for this challenge. Upon opening it with Word 2016 we find the opening of the famous soliloquy from Shakespeare's Hamlet.

![Hamlet Text](https://github.com/jashanbhoora/write-ups-2016/blob/master/angstromctf-2016/crypto/shakespeare-60/shakespeare-1.jpg)

There's nothing obvious that stands out in the text, and there doesn't seem to be anything embedded in the document.
Following the hint, I searched for "Shakespeare conspiracies", and the third result gave me what I was looking for: [The Shakespeare Authorship Question](https://en.wikipedia.org/wiki/Shakespeare_authorship_question)

To quote the page: "The Shakespeare authorship question is the argument that someone other than William Shakespeare of Stratford-upon-Avon wrote the works attributed to him"..."The controversy has since spawned a vast body of literature, and more than 80 authorship candidates have been proposed, the most popular being Sir Francis Bacon; Edward de Vere, 17th Earl of Oxford; Christopher Marlowe; and William Stanley, 6th Earl of Derby."

Reading these names prompted me to start searching for encryption methods related to the supposed authors. Sir Francis Bacon was first, so I started off by searching for "Bacon encoding"...
And what do you know! It turns out Sir Bacon devised a form of steganography that is commonly called the [Baconian Cipher](https://en.wikipedia.org/wiki/Bacon%27s_cipher)!

The Wikipedia article does a pretty good job of explaining it, so I won't go into the details here. To summarise, Baconian Ciphers encode data in the presentation of the text, and not the text itself. After a bit of thought and experimentation, I realised that the body of text we had been given used two different (but visibly identical) fonts: Calibri Light (Headings) and Calibri (Body).

![Hamlet Text](https://github.com/jashanbhoora/write-ups-2016/blob/master/angstromctf-2016/crypto/shakespeare-60/shakespeare-2.jpg)

I used Word's "Select Text with Similar Formatting" tool to grab all of one of the fonts, then used Shift+F3 to make the selection all uppercase. I also removed any non-alphabetic from the string at this point, which left me with: tOBeoRNottOBeTHATiStHeQueSTIONWHetHErTISnOBlERINTHeMInDtOSuffERThESlINGSaNDaRRowSOFoUTRAGEoUSFoRtuNeORTOTAkeARMSaGAINStaSEAofTRoUBlESANDbYOPpOSInGEnDTHEM

This then needed to be converted to the A/B string that Baconian Ciphers use. I did this with a couple of lines of Python.

```python
intext = "tOBeoRNottOBeTHATiStHeQueSTIONWHetHErTISnOBlERINTHeMInDtOSuffERThESlINGSaNDaRRowSOFoUTRAGEoUSFoRtuNeORTOTAkeARMSaGAINStaSEAofTRoUBlESANDbYOPpOSInGEnDTHEM"
outtext = ""
for c in intext:
    if c.isupper():
            outtext += "B"
    else:
            outtext += "A"

print outtext
'ABBAABBAAABBABBBBABABABAABBBBBBBAABBABBBABBABBBBBBABBABABBAAABBBABBABBBBABBABBAABBBABBBBBBABBBABAABABBBBBBAABBBBABBBBBAABBBAABBABBABBBBBABBBABBBABBABBBBB'
```

Finally, I plugged the resulting string into an online [Baconian Cipher Decoder](http://www.geocachingtoolbox.com/index.php?page=baconianCipher) and fiddling around with the parameters I get this:
> theflagisastreetcarnameddeqire

I must have gotten something very slightly wrong somewhere down the line... Anyway, the flag is easy to work out from here.

Flag: *astreetcarnameddesire*

## Other write-ups and resources

* [Jashan Bhorra](https://github.com/jashanbhoora/write-ups-2016/tree/master/angstromctf-2016/crypto/shakespeare-60)
