# Pwn2Win CTF 2016: Bathing and Grooming

**Category:** Web
**Points:** 100|400
**Solves:** 1
**Description:**

> Our informant John has discovered that the access key for the murder request
> system changes on every new death carried by the Club. The key is the MD5 of
> the name of ALL the deads until now, in the order they were inserted in the
> database, and without including any separator between the names. Find the
> access key to allow our rebel group to shutdown the system. They use a
> "Bathing and Grooming" website as a cover: https://welovepets.pwn2win.party.
> The flag must be entered in the format CTF-BR{MD5-of-ALL-the-names}.
>
> Bonus (+300 points): For those who, once they discover the table which
> contains the names, are able to obtain the MD5 making a maximum of
> 15 HTTP requests to the website server. Show your complete resolution
> (including > sourcecode) to a judge in order to prove you needed
> 15 requests or less.


## Write-up

The website contains a SQL injection flaw in `/contact/procedure` that is fairly
easy to be found and exploited. The flaw is present in the "Pet's code" field,
which should normally receive a number, but its type can be easily changed
to "text" using the web browser's inspect element feature.

However, there are several limits in place which make it difficult to download the
entire list of names:

 * A mean rate of 3 HTTP requests per minute per IP address is allowed.
 * The form uses reCAPTCHA.
 * Output is truncated to max 32 chars.

By computing the MD5 server-side, we can get around these limits. However,
the server runs SQLite, which has no native MD5 function. Thus, we have to
implement MD5 ourselves in pure SQL.

The following are the main obstacles for achieving that:

 * SQLite is slow at handling big strings. BLOBs behave slightly better, but not
   all needed operations are available on them. Also, accessing a position appears
   not to be O(1) as you would expect. Therefore, we need to break the string in
   some chunks to speed up the calculation.

 * The `WITH RECURSIVE` statement allows to construct loops, but there seems to
   be no way to nest loops and retain acceptable performance. Therefore you need
   to code in state machine style in order to do everything in a single loop.

 * The `VALUES` construction allows to create "table literals" which could hold
   the constants required for computing MD5. However, it is slow to access these
   tables. There seems to be no way to inject a table containing a primary key
   or some kind of index. The solution is to use string literals as arrays.

The [md5.sql](md5.sql) file implements MD5 in pure SQL following these guidelines.
It receives the following parameters:

 * `:OFFSET` and `:LENGTH` of the chunk that is going to be processed.
 * `:A0`, `:B0`, `:C0` and `:D0` hold the MD5 algorithm state.

After processing all of the chunks, the last bytes of the string which don't fit
in a 64 byte block are retrieved, and the final step of MD5 can be implemented
in the attacker's machine.

The [md5_solve.py](md5_solve.py) script coordinates this calculation. It replaces the
correct parameters in [md5.sql](md5.sql) and copies it to the clipboard. The attacker
then pastes the resulting SQL in the web browser and manually solves the CAPTCHA.
After the result is shown in an alert box, the attacker copies it to clipboard.
The script monitors the clipboard, and immediately proceeds to mount the SQL injection
required for the next HTTP request.

Before running the script, install the pyperclip library, which is responsible
for clipboard handling:

```
sudo -H python -m pip install pyperclip
```

After all required HTTP requests are made, the script returns the flag
(MD5 of all names contained in the `procedures` table).


## Other write-ups and resources

* [Challenge source code](https://github.com/epicleet/bathing-and-grooming)
* [Dragon Sector](http://dragonsector.pl/docs/pwn2win2016_writeups.pdf)
