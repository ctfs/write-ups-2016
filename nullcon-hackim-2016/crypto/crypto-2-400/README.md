# nullcon HackIM : Crypto Question 2

**Category:** Crypto
**Points:** 400
**Solves:** 
**Description:**

> Some one was here, some one had breached the security and had infiltrated here. All the evidences are touched, Logs are altered, records are modified with key as a text from book.The Operation was as smooth as CAESAR had Conquested Gaul. After analysing the evidence we have some extracts of texts in a file. We need the title of the book back, but unfortunately we only have a portion of it...
> 
> 
> [The_extract.txt](./The_extract.txt)


## Write-up

After reading the description it was pretty clear this was a Caesar cipher. Upon throwing 'The_extract.txt' into [Xarg's Caesar decrypter](http://www.xarg.org/tools/caesar-cipher/) we can recover what seems like an [excerpt from a book](./The_text.txt)(which would match the problem description). 

Afterwards we can throw the first sentence of the plaintext into Google Books, where we are met with multiple books, but the first result 'In the Shadow of Greed' is the correct flag!

## Other write-ups and resources

* none yet
