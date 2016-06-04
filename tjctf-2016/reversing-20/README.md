# tjctf-2016 : reversing-20

**Category:** Binary**Points:** 20
**Description:** Reversing can be very easy

## Write-up

Reversing usually indicates the challenge involves reverse engineering a compiled file (commonly and ELF file). By opening the downloaded file in a basic text editor (notepad, vim, nano, leafpad, etc.) the header indicates it is an ELF file. Google will tell you ELF files are native to Linux (there are no legitimate ELF emulators for other operating systems). I booted Oracle VirtualBox (VMware works too) in Kali Linux and uploaded the ELF file (as reversing.elf). Then simply run `Strings reversing.elf`and it will print out the contents of the ELF file. Scroll through and eventually you will find this string in reverse: `tjctf{literally_reversing}`

## Other write-ups and resources

* [MilWestA - CTFtime.org](https://ctftime.org/writeup/3455)
