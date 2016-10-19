# tjctf-2016 : one-time-subtraction-20

**Category:** Cryptography
**Points:** 20
**Description:** I encrypted this flag with a one time subtraction, but my friend says it's not secure because my key is only one byte. Can you check if this is secure?

## Write-up

This challenge starts us off with this ciphertext:`241 231 224 241 227 248 173 235 176 220 223 246 241 176 220 174 240 220 235 173 241 220 176 235 173 242 228 229 250 135`. The description explicitly states the text is encrypted using a one time pad, which is simply using a list of shifts which are repeated if the length of the list is shorter than the plaintext message. All flags are in the format `tjctf{flag_goes_here}` so we can determine the shift between the ciphertext number `241` and what we know will be the ASCII character `t` which is represented by the decimal number `116`. Finding the difference between the two `241 - shift = 116` makes our shift `125`. Next we try the second number using the same method for the letter `j` when it appears to have the same shift: `125`. Shifting each number in the ciphertext down by `125` should reveal the flag: `tjctf{0n3_byt3_1s_n0t_3n0ugh}`.

## Other write-ups and resources

* [My Computer is a Potato - gitbooks.io](https://bobacadodl.gitbooks.io/tjctf-2016-writeups/content/one_time_subtraction_20_pts.html)
