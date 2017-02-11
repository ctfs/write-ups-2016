# NCL 2016 Preseason : Network-Traffic-Analysis-FTP-160

__Category__: Network Traffic Analysis

__Points__: 160

## Write-up

<a href="https://jhalon.github.io/images/ncl11.png"><img src="https://jhalon.github.io/images/ncl11.png"></a>

For this challenge we are provided the following file: [NCL-2016-Pre-FTP.pcap](https://jhalon.github.io/download/NCL-2016-Pre-FTP.pcap)

--

__What was the first username/password combination attempt made to log in to the server? e.g. 'user/password'__

When we open up our pcap in Wireshark, the first thing we want to do is follow the __TCP stream__ of the first packet in the capture. Once we do, we are provided with the following stream information and the corresponding username/password.

<a href="https://jhalon.github.io/images/ncl-ftp1.png"><img src="https://jhalon.github.io/images/ncl-ftp1.png"></a>

__Answer: user1/cyberskyline__

--

__What software is the FTP server running? (Include name and version)__

Since we are already in the TCP stream view, we can see the first line is the server’s banner information, this provides us the server and it's version.

<a href="https://jhalon.github.io/images/ncl-ftp1.png"><img src="https://jhalon.github.io/images/ncl-ftp1.png"></a>

__Answer: FileZilla 0.9.53__

--

__What is the first username/password combination that allows for successful authentication?__

In our TCP stream view, we can go up to the next stream and we will be presented with another login attempt.

<a href="https://jhalon.github.io/images/ncl-ftp2.png"><img src="https://jhalon.github.io/images/ncl-ftp2.png"></a>

__Answer: user1/metropolis__

--

 __What is the first command the user executes on the ftp server?__

Looking at the stream, and understanding FTP commands we can rule out __PORT__ as a legit command, so we are left with __LIST__.

<a href="https://jhalon.github.io/images/ncl-ftp2.png"><img src="https://jhalon.github.io/images/ncl-ftp2.png"></a>

__Answer: LIST__

--

__What file is deleted from the ftp server"?__

The __DELE__ command is being used, which deletes a specified file on the server. That file is our answer.

<a href="https://jhalon.github.io/images/ncl-ftp2.png"><img src="https://jhalon.github.io/images/ncl-ftp2.png"></a>

__Answer: bank.cap__

---

__What file is uploaded to the ftp server?__

The __STOR__ command allows you to upload files to an FTP server. The file name after the command is our answer.

<a href="https://jhalon.github.io/images/ncl-ftp2.png"><img src="https://jhalon.github.io/images/ncl-ftp2.png"></a>

__Answer: compcodes.zip__

--

__What is the MD5 sum of the uploaded file?__

To do this we have to increment our TPC stream till we find the __FTP-DATA__ of the file being uploaded. We find the data in stream 6. To get the MD5 sum of the file, we have to change the __Show data as__ to __RAW__ as shown below. Once done, go ahead and save that file to the root directory. 

<a href="https://jhalon.github.io/images/ncl-ftp3.png"><img src="https://jhalon.github.io/images/ncl-ftp3.png"></a>

Once the file is saved, we will use the __md5sum__ command in Linux to give us the file's MD5 Hash.

```console
root@kali:~# ls
Desktop    download   hashcat  node-v0.4.4  Public     Videos
Documents  Downloads  Music    Pictures     Templates
root@kali:~# md5sum download
3303628e25d43be4e11cc8878c5c5878  download
```

__Answer: 3303628e25d43be4e11cc8878c5c5878__

--

__What file does the anonymous user download?__

Once again, back in the TPC stream, on stream 4 - we see that someone is logging in as anonymous. The file name that we need for our answer is used with the __RETR__ command.

<a href="https://jhalon.github.io/images/ncl-ftp4.png"><img src="https://jhalon.github.io/images/ncl-ftp4.png"></a>

__Answer: compcodes.zip__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-network-analysis1/
