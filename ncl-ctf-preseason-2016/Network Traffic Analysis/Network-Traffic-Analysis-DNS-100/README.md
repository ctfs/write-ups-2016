# NCL 2016 Preseason : Network-Traffic-Analysis-DNS-100

__Category__: Network Traffic Analysis

__Points__: 100

## Write-up

<a href="https://jhalon.github.io/images/ncl12.png"><img src="https://jhalon.github.io/images/ncl12.png"></a>

For this challenge we are provided the following file: [NCL-2016-Pre-DNS.cap](https://jhalon.github.io/download/NCL-2016-Pre-DNS.cap)

--

__What is the type of the DNS record requested?__

Simply type in __dns__ in the Wireshark filter to leave us only with the DNS packets. The first query will be our answer.

<a href="https://jhalon.github.io/images/ncl-dns1.png"><img src="https://jhalon.github.io/images/ncl-dns1.png"></a>

__Answer: AXFR__

--

__What domain was requested?__

Looking at the AXFR query we see the domain name as well.

<a href="https://jhalon.github.io/images/ncl-dns1.png"><img src="https://jhalon.github.io/images/ncl-dns1.png"></a>

__Answer: etas.com__

--

__How many items were in the response?__

Click on the 2nd dns packet which will be our response, and dig into the __Answers__ section.

<a href="https://jhalon.github.io/images/ncl-dns2.png"><img src="https://jhalon.github.io/images/ncl-dns2.png"></a>

__Answer: 4__

--

__What is the TTL for all of the records?__

Dig into one of the answers, and look for the __Time to live__.

<a href="https://jhalon.github.io/images/ncl-dns3.png"><img src="https://jhalon.github.io/images/ncl-dns3.png"></a>

__Answer: 3600__

--

__What is the IP address for the "welcome" subdomain?__

Looking back at the answers for __welcome.etas.com__ it gives us the IP address.

<a href="https://jhalon.github.io/images/ncl-dns3.png"><img src="https://jhalon.github.io/images/ncl-dns3.png"></a>

__Answer: 1.1.1.1__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-network-analysis1/
