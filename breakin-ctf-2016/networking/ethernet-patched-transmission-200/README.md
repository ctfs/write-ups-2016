# Break In 2016 - Ethernet Patched Transmission

**Category:** Networking
**Points:** 200
**Author:** networ-k-ing
**Solves:** 6
**Description:**

> Seems like someone intercepted and altered the frames. Can you patch it?
>     
>     >>Ingress>>
>     0x0000: 35 02 d2 d2 d2 d2 64 c4 14 74 02 94 08 00 45 00
>     0x0010: 00 3c a6 65 40 00 3e 06 75 a5 45 75 14 25 e3 02
>     0x0020: e4 14 dd c4 1f 90 00 00 00 00 00 00 00 00 a0 02
>     0x0030: 38 90 c7 d0 00 00 02 04 05 b4 04 02 08 0a e4 14
>     0x0040: 45 84 00 00 00 00 01 03 03 07
>     
>     >>Ingress>>
>     0x0000: 36 03 d3 d4 d5 d6 65 c1 13 72 02 94 08 00 45 00
>     0x0010: 00 3c a6 65 40 00 3e 06 07 29 31 43 19 43 21 44
>     0x0020: 23 64 dd c4 1f 90 00 00 00 00 00 00 00 00 a0 02
>     0x0030: 38 90 59 54 00 00 02 04 05 b4 04 02 08 0a e4 14
>     0x0040: 45 84 00 00 00 00 01 03 03 07
>     
>     >>Ingress>>
>     0x0000: a4 3b 45 cd 1d 76 56 22 75 15 02 41 08 00 45 00
>     0x0010: 00 3c a6 65 40 00 3e 06 54 e8 32 45 66 14 65 34
>     0x0020: 43 e1 dd c4 1f 90 00 00 00 00 00 00 00 00 a0 02
>     0x0030: 38 90 b0 ff 00 00 02 04 05 b4 04 02 08 0a e4 14
>     0x0040: 45 84 00 00 00 00 01 03 03 07
>     
>     <<Egress<<
>     0x0000:  ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 08 00 45 00
>     0x0010:  00 3c 00 00 40 00 3e 06 1c 0b ?? ?? ?? ?? ?? ??
>     0x0020:  ?? ?? 1f 90 dd c4 00 00 00 00 00 00 00 01 a0 ??
>     0x0030:  38 90 18 79 00 00 02 04 05 b4 04 02 08 0a 53 e3
>     0x0040:  8e e8 ?? ?? ?? ?? 01 03 03 07

## Write-up

In this question 4 packets were given initially out of which one 
packet had some hex bytes missing. So the first step should be to 
decode/analyse the given packets in a packet decoder/analyser like 
wireshark. After analyzing the packet in wireshark one can see that 
the given ingress (input) packets were tcp syn packets, so now by 
common sense the egress (output) packet, which had missing bytes, 
should be a syn/ack packet. Even if someone had doubts regarding 
the protocol of the egress packet, they could have always used 
the checksum to guess the reply flag and also there were many other 
hints to find the reply type.

So, now we can begin filling up the missing bytes in the egress packet. 
We already covered one of the missing byte.

    0x12 for syn/ack

Moving on to other missing bytes, we can see that the TSECR i.e. Timestamp Echo Reply 
field also had some missing bytes, so the next thing to fill up could be 
this section. Here we had to use the TSVAL field of the recieved syn packets, 
so this field gave us 4 more missing bytes:

    e4 14 45 84

since every ingress packet had same TSVAL value. Finally the only fields missing were source
and destination mac and ip addresses. Now this was the part where we have to use the src 
and dest mac and ip-addrs of the given packets one by one and then figure out the correct one by  
using the ip-checksum. If someone used the given order of packets, they would have gotten 
the correct answer after their first check itself i.e. the mac and ip-addrs of the first 
ingress packet were the correct combination for the reply.

So, the missing bytes were:

    64 c4 14 74 02 94 35 02 d2 d2 d2 d2 e3 02 e4 14 45 75 14 25 12 e4 14 45 84

And if someone observed carefully enough then they would have understood that the above bytes are reverse hex representation of ascii chars.
So we reverse every char:

    46 4c 41 47 20 49 53 20 2d 2d 2d 2d 3e 20 4e 41 54 57 41 52 21 4e 41 54 48  

which was:

    FLAG IS ----> NATWAR!NATH

Hence Flag is `NATWAR!NATH`

Packet syntax:

    [(00 07 0e 64 f9 3f) dest-mac-addr (d4 c9 ef 66 da f2) src-mac-addr (08 00) type-ip] ETH-2_LAYER 
    [45 00 00 (Type of Service-TOS) 3c (a6 65) identification 40 00 (40) TTL (06) protocol_tcp (4a 23) header-checksum (0a 01 21 c8) src-ipv4 (0a 04 14 67) dest-ipv4 ]IP_LAYER 
    [(ad 2c) src-port (1f 90) dest-port (ca 72 ea 9d) seq-no (00 00 00 00) ack-no a0 (02) tcp-flags (syn in this case) (72 10) window_size (bb 90) checksum (00 00) urgent-pointer (02 04 05 b4 04 02 08 (kind-timestamp) 0a (length-10) (01 66 4c f8) TSval (00 00 00 00) TSecr 01 03 03 07) options] TCP_LAYER

## Other write-ups and resources

* none yet
