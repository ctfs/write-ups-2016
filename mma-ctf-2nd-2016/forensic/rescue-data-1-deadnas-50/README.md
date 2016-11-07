# MMA CTF 2nd 2016 : rescue-data-1-deadnas-50

**Category:** Forensic Warmup
**Points:** 50
**Solves:** 57
**Description:**

> Today, our 3-disk NAS has failed. Please recover flag.
>
> [[deadnas.7z](./deadnas.7z)]([deadnas.7z](./deadnas.7z))
>
>
> Hint 1: The NAS used RAID.
>
> Hint 2: [RAID-5](<https://en.wikipedia.org/wiki/RAID_5>#RAID_5)


## Write-up

In Tokyo Westerns CTF Rescue Data1:deadnas it is obvious from the description that this is a RAID recovery problem of some sort.  Given three files one of which just contains the words "crashed :-(".  Doing 'file' on the remaining disk0 file we get...

disk0: x86 boot sector, mkdosfs boot message display, code offset 0x3c, OEM-ID "mkfs.fat", sectors/cluster 4, root entries 512, sectors 2048 (volumes <=32 MB) , Media descriptor 0xf8, sectors/FAT 2, heads 64, serial number 0x867314a9, unlabeled, FAT (12 bit)

There are also chunks of apparently good data at intervals throughout the remaining disk0 and disk2 files.

In this three disk RAID each physical block contains either data or a XOR product of the other two blocks. Like this...

BLOCK        DISK0        DISK1        DISK2
    0              data            product      data
    1              data            data            product
    2              product       data           data
    3              data            product      data
    4              data            data           product

Knowing this I recovered disk1 using a file xor utility available here: https://github.com/scangeo

xor-files -r disk1 disk0 disk2

I knew this was correct when I found chunks of good data on the newly created disk1.

From here on, everything is done in bash with commonly available Linux helper commands.

Next I had to figure out the size of the disk blocks.  Looking at the disks with hexedit it seemed that good data occured in about 512b size chunks.  This was most apparent around 0x2800-0x3300 when comparing the three images side by side.  Using this I cut the three files into 512 byte size files with split:

mkdir disk0_split disk1_split disk2_split
split -b 512 -a 3 --additional-suffix 0 disk0 disk0_split/disk
split -b 512 -a 3 --additional-suffix 1 disk1 disk1_split/disk
split -b 512 -a 3 --additional-suffix 2 disk2 disk2_split/disk

Knowing that disk0/block0 is valid data there are only two ways the disk could go back together.  Looking back at the RAID structure block example above block0 can be either data, product, data or data, data, product.  Again the data around 0x2800 to 0x3300 helped me determine that the correct sequence for block 0 was data data product.  These three snippets copy just the data blocks into a directory and ignore the product blocks.

`mkdir wholedisk`
```
count=2
for file in `ls disk0_split`; do
  if [[ $((count%3)) -ne 1 ]]; then
    cp disk0_split/$file wholedisk
  fi
  ((count++))
done

count=0
for file in `ls disk1_split`; do
  if [[ $((count%3)) -ne 1 ]]; then
    cp disk1_split/$file wholedisk
  fi
  ((count++))
done

count=1
for file in `ls disk2_split`; do
  if [[ $((count%3)) -ne 1 ]]; then
    cp disk2_split/$file wholedisk
  fi
  ((count++))
done

# Finally restoring the original disk...

cd wholedisk
for file in `ls`; do
  cat $file >> ../wholedisk.img
done
```
Once I mounted the resulting image I was able to see the flag.jpg file containing the flag.

## Other write-ups and resources

* [RingZer0](https://github.com/tothi/ctfs/tree/master/mma-ctf-2016/deadnas)
* http://www.codilime.com/tw-mma-2-2016-deadnas/
* [Invulnerable (Russian)](http://countersite.org/articles/sysadmin/116-deadnas-writeup.html)
* http://megabeets.net/twctf-2016-web-rescue-data-1-deadnas/
