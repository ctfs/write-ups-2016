# National Cyber League Postseason 2016 : vsftpd

**Category:** log analysis  
**Points:** 95  
**Solves:**  
**Description:**  

> Inspect a vsftpd log from the city's public download server.
> * 15: How many unique IP addresses attempted to connect to the server?
> * 20: How many different IP addresses were able to log in successfully?
> * 15: How many file transfers were made successfully?
> * 20: What is the name of the file that failed to download the most?
> * 25: How many successful downloads were made for files that are 2 levels deep from the root (eg. /xxx/xxx/xxx.xxx)?

## Write-up

1.	How many unique IP addresses tried to connect?  
	A good regex to keep on hand is the one for finding IPs:
	
		$ grep "[1-9][0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" NCL-2016-Post-vsftpd.log
		...
		...
		Mon Nov 28 04:13:31 2016 [pid 30042] CONNECT: Client "193.42.151.220"
		Mon Nov 28 04:13:31 2016 [pid 30041] [myomonitor] OK LOGIN: Client "193.42.151.220"
		
	After running this command, we see that there seem to be two lines for each IP, and we see the statement CONNECT indicating the IP tried to connect. So we reshuffle our command:
	
		$ grep CONNECT NCL-2016-Post-vsftpd.log | grep "[1-9][0-9]*\.[0-9]*\.[0-9]*\.[0-9]*"
			# we see this gives us all the IPs, but with a lot of junk text, so try to -o flag:
		$ grep CONNECT NCL-2016-Post-vsftpd.log | grep -o "[1-9][0-9]*\.[0-9]*\.[0-9]*\.[0-9]*"
			# this gives us just the IPs ...
		$ grep CONNECT NCL-2016-Post-vsftpd.log | grep -o "[1-9][0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" | sort
			# sort can sort the IPs, so we now we remove duplicates ...
		$ grep CONNECT NCL-2016-Post-vsftpd.log | grep -o "[1-9][0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" | sort | uniq -c
			# this counts the number of occurrences of each IP (so the number of lines is # unique IPs):
		$ grep CONNECT NCL-2016-Post-vsftpd.log | grep -o "[1-9][0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" | sort | uniq -c | wc -l
		250		# final answer!
	
2.	How many different IP addresses successfully logged in?  
	Remember there was a line specifying `OK LOGIN`, so now we try:
	
		$ grep "OK LOGIN" NCL-2016-Post-vsftpd.log | grep -o "[1-9][0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" | sort | uniq -c | wc -l
		32
		
3.	How many file transfers were made successfully?  
	Looking more through some of the file, we find the phrase `OK DOWNLOAD`, so:
	
		$  grep "OK DOWNLOAD" NCL-2016-Post-vsftpd.log | wc -l
    	6755
		
4.	What is the name of the file that failed to download the most?  
	Taking a guess, we try `grep -i failed` but don't find any matches. Then we try `grep -i fail` and find a list of failed logins and failed downloads. With the regex `"FAIL DOWNLOAD"` we find a bunch of lines but how can we sort them?  
	One way to sort nicely to to use `grep -o` again to grab the name of the file. Each filepath starts with '/', so our regex turns into:
	
		$ grep "FAIL DOWNLOAD" NCL-2016-Post-vsftpd.log | grep -o "\/.*\""
			# '\/' escapes the first slash in the filepath
			# .* matches the rest of the filename
			# \" matches the quote at the end of the filename
			
	Since we need the name of the file that failed the most, we sort the output from `grep`, and then use [`uniq -c`](https://linux.die.net/man/1/uniq) to count the lines:  
	`$ grep -i "FAIL DOWNLOAD" NCL-2016-Post-vsftpd.log | grep -o "\/.*\""| sort | uniq -c`  
	And we can read from the output to see that `/Core/INSITU_BS_NRT_OBSERVATIONS_013_034/index_latest.txt` failed to download 4 times.
	
5.	How many successful downloads were made for files that are 2 levels deep from the root (e.g. /xxx/xxx/xxx.xxx)?  
	With this one we cheat a bit and resort to using python to help parse filenames:
	
		$ grep "OK DOWNLOAD" NCL-2016-Post-vsftpd.log | grep -o "\"\/.*\"" > oks.txt
			# gets only the filenames of all ok downloads, and saves them to the oks.txt file
		$ python
		>>> f = open("oks.txt")
		>>> files = [ line.strip() for line in f.readlines() ]
		>>> two_deep_files = 0
		>>> for file in files:
		...	if file.count('/') == 3:	# the files we're looking for have exactly 3 '/' in the full pathnames
		...		two_deep_files += 1
		...
		>>> i
		905		# final answer!

## Other write-ups and resources

(TODO)
