# Break In 2016 - Find The Idiot

**Category:** Forensics
**Points:** 100
**Solves:** 90
**Description:**

> Your friend Bob, is an expert penetration tester. 
> He loves solving and creating puzzles. 
> He is invited by Pied Diaper Inc. for some testing. 
> You join him for this technical expedition.  At the site, you watch 
> him work for a few minutes, when he exclaims, "What an idiot!". Then,
> he looks at you with a with a playful gaze. 
> Then, handing out a flash drive to you he says, "Find the idiotic user".
>
> Link: [Here](find-the-idiot.zip)

# Write-up

This is a straight forward question. You are given a zip file containing the
entire filesystem dumps for the users. You have to run a dictionary attack on the
shadow file.

The attack reveals that user `gohan` has password `dragon1`. 

The flag is `dragon1`.

# Other write-ups and resources 

* none yet
