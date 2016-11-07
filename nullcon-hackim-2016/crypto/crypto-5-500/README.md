# nullcon HackIM : Crypto Question 5

**Category:** Crypto
**Points:** 500
**Solves:**
**Description:**

> Now you are one step away from knowing who is that WARRIOR. The Fighter who will decide the fate of war between the 2 countries. The Pride of One and Envey of the Other... You have got the secrete file which has the crucial information to identify the fighter. But the file is encrypted with a RSA-Private key. Good news you have its corresponding public key in a file. Bad news there are 49 other keys. Whos is the Fighter.
>
>
> [crypto5.zip](./crypto5.zip)


## Write-up

by [unicornasfuel](https://github.com/unicornsasfuel)

crypto5.zip contains two files: `warrior.txt` and `all_keys.txt`.

The keys are all RSA public keys, in ASCII-armored format. They are all the same keylength, and as such occupy the same number of lines in the file per key, making it easy to carve out each key. As there are only 50 keys, we can use an exhaustive search method to determine which is the correct key, attempting to decrypt the ciphertext with each one.

While we would normally apply a plaintext scoring system to programmatically determine which is the most likely candidate for successful decryption, there are so few keys that we can simply spit out all the candidate decryptions and then scroll through them until we see text.

Several challengers were confused about the statement that the message was encrypted with the private key, being under the impression that private keys cannot be used to encrypt under RSA. In reality, either key in a keypair can be used as the private or public component. Since the encryption and decryption operations do not differ except in the use of the other half of the keypair, we can use standard libraries to "encrypt" the data with each public key in order to decrypt it.

We can use Python and PyCrypto to solve the puzzle, like so:

~~~Python
from Crypto.PublicKey import RSA

ciphertext_fh = open('warrior.txt','r')
ciphertext = ciphertext_fh.read()
ciphertext_fh.close()

key_fh = open('all_keys.txt','r')
key = ''
for line_counter in range(9):
   key += key_fh.readline()

while key != '':
   cipher = RSA.importKey(key)
   print repr(cipher.encrypt(ciphertext, 'dummy')) # dummy second argument for compatibility
   key = ''
   for line_counter in range(9):
      key += key_fh.readline()
~~~

We search through the resulting outputs for the word "the", and find a properly padded decrypted message:

~~~
("\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00This fighter is a designation for two separate, heavily upgraded derivatives of the Su-35 'Flanker' jet plane. They are single-seaters designed by Sukhoi(KnAAPO).\n",)
~~~

Googling for this text results in a Wikipedia page on a fighter jet at https://en.wikipedia.org/wiki/Sukhoi_Su-35.

The flag is the name of the fighter jet: `Sukhoi Su-35`

## Other write-ups and resources

* <https://cryptsec.wordpress.com/2016/01/31/hackim-ctf-2016-write-up-crypto-question-5-500-points/>
* [P4 Team](https://github.com/p4-team/ctf/tree/master/2016-01-29-nullcon/crypto_5#eng-version)
* <http://h4ckx0re-ctf-crew.co.nf/2016/01/31/hackim-ctf-2016-crypto-5/>
* [Chinese](http://www.cnblogs.com/Christmas/p/5176600.html)
* [0x90r00t](https://0x90r00t.com/2016/02/03/hackim-2016crypto-500-crypto-question-5-write-up/)
