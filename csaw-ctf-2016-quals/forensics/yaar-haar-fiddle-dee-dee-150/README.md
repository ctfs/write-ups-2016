# CSAW CTF 2016 Quals: Yaar_Haar_Fiddle_Dee_Dee

**Category:** Forensics
**Points:** 150
**Solves:**
**Description:**

DO WHAT YE WANT 'CAUSE A PIRATE IS FREE. YOU ARE A PIRATE!

## Write-up

The challenge name, "YAAR HAAR FIDDLE DEE DEE" is a reference to a viral youtube video, as well as a hint. The description is just some of the lyrics of the viral song.
The challenge is a pcap of a "conversation" created with python sockets. There 3 base 64 encoded strings, one is just a blob of 100x100 grayscale images, one is an encrypted zip file, and one is an xml file which is formatted to opencv's haar cascade format. Players must seperate out the images, load the haar cascade file with opencv and run it against the images in the file, all of this, as well as the parameters required, are alluded to in the dialog that is also in the pcap. They will also need to draw a square over the object that the haar cascade detects, so that they can successfully identify it as a "skull and crossbones", which is then the password for the encrypted zip file (without spaces, as stated in the pcap), which contains flag.txt. the dialog also helpfully states that the map (the cascade file) points to the key (the skull and crossbones) for the booty (the zip file), and also says no spaces and no capitalized letters.

### Flag

flag{b31Ng_4_P1r4tE_1s_4lR1GHT_w1Th_M3}

### Condensed Solution

extract base64 strings, decode into 3 different files
binwalk -e the image blob
use opencv python docs to write a haar cascade script
identify the jollyroger and use that as the password for the zip
cat flag.txt

## Other write-ups and resources

* https://github.com/krx/CTF-Writeups/tree/master/CSAW%2016%20Quals/for150%20-%20Yaar%20Haar%20Fiddle%20Dee%20Dee
* http://rotimiakinyele.com/csaw-ctf-quals-2016-writeups.jsp
* http://kikisctf.blogspot.hr/2016/09/csaw-2016-quals-forensic-150-yaar-haar.html
