# IceCTF-2016 : search-40

**Category:** Misc
**Points:** 40
**Description:**

There's something about this domain... search.icec.tf, I don't see anything but maybe its all about the conTEXT.

## Writeup

This challenge requires DNS lookup knowledge. DNS (Domain Name System) provides computers information about a specific domain. It is somewhat recognizable as a DNS record, as `TXT` is one of many DNS record types. Using `dig`, we can run `dig -t TXT search.icec.tf/` to search that domain for TXT records in the DNS. For the long output of the query, check out rawsec's write-up linked below, where you will see the flag is `IceCTF{flag5_all_0v3r_the_Plac3}`

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/IceCTF-2016-IceCTF-40-Search-Misc/)
* https://github.com/Idomin/CTF-Writeups/blob/master/IceCTF/Search-misc-40
* https://github.com/318BR/IceCTF/tree/master/2016/Stage2/Search
* https://mrpnkt.github.io/2016/icectf-2016-search/
* https://www.youtube.com/watch?v=gjUlI310_mA
* https://github.com/TeamContagion/CTF-Write-Ups/blob/master/icectf-2016/Misc/Search
* [Japanese](https://ctftime.org/writeup/3810)
