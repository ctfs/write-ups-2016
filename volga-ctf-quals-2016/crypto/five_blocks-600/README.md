#Volga CTF Quals 2016 five_blocks writeup

###*Category:* Crypto *Points:* 600

> The creators of the AI we're so desperately looking for used the remote server to encrypt their data. It seems that this service merely encrypts the data we're sending to it. We managed to find a possibly valuable piece of encrypted data along with the server's script. Could you take a look and see if anything can be done?
>
> nc five-blocks.2016.volgactf.ru 8888
>
> Hints
>
> What would you get if you'd encrypted four-block data of the form AABC, where A, B, C are 64-bit arbitrary blocks?
> 
> Are the rounds of the second block cipher completely dependent or independent of each other? Or is the truth somewhere in the middle?

[server.py](crypto/five_blocks-600/server.py)
[ciphers.py](crypto/five_blocks-600/ciphers.py)
[flag.enc](crypto/five_blocks-600/flag.enc)

## write-up

(TODO)

## Other write-ups and resources

(TODO)
