# NCL 2016 Preseason : Network-Traffic-Analysis-HTTP-2-180

__Category__: Network Traffic Analysis

__Points__: 180

## Write-up

<a href="https://jhalon.github.io/images/ncl14.png"><img src="https://jhalon.github.io/images/ncl14.png"></a>

For this challenge we are provided the following file: [NCL-2016-Pre-HTTP 2.pcap](https://jhalon.github.io/download/NCL-2016-Pre-HTTP 2.pcap)

--

__What was the compromised website that was used to infect users with malware?__

Looking through the streams, we come across __Referer__ in stream 4. This shows us that someone is requesting another webpage, looking at the __Referer__ URL will provide us the compromised website name.

<a href="https://jhalon.github.io/images/ncl-http2-1.png"><img src="https://jhalon.github.io/images/ncl-http2-1.png"></a>

__Answer: php.net__

--

__What version of the php was the website using?__

Let's go back to the first stream to see the HTTP Request for __php.net__, and that will provide us the info we need.

<a href="https://jhalon.github.io/images/ncl-http2-2.png"><img src="https://jhalon.github.io/images/ncl-http2-2.png"></a>

__Answer: 5.4.16__

--

__What version of Apache was the website using?__

Same as above, just look for __PHP__.

<a href="https://jhalon.github.io/images/ncl-http2-2.png"><img src="https://jhalon.github.io/images/ncl-http2-2.png"></a>

__Answer: 2.2.21__

--

__In what year was the capture made?__

We can use the current TCP stream and just look for __Date__.

<a href="https://jhalon.github.io/images/ncl-http2-2.png"><img src="https://jhalon.github.io/images/ncl-http2-2.png"></a>

__Answer: 2013__

--

__What domain servers up the malicious file?__

We can see that in stream 7 there is a GET request for a __.SWF__ file which is a Shockwave File, and possibly is malicious. (Question 7 basically gives it away...)

<a href="https://jhalon.github.io/images/ncl-http2-3.png"><img src="https://jhalon.github.io/images/ncl-http2-3.png"></a>

__Answer: zivvgmyrwy.3razbave.info__

--

__What is the IP address of the malicious domain?__

Just exit out of the TCP stream, and the first packet there should provide us the source IP.

<a href="https://jhalon.github.io/images/ncl-http2-5.png"><img src="https://jhalon.github.io/images/ncl-http2-5.png"></a>

__Answer: 192.168.40.10__

--

__At what packet number is the first request for a malicious .SWF made?__

Just as above, the packet where we got the IP also will be the packet # for the .SWF request.

<a href="https://jhalon.github.io/images/ncl-http2-5.png"><img src="https://jhalon.github.io/images/ncl-http2-5.png"></a>

__Answer: 173__

--

__What packet number requests the first successfully delivered payload?__

Working in IT Security, I know when a payload is successfully ran since you see "__This program cannot be run in DOS mode.__" in the packet captures... so if we go through the streams, we will see packet 213 is the first one to initiate the payload.

<a href="https://jhalon.github.io/images/ncl-http2-4.png"><img src="https://jhalon.github.io/images/ncl-http2-4.png"></a>

__Answer: 213__

--

## Other Write-ups and Resources

* [Jack Halon - KKB](https://jhalon.github.io/ncl-network-analysis1/)
