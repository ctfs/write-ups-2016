# tjctf-2016 : may-1-2600-100

**Category:** Forensics**Points:** 100
**Description:** Sometimes I miss that land of bliss.

## Write-up

After downloading and unzipping the file provided, it appears as a .DBX file. Googling 'dbx file' indicates the file at hand is a saved message from Microsoft Outlook. Download a free, simple DBX file viewer, then open the DBX file. Reading  the message, it refers to an attached file of a computer backup. Most free DBX viewers won't let you download the attachment easily, so you may have to find the raw attachment of the .BKF file in base 64 form. Then download a base64 to bkf file tool. Compile the base 64 attachment into the BKF file format. Google search for a BKF file viewer and download it. Then walk through the file system of the BKF file until you find the flag.doc file (there are two, only one has a flag) and find your way into the file, where you will find the following flag: `tjctf{@_b1@sT_Fr0M_tH3_Pa$t}`

## Other write-ups and resources

* [MilWestA - CTFtime.org](https://ctftime.org/writeup/3451)
* [SiBears - SiBears.ru](http://sibears.ru/labs/TJCTF-2016-May-1-2600/)
* [Invulnerable (Russian)](http://countersite.org/articles/sysadmin/99-outbox-forensics-tjctf-2016.html)
 * [My Computer is a Potato - gitbooks.io](https://bobacadodl.gitbooks.io/tjctf-2016-writeups/content/may_1st,_2060_100_pts.html)
