# Sunshine CTF 2016 : Get gud kid

**Category:** Forensics
**Points:** 300
**Solves:** ?
**Description:**

> Description: http://ctf.bsidesorlando.org/static/uploads/213d461c72e1db462eb6e54c612f3fcf/moon.png
> 

## Write-up

We are presented with a file containing several (corrupt) ZIP files that contain JPEG images. Using file carving methods we can extract seven cat pictures but there's nothing in those pictures. During the CTF a hint was released that we have to look between the structs, so I started to dump the locations of the ZIP headers.

A nice overview and explanation of the different ZIP files can, of course, be found on [Wikipedia](https://en.wikipedia.org/wiki/Zip_%28file_format%29#Design). In short, we got a local file header before each file in the ZIP archive, we got the central directory header header containing a list of all files and behind it we got the end of central directory header.

```perl
use strict;
use warnings;

open(F, '<', 'get_gud_kid.dat');

my $magic_local_file = "\x50\x4b\x03\x04";
my $magic_central_dir = "\x50\x4b\x01\x02";
my $magic_end = "\x50\x4b\x05\x06";
my @window = (0, 0, 0, 0);
my $bytes_read = 0;

while(read(F, my $char, 1)) {
    shift @window; push @window, $char;
    if(("\xff" eq $window[1] && "\xd8" eq $window[2])) {
        print "JPG STARTS \@ $bytes_read...\n";
    }
    if(("\xff" eq $window[1] && "\xd9" eq $window[2])) {
        print "JPG ENDS \@ $bytes_read...\n";
    }

    if($magic_local_file eq join('', @window)) {
        print "Found local file header \@ $bytes_read...\n";
    } elsif($magic_central_dir eq join('', @window)) {
        print "Found central dir \@ $bytes_read...\n";
    } elsif($magic_end eq join('', @window)) {
        print "Found End of central dir \@ $bytes_read...\n";
    } elsif('flag' eq join('', @window)) {
        print "Found keyword: 'flag'\n";
    }

    $bytes_read++;
}

close(F);
```

```bash
$ perl get_gud.pl
Found local file header @ 182...
JPG STARTS @ 219...
JPG ENDS @ 368678...
Found central dir @ 368681...
Found End of central dir @ 368735...
Found local file header @ 368757...
Found local file header @ 368778...
JPG STARTS @ 368815...
JPG ENDS @ 779040...
Found central dir @ 779043...
Found End of central dir @ 779097...
Found keyword: 'flag'
Found local file header @ 779140...
JPG STARTS @ 779177...
JPG ENDS @ 928404...
Found central dir @ 928407...
Found End of central dir @ 928461...
Found local file header @ 928504...
JPG STARTS @ 928541...
JPG ENDS @ 1545705...
Found central dir @ 1545708...
Found End of central dir @ 1545762...
Found central dir @ 1545791...
Found local file header @ 1545805...
JPG STARTS @ 1545842...
JPG ENDS @ 1921240...
Found central dir @ 1921243...
Found End of central dir @ 1921297...
Found local file header @ 1921340...
JPG STARTS @ 1921377...
JPG ENDS @ 2282642...
Found central dir @ 2282645...
Found End of central dir @ 2282699...
Found keyword: 'flag'
Found local file header @ 2282742...
JPG STARTS @ 2282779...
JPG ENDS @ 2792046...
Found central dir @ 2792049...
Found End of central dir @ 2792103...
Found End of central dir @ 2792126...
```

Because of the hint, I dumped all bytes from the End of Central Directory header until the local file header as those bytes seemed most promising. (Notice the keyword "flag" appearing a few times between those two headers).

```perl
use strict;
use warnings;

open(F, '<', 'get_gud_kid.dat');

my $magic_local_file = "\x50\x4b\x03\x04";
my $magic_central_dir = "\x50\x4b\x01\x02";
my $magic_end = "\x50\x4b\x05\x06";
my @window = (0, 0, 0, 0);
my $bytes_read = 0;

my $between_eocd_lfh = 0;

while(read(F, my $char, 1)) {
        shift @window; push @window, $char;
        print $char if $between_eocd_lfh;

        if($magic_local_file eq join('', @window)) {
                $between_eocd_lfh = 0;
        } elsif($magic_end eq join('', @window)) {
                print join('', @window); # Also print the magic bytes
                $between_eocd_lfh = 1;
        }

        $bytes_read++;
}


close(F);
```

```
perl get_gud.pl | xxd
00000000: 504b 0506 0000 0000 0100 0100 3600 0000  PK..........6...
00000010: 739f 0500 0000 504b 0304 504b 0506 0000  s.....PK..PK....
00000020: 0000 0100 0100 3600 0000 9942 0600 0000  ......6....B....
00000030: 001d 0000 000b 0000 0066 6c61 6767 6564  .........flagged
00000040: 2e74 7874 6350 4b03 0450 4b05 0600 0000  .txtcPK..PK.....
00000050: 0001 0001 0036 0000 0013 4702 0000 0033  .....6....G....3
00000060: 5675 6532 6431 4d33 4e7a 5833 5666 5a7a  Vue2d1M3NzX3VfZz
00000070: 4230 5832 504b 0304 504b 0506 0000 0000  B0X2PK..PK......
00000080: 0100 0100 3600 0000 f46a 0900 0000 6431  ....6....j....d1
00000090: 5a48 303d 0a50 4b01 0214 0014 0000 0000  ZH0=.PK.........
000000a0: 002f 8750 4b03 0450 4b05 0600 0000 0001  ./.PK..PK.......
000000b0: 0001 0036 0000 008e ba05 0000 0066 48ee  ...6.........fH.
000000c0: c8ee f11d 0000 001d 0000 000b 0000 0000  ................
000000d0: 0000 504b 0304 504b 0506 0000 0000 0100  ..PK..PK........
000000e0: 0100 3600 0000 5983 0500 0000 0000 0000  ..6...Y.........
000000f0: 00b6 8100 0000 0066 6c61 6767 6564 2e74  .......flagged.t
00000100: 7850 4b03 0450 4b05 0600 0000 0001 0001  xPK..PK.........
00000110: 0036 0000 007b c507 0000 0074 504b 0506  .6...{.....tPK..
00000120: 504b 0506 0000 0000 0100 0100 3900 0000  PK..........9...
00000130: 4600 0000 0000                           F.....
```

We can see some strings resembling base64. Let's add the two big ones together: "3Vue2d1M3NzX3VfZzB0X2d1ZH0=". Decoding:
```
$ perl -MMIME::Base64 -le 'print decode_base64("3Vue2d1M3NzX3VfZzB0X2d1ZH0=")'
?[???L????W????Y
<TODl>
``` 

Let's try adding the 'G' just before the '3':
```
$ perl -MMIME::Base64 -le 'print decode_base64("G3Vue2d1M3NzX3VfZzB0X2d1ZH0=")'
n{gu3ss_u_g0t_gud}
```

So: sun{gu3ss_u_g0t_gud} (which is "c3Vue2d1M3NzX3VfZzd1ZH0=" in base64)

Note: For some reason, submitting the flag during the CTF failed but I'm pretty sure this is the answer.


## Other write-ups and resources

None.
