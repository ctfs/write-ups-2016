# NCL 2016 Preseason : Nginx-History-Analysis-260

__Category__: Log Analysis

__Points__: 260

## Write-up

<a href="https://jhalon.github.io/images/ncl9.png"><img src="https://jhalon.github.io/images/ncl9.png"></a>

For this challenge we are provided the following file: [NCL-2016-Pre-access.log](https://jhalon.github.io/download/NCL-2016-Pre-access.log)

All of my work done with this log involved the use of the Linux [CLI](https://en.wikipedia.org/wiki/Command-line_interface).

--

__How many different IP addresses reached the server?__

```console
root@kali:~# cat NCL-2016-Pre-access.log | cut -d' ' -f 1 | sort | uniq -c | wc -l
47
```

__Answer: 47__

--

__How many requests yielded a 200 HTTP status?__

```console
root@kali:~# cat NCL-2016-Pre-access.log | grep '" 200' | wc -l
19
```

__Answer: 19__

--

__How many requests yielded a 400 HTTP status?__

```console
root@kali:~# cat NCL-2016-Pre-access.log | grep '" 400' | wc -l
38
```

__Answer: 38__

--

__What IP address rang at the doorbell?__

```console
root@kali:~# cat NCL-2016-Pre-access.log | grep "bell" | cut -d' ' -f 1
186.64.69.141
```

__Answer: 186.64.69.141__

--

__What version of the Googlebot visited the website?__

```console
root@kali:~# cat NCL-2016-Pre-access.log | grep "Googlebot"
66.249.67.130 - - [01/Oct/2015:03:08:10 -0400] "GET /robots.txt HTTP/1.1" 502 166 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
---snip---
```

__Answer: 2.1__

--

__Which IP address attempted to exploit the shellshock vulnerability?__

```console
root@kali:~# cat NCL-2016-Pre-access.log | grep "/bin/bash" | cut -d' ' -f 1
61.161.130.241
```

__Answer: 61.161.130.241__

--

__What was the most popular version of Firefox used for browsing the website?__

```console
root@kali:~# cat NCL-2016-Pre-access.log | grep "Firefox" | cut -d' ' -f 18 | sort | uniq -c 
      4 en-US;
      9 Firefox/31.0"
      1 Gecko/20100101
      2 rv:30.N)
```

__Answer: 31__

--

__What is the most common HTTP method used?__

```console
root@kali:~# cat NCL-2016-Pre-access.log | cut -d' ' -f 6 | sort | uniq -c
      6 ""
     15 "CONNECT
     60 "GET
      1 "HEAD
      1 "POST
      1 "quit"
      4 "\x00"
      1 "\x04\x01\x00P\xC0c\xF660\x00"
      6 "\x04\x01\x00P\xC6\xCE\x0Eu0\x00"
      4 "\x05\x01\x00"
```

__Answer: GET__

--

__What is the second most common HTTP method used?__

```console
root@kali:~# cat NCL-2016-Pre-access.log | cut -d' ' -f 6 | sort | uniq -c
      6 ""
     15 "CONNECT
     60 "GET
      1 "HEAD
      1 "POST
      1 "quit"
      4 "\x00"
      1 "\x04\x01\x00P\xC0c\xF660\x00"
      6 "\x04\x01\x00P\xC6\xCE\x0Eu0\x00"
      4 "\x05\x01\x00"
```

__Answer: CONNECT__

--

__How many requests were for \x04\x01\x00P\xC6\xCE\x0Eu0\x00?__

```console
root@kali:~# cat NCL-2016-Pre-access.log | cut -d' ' -f 6 | sort | uniq -c
      6 ""
     15 "CONNECT
     60 "GET
      1 "HEAD
      1 "POST
      1 "quit"
      4 "\x00"
      1 "\x04\x01\x00P\xC0c\xF660\x00"
      6 "\x04\x01\x00P\xC6\xCE\x0Eu0\x00"
      4 "\x05\x01\x00"
```

__Answer: 6__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-log-analysis/
