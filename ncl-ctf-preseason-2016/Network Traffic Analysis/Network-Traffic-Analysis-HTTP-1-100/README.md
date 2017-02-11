# NCL 2016 Preseason : Network-Traffic-Analysis-HTTP-1-100

__Category__: Network Traffic Analysis

__Points__: 100

## Write-up

<a href="https://jhalon.github.io/images/ncl13.png"><img src="https://jhalon.github.io/images/ncl13.png"></a>

For this challenge we are provided the following file: [NCL-2016-Pre-HTTP 1.cap](https://jhalon.github.io/download/NCL-2016-Pre-HTTP 1.cap)

--

__What Linux tool was used to execute a file download?__

As we have done before, follow the TCP stream of the first packet and you should see the __User-Agent__, which is what initiated the request. We see that the Linux tool __wget__ was used.

<a href="https://jhalon.github.io/images/ncl-http1-1.png"><img src="https://jhalon.github.io/images/ncl-http1-1.png"></a>

__Answer: wget__

--

__What is the name of the web server software that handled the request?__

Just look for the __Server__ line for the answer.

<a href="https://jhalon.github.io/images/ncl-http1-1.png"><img src="https://jhalon.github.io/images/ncl-http1-1.png"></a>

__Answer: Nginx__

--

__From what IP address did the request originate?__

Going back to our packets, let's find the __GET__ command and look at __Source__.

<a href="https://jhalon.github.io/images/ncl-http1-3.png"><img src="https://jhalon.github.io/images/ncl-http1-3.png"></a>

__Answer: 192.168.1.140__

--

__What is the IP address of the server?__

Same packet, just look at __Destination__.

<a href="https://jhalon.github.io/images/ncl-http1-3.png"><img src="https://jhalon.github.io/images/ncl-http1-3.png"></a>

__Answer: 174.143.213.184__

--

__What is the md5sum of the file downloaded?__

For this one, we have to go to __File__ > __Export Objects__ > __HTTP__ and you will see a pop up like below.

<a href="https://jhalon.github.io/images/ncl-http1-2.png"><img src="https://jhalon.github.io/images/ncl-http1-2.png"></a>

Go ahead and save that image to the root directory. Then we can run the __md5sum__ command in our CLI against the image - this will return the images MD5 Hash.

```console
root@kali:~# ls
Desktop    download   hashcat   Music        Pictures  Templates
Documents  Downloads  logo.png  node-v0.4.4  Public    Videos
root@kali:~# md5sum logo.png 
966007c476e0c200fba8b28b250a6379  logo.png
```

__Answer: 966007c476e0c200fba8b28b250a6379__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-network-analysis1/
