# DEFCON oCTF 2016 - the_wire

**Category:** Networking
**Points:** 400
**Author:** yotta
**Description:**

> the_wire 400 ---
> This game would be easy to win, if only you could time travel.
> 
> http://172.31.1.51/

## Write-up

The challenge is some sort of a lottery. The bidding procedure is as follows:

1. We send a ticket (some string) and a timestamp from the near future to the server.
2. The server then sends us a MAC signature of the (ticket, timestamp) pair.
3. There is a separate server which yields time-dependent tokens called beacons. However, it does not show beacons for timestamps from the future.
4. We wait for the time to come. Then the beacon is available both to us and to the main server.
5. Our goal is to get `H = SHA1(beacon, ticket)` such that H in hex starts with 7 zeros.
6. If it holds, we send (beacon, ticket, timestamp, mac) to the server, it checks the MAC and the beacon and gives us a flag.

The main problem is that we can't bruteforce ticket locally, since we don't know the beacon beforehand. Also there is some proof-of-work required to send tickets, so sending lots of tickets will not work.

## Shortcut Write-up

It turned out that there is an unintended bug in the redeeming procedure. Namely, the beacon could be adjusted by appending nullbytes and newline bytes. We can locally bruteforce a combination of those which will give the right hash.

First, we obtain some valid data:

```javascript
{
    "beacon": "V6ZqEIx3b3je7ItTnPnNDmTkAxS9WaSuAtOLxVjEmT6x2aP2fcJB5bMMuBFuwqA6a7f955rd+OHqOmrR4g7ZmiTqjM/0Eb+nkJ0W1VxsbCwQJ190PcpdyHk3n5wlWHKxJ/Tl10Rk/map75v+EWsQJANxDiHualWi7sDNuM4cyzroS/4K",
    "mac": "a8b4480d0d6c7ecae8c16e5f96480f93989e3fcd06ef3a595c172972325b5f69ca53947187056fb1fb64837f3011384bac98cdd12b8496af810651c7c7de0cab",
    "ticket": "pdl52g7qnbl2",
    "time": 1470523920
}
```

Then we bruteforce locally nullbytes and newlines:

```python
from random import randint
from hashlib import sha1

beacon = "V6ZqEIx3b3je7ItTnPnNDmTkAxS9WaSuAtOLxVjEmT6x2aP2fcJB5bMMuBFuwqA6a7f955rd+OHqOmrR4g7ZmiTqjM/0Eb+nkJ0W1VxsbCwQJ190PcpdyHk3n5wlWHKxJ/Tl10Rk/map75v+EWsQJANxDiHualWi7sDNuM4cyzroS/4K"
ticket = "pdl52g7qnbl2"
cnt = 0
while 1:
    sub = "".join(("\x00" if randint(0, 1) == 0 else "\n") for i in xrange(30))
    test = beacon + sub + ";" + ticket
    h = sha1(test).hexdigest()
    if h.startswith("0000000"):
        print "FOUND", h, sub.encode("hex")
        break
```

For example,

`app = "\x00\x0a\x0a\x00\x0a\x00\x0a\x00\x0a\x00\x00\x00\x0a\x00\x0a\x00\x0a\x0a\x00\x0a\x0a\x0a\x00\x00\x00\x0a\x00\x00\x0a\x00"`

does work. Then we append it to the beacon, submit it and get the flag:

**why_mak3_7rillions_wh3n_y0u_can_m4ke_bi1li0ns**

## Intended Way

The intended solution was to skew the Beacon server's clock by responding to the NTP requests it was sending to every client. To find this we should have listened and looked at the network traffic.

Then we could obtain beacons from the future and bruteforce the right ticket locally.

# Other write-ups and resources

* none yet
