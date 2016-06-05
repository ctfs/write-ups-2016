# tjctf-2016 : super-questionable-luggage-service-30

**Category:** Web**Points:** 30
**Description:** I was using this great luggage storing service, but I accidentally stored my flag with them. Fortunately, my flag went in the wrong way, so it shouldn't be difficult for you to find. Right? [super-questionable-luggage.p.tjctf.org](http://super-questionable-luggage.p.tjctf.org)

## Write-up

This challenge takes some messing around, but if you monitor the data sent from the front end to the back end, you will soon realize they left a major hiccup in their security. All front end infrastructure and all data that hasn't reached the server can be altered. Normally web services will accept the exact text their user enters and sanitize (change to a safe format) characters used in SQL injections such as ';# on the server side. However, this service sanitizes the input, then sends it to the back end where it is immediately executed in an SQL statement. Since we can edit data after the form sends it and before the server receives it, we can put back in the infamous SQL injection using BurpSuite through Kali Linux, or through a simple POST request client. If you have change the data in the POST request to say `' OR 1=1;#` then the SQL server will execute that and return all the luggage entries in the database. While reading through the long list of luggage identifiers, you should see the following flag: `tjctf{th1s_m4d3_1t_e4s1er}`

## Other write-ups and resources

* [MilWestA - CTFtime.org](https://ctftime.org/writeup/3457)
