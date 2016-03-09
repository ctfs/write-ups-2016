# Cyber Security Challenge 2016: exFat is not Fat

**Category:** Digital Forensics  
**Points:** 90  
**Challenge designer:** Yves Vandermeer  
**Description:**  
> Recover deleted file \fccu\logo.jpg on the provided forensic copy and provide the md5 hash value.

>Hint: Use FAT chaining

## Write-up
-	All exFAT values are encoded using “little-endian”. You can use any hex editor to solve this challenge.
-	Analyse the forensic image and discover that it is one exFAT partition (TSK fsstat is helpful if wanting to avoid manual decoding) : Cluster size = 1024 bytes (2 sectors) FAT starts at sector 128 (962 sectors in total)
-	Search into the volume for the unallocated entry “logo.jpg” into FCCU folder. The entry starts at offset 125.424.288.
-	First byte of the entry “0x05” means “first 32 bytes set for an unallocated entry” (a used entry should start with “0x85).
-	Second bytes “0x02” indicate how many “32 bytes set” sub-entries are following to document this file
-	Next “32 bytes”, starting with “0x40” are describing the file allocation. This is what we need to recover file content. (should be starting with “0xC0” If still allocated).
-	Second byte “0x01” indicates that the “FAT” is used to keep the chaining. The file is probably fragmented. At offset 0x14 relative to this sub-entry, the Dword value points to the first cluster containing file data, and offset 0x18 Dword provides file length.
-	The work is now to follow the cluster chain using the FAT (every cluster is represented by a 4 bytes value, containing next chained clusters or, for the last one 0xFFFFFFFF.
-	Having list of clusters and file size, a combination of several “dd” commands deliver the file and allows to compute the hash value for the solution.

##Solution
41aeeec732ab724a53178620fddd6fbf

## Other write-ups and resources
- Mount on windows
- Use recuva
