# MMA CTF 2nd 2016 : broken-ntfs-500

**Category:** Forensic
**Points:** 500
**Solves:** 3
**Description:**

> Someone broke my disk!!
> 
> I discovered this command from .bash_history.
> 
> 
> openssl aes-256-cbc -e -in /tmp/flag.jpg -out /mnt/flag:flag -pass file:<(openssl aes-256-cbc -e -in ./key -pass pass:`pwd`/key -nosalt)
> 
> Please recover flag from [problem.7z](https://twctf7qygt6ujk.azureedge.net/uploads/problem.7z-5c486dcd3b71cf9e7d91167837ba4cadd4f2bb8a75d34bc637d7495fa05165e6)
> 
> 
> Note: the ntfs.dd is mounted to /mnt.
> 
> 
> [2016/09/03 19:12 JST] The statement is fixed．(-pass pass:`pwd` -> -pass pass:`pwd`/key)
> 
> 
> Hints:
> 
> 
> 1. $MFT is broken
> 
> 2. You can determine only one key file used for encrypting.


## Write-up

(TODO)

## Other write-ups and resources

* none yet
