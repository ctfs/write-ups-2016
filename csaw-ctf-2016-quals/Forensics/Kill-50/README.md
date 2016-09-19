# CSAW CTF 2016 Quals: Kill

**Category:** Forensics
**Points:** 50
**Solves:**
**Description:**

Is kill can fix? Sign the autopsy file?

## Write-up

`kill.pcapng` is kill. The file signature should be corrected to `0A 0D 0D 0A`... The third file's FTP-DATA starting at packet 696 contains the flag in a jpg file.

### Flag

`flag{roses_r_blue_violets_r_r3d_mayb3_harambae_is_not_kill}`

## Other write-ups and resources

* https://github.com/krx/CTF-Writeups/tree/master/CSAW%2016%20Quals/for50%20-%20kill
* http://www.megabeets.net/csaw-2016-kill/
* https://github.com/73696e65/ctf-notes/blob/master/2016-ctf.csaw.io/forensics-50-kill.md
* https://bannsecurity.com/index.php/home/10-ctf-writeups/38-csaw-2016-kill
