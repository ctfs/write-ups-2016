# NCL 2016 : Cracking-Medium-120

__Category__: WiFi Cracking

__Points__: 120

## Write-up

<a href="https://jhalon.github.io/images/nclp-4.png"><img src="https://jhalon.github.io/images/nclp-4.png"></a>

For this challenge we are provided the following file: [NCL-2016-Game2-MediumWifi.pcap](https://jhalon.github.io/download/NCL-2016-Game2-MediumWifi.pcap)

--

__What is the SSID of the vulnerable WiFi Network?__

Once we open the pcap in Wireshark, all you really have to do is click on __Wireless__ in the tool bar, and from the drop down click __WLAN Traffic__.

<a href="https://jhalon.github.io/images/ncl-ch-2.png"><img src="https://jhalon.github.io/images/ncl-ch-2.png"></a>

Once we do so, we will get a pop up with the Wireless LAN Statistics. Just look at the first line under __SSID__ for the answer.

<a href="https://jhalon.github.io/images/ncl-cm-1.png"><img src="https://jhalon.github.io/images/ncl-cm-1.png"></a>

__Answer: NCL-Secure-Legacy__

--

__What is the BSSID of the vulnerable WiFi Network?__

Just as above, look at line 1, right under __BSSID__.

<a href="https://jhalon.github.io/images/ncl-cm-1.png"><img src="https://jhalon.github.io/images/ncl-cm-1.png"></a>

__Answer: c0:4a:00:80:76:e4__

--

__What is the MAC address of the connected client that had the most combined send/received packets?__

For this answer look down the __Beacons__ and __Data Pkts__ columns. We can see that __e0:55:3d:18:0c:a8__ sent/received the most packets combined.

<a href="https://jhalon.github.io/images/ncl-cm-1.png"><img src="https://jhalon.github.io/images/ncl-cm-1.png"></a>

__Answer: e0:55:3d:18:0c:a8__

--

__What is the password of the vulnerable WiFi Network?__

For this answer we will have to use [Aircrack-NG](https://www.aircrack-ng.org/) to be able to crack the WiFI Password. Just use the aircrack-ng command with the downloaded pcap, and it should crack the password for you!

```console
root@kali:~/Downloads# aircrack-ng NCL-2016-Game2-MediumWifi.pcap 
Opening NCL-2016-Game2-MediumWifi.pcap
Read 83449 packets.

   #  BSSID              ESSID                     Encryption

   1  C0:4A:00:80:76:E4  NCL-Secure-Legacy         WEP (14842 IVs)

Choosing first network as target.

Opening NCL-2016-Game2-MediumWifi.pcap
Attack will be restarted every 5000 captured ivs.
Starting PTW attack with 14842 ivs.

                                 Aircrack-ng 1.2 rc4


                 [00:00:01] Tested 3481 keys (got 14842 IVs)

   KB    depth   byte(vote)
    0    0/  1   6E(23040) 0D(19456) 06(18688) 1E(18432) 37(18432) 
    1    0/ 15   6F(20736) 68(20224) 3B(19968) 70(19968) 64(19712) 
    2    6/  8   AC(18944) 34(18432) 39(18432) 40(18176) 4A(18176) 
    3    0/  1   45(23552) 61(19968) 24(19200) D2(19200) 02(18944) 
    4   14/ 33   50(17920) AB(17664) B8(17664) C1(17664) F7(17664) 

                     KEY FOUND! [ 6E:6F:57:45:50 ] (ASCII: noWEP )
	Decrypted correctly: 100%

```

__Answer: noWEP__

--

## Other Write-ups and Resources

* [Jack Halon - KKB](https://jhalon.github.io/ncl-regular-season-2/)
