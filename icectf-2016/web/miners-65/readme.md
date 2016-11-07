# IceCTF-2016 : miners-65

**Category:** Web
**Points:** 65
**Description:**

The miners website has been working on adding a login portal so that all miners can get the flag, but they haven't made any accounts! However, your boss demands the flag now! Can you get in anyway? miners.vuln.icec.tf

## Writeup

The description of this challenge indicates the database is empty (no accounts). PHP won't return anything if the number of resulting rows is one, but if it gets anything back, it will show you the flag. The `UNION` keyword in SQL combines two `SELECT` statements  (e.g. `SELECT firstnames FROM users WHERE age=18 UNION SELECT firstnames FROM users WHERE age=64` which returns the firstnames of all users of of age 18 or 64. So, if the login can be tricked into returning a match for the username and password (0 results) and some numbers, it will print our flag. The query `SELECT * FROM users WHERE username='' UNION SELECT 1,2,3#` should work. Notice the `#` at the end denotes a comment, so nothing will be run after that (password doesn't matter). Therefore, submitting an username of `' UNION SELECT 1,2,3#` and any password should echo out `Your flag is: IceCTF{the_miners_union_is_a_strong_one}`.

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/IceCTF-65-Miners-Web/)
* http://hyp3rv3locity.com/content/icectf-2016-miners-web-65-pt
* https://www.youtube.com/watch?v=jHwwpDInSWk
