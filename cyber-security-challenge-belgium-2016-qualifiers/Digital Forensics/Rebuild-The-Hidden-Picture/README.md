# Cyber Security Challenge 2016: Rebuild the hidden picture

**Category:** Digital Forensics  
**Points:** 30  
**Challenge designer:**  Yves Vandermeer  
**Description:**  
> Provide MD5 hash value for the JPEG picture file hidden by a suspect in [this file](this-file-challenge-source-files/FCCU_E.dd)
>
Note: Criminals are known to mess with their files to make your life harder, avoid the blocks that they tried to wipe.

> Hints: 
> - Use file type headers
> - Use file type trailers

## Write-up
- Use foremost to extract the image:  

`foremost -t jpeg,png FCCU_E.dd`

Once we open the image, we can see that it is not prefect. a simple xdd command shows “blocks” of zeroes. A deeper search show that “Zeroed” blocks are at sector 3000 (3000 sectors), and 9000 (3000 sectors).

It’s now time to extract only “good” sectors and avoid zeroed ones. Something like :

```
dd if=test.jpg count=3000 > result.jpg  
dd if=test.jpg count=3000 skip=6000 >> result.jpg
dd if=test.jpg count=3562 skip=12000 >> result.jpg
```
Computing md5 on result.jpg file gives the answer

##Solution
221fda8d1e083526038c6e1fa82d49f6

## Other write-ups and resources
