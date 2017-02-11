# NCL 2016 Preseason : Squid-Proxy-Log-Analysis-300

__Category__: Log Analysis

__Points__: 300

## Write-up

<a href="https://jhalon.github.io/images/ncl10.png"><img src="https://jhalon.github.io/images/ncl10.png"></a>

For this challenge we are provided the following file: [NCL-2017-Pre-squid_access.log](https://jhalon.github.io/download/NCL-2017-Pre-squid_access.log)

--

__In what year was this log saved?__

With this question, let's start by looking at the first line of the access log.

```
1286536308.779    180 192.168.0.224 TCP_MISS/200 411 GET http://liveupdate.symantecliveupdate.com/minitri.flg - DIRECT/125.23.216.203 text/plain
```

We can see that the first few numbers represent the time. Since Squid is a Linux Proxy, this time is in Epoch. So all I did was go online to [EpochConverter](http://www.epochconverter.com/) and converted the time. You should get something similar to what I have below.

<a href="https://jhalon.github.io/images/squid1.png"><img src="https://jhalon.github.io/images/squid1.png"></a>

__Answer: 2010__

--

 __How many milliseconds did the fastest request take?__

Just eyeing the log we can see that at the end, on line 111 we have the fastest request.

```
1286536331.040      5 192.168.0.227 TCP_MISS/503 855 GET http://s2.youtube.com/s? - NONE/- text/html
```

__Answer: 5__

--

__How many milliseconds did the longest request take?__

Just eyeing the log we can see that at the end, on line 113 we have the longest request.

```
1286536351.746  41762 192.168.0.227 TCP_MISS/200 5340945 GET http://v15.lscache3.c.youtube.com/videoplayback? - DIRECT/122.160.120.150 video/x-flv
```

__Answer: 41762__

--

__How many different IP addresses used this proxy service?__

```console
root@kali:~# cat NCL-2017-Pre-squid_access.log | cut -d'T' -f 1 | egrep -o '([0-9]{1,3}\.){3}[0-9]{1,3}' | sort | uniq | wc -l
4
```

__Answer: 4__

--

__How many GET requests were made?__

```console
root@kali:~# cat NCL-2017-Pre-squid_access.log | grep "GET" | wc -l
35
```

__Answer: 35__

--

__How many POST requests were made?__

```console
root@kali:~# cat NCL-2017-Pre-squid_access.log | grep "POST" | wc -l
78
```

__Answer: 78__

--

__What company created the antivirus used on the host at 192.168.0.224?__

```console
root@kali:~# cat NCL-2017-Pre-squid_access.log | grep "192.168.0.224"
1286536308.779    180 192.168.0.224 TCP_MISS/200 411 GET http://liveupdate.symantecliveupdate.com/minitri.flg - DIRECT/125.23.216.203 text/plain
1286536308.910     37 192.168.0.224 TCP_MISS/200 4083 GET http://liveupdate.symantecliveupdate.com/streaming/norton$202009$20streaming$20virus$20definitions_1.0_symalllanguages_livetri.zip - DIRECT/125.23.216.203 application/zip
```

__Answer: symantec__

--

__What url is used to download an antivirus update?__

```console
root@kali:~# cat NCL-2017-Pre-squid_access.log | grep "192.168.0.224" | cut -d' ' -f 11
http://liveupdate.symantecliveupdate.com/streaming/norton$202009$20streaming$20virus$20definitions_1.0_symalllanguages_livetri.zip
```

__Answer: http://liveupdate.symantecliveupdate.com/streaming/...__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-log-analysis/
