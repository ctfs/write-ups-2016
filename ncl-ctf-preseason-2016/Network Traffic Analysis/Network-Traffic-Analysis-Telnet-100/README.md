# NCL 2016 Preseason : Network-Traffic-Analysis-Telnet-100

__Category__: Network Traffic Analysis

__Points__: 100

## Write-up

<a href="https://jhalon.github.io/images/ncl15.png"><img src="https://jhalon.github.io/images/ncl15.png"></a>

For this challenge we are provided the following file: [NCL-2016-Pre-Telnet.pcap](https://jhalon.github.io/download/NCL-2016-Pre-Telnet.pcap)

--

__What is the username that was used to successfully log in?__

First thing we need to do when we open up the pcap is to follow the TPC Stream. Once we do that, we are shown the Telnet stream. Keep in mind that Telnet will echo back each key (except for password) so try not to get confused.

To get our answer just look for "__login__".

<a href="https://jhalon.github.io/images/ncl-telnet-1.png"><img src="https://jhalon.github.io/images/ncl-telnet-1.png"></a>

__Answer: test__

--

__What is the password that was used to successfully log in?__

Since we already know that the password is not echoed back in telnet, just look for "__password__" and we will have our answer.

<a href="https://jhalon.github.io/images/ncl-telnet-1.png"><img src="https://jhalon.github.io/images/ncl-telnet-1.png"></a>

__Answer: capture__

--

__What command was executed once the user was authenticated?__

Looking at line 6, we can see that "__$__" is displayed - meaning that this is a command line entry, thus the user has authenticated successfully. This would be the first command execution.

<a href="https://jhalon.github.io/images/ncl-telnet-1.png"><img src="https://jhalon.github.io/images/ncl-telnet-1.png"></a>

__Answer: uname__

--

__In what year was this capture created?__

Just look at line 8, and look for what "__date__" uname returned.

<a href="https://jhalon.github.io/images/ncl-telnet-1.png"><img src="https://jhalon.github.io/images/ncl-telnet-1.png"></a>

__Answer: 2011__

--

__What is the hostname of the machine that was logged in to?__

Knowing how [uname](https://linux.die.net/man/2/uname) prints out the system information will help us decipher which one is the hostname. Uname displays the hostname as the second object.

<a href="https://jhalon.github.io/images/ncl-telnet-1.png"><img src="https://jhalon.github.io/images/ncl-telnet-1.png"></a>

__Answer: cm4116__

--

__What CPU architecture does the remote machine use?__</span>

Just as above, uname returns the machines hardware identifier second to last.

<a href="https://jhalon.github.io/images/ncl-telnet-1.png"><img src="https://jhalon.github.io/images/ncl-telnet-1.png"></a>

__Answer: armv4tl__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-network-analysis2/
