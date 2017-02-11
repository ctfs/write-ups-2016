# NCL 2016 : Cracking-Hard-125

__Category__: WiFi Cracking

__Points__: 125

## Write-up

<a href="https://jhalon.github.io/images/nclp-5.png"><img src="https://jhalon.github.io/images/nclp-5.png"></a>

For this challenge we are provided the following file: [NCL-2016-Game2-HardWifi.cap](https://jhalon.github.io/download/NCL-2016-Game2-HardWifi.cap)

--

__What is the SSID of the vulnerable WiFi Network?__

Once we open the pcap in Wireshark, all you really have to do is click on __Wireless__ in the tool bar, and from the drop down click __WLAN Traffic__.

<a href="https://jhalon.github.io/images/ncl-ch-2.png"><img src="https://jhalon.github.io/images/ncl-ch-2.png"></a>

Once we do so, we will get a pop up with the Wireless LAN Statistics. Just look at the first line under __SSID__ for the answer.

<a href="https://jhalon.github.io/images/ncl-ch-1.png"><img src="https://jhalon.github.io/images/ncl-ch-1.png"></a>

__Answer: NCL-Secure__

--

__How many data packets were captured from the associated client?__

Just look down the __Data Pkts__ column, and we will see that __33:33:00:00:00:16__ has 15 packets. If you analyze the PCAP logs, you will see that the WiFi communicated directly with that client.

<a href="https://jhalon.github.io/images/ncl-ch-1.png"><img src="https://jhalon.github.io/images/ncl-ch-1.png"></a>

__Answer: 15__

--

__What is the password of the vulnerable WiFi Network?__

Just as we have done with the previous question, we will have to run aircrack-ng. But... aircrack-ng will not have the password by default! So we will have to use a wordlist! I simply used the __rockyou__ wordlist.

```console
root@kali:~/Downloads# aircrack-ng -w /root/rockyou.txt NCL-2016-Game2-HardWifi.cap 
Opening NCL-2016-Game2-HardWifi.cap
Read 167 packets.

   #  BSSID              ESSID                     Encryption

   1  C0:4A:00:80:76:E4  NCL-Secure                WPA (1 handshake)

Choosing first network as target.

Opening NCL-2016-Game2-HardWifi.cap
Reading packets, please wait...

                                 Aircrack-ng 1.2 rc4

      [00:00:05] 19972/9822768 keys tested (3487.18 k/s) 

      Time left: 46 minutes, 51 seconds                          0.20%

                           KEY FOUND! [ 1drummer ]


      Master Key     : 36 B2 B8 EB F1 B6 0C C0 70 0B D1 56 DC 2D 13 DF 
                       A4 D7 61 6D AC C8 6C 27 A4 3D F2 E6 AC D0 42 F0 

      Transient Key  : 62 68 62 6B FB AF 21 69 02 A1 B1 B3 D7 1E A6 41 
                       31 A5 AD 5F E8 A7 E9 F6 45 B1 31 16 E6 5A A5 B9 
                       51 45 94 E0 D2 DE 13 AC D4 6E 9E 72 35 82 29 C8 
                       76 BA 62 6D 69 A2 5B D7 88 C7 26 5F D7 F7 8F 4B 

      EAPOL HMAC     : C1 67 B9 73 EE EA E9 EE 1A B2 52 E7 02 58 7F BF 
```

__Answer: 1drummer__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-regular-season-2/
