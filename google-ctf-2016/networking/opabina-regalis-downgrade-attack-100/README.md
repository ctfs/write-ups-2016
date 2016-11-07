# google-ctf-2016 : opabina-regalis-downgrade-attack-100

**Category:** Networking
**Points:** 100
**Solves:** 53
**Description:**
Following on from Opabina Regalis - Token Fetch, this challenge listens on ssl-added-and-removed-here.ctfcompetition.com:20691.

To ensure that your code works as expected, you should use the following test case:
~~~~
   chk = CalcPass("Mufasa", "testrealm@host.com", "Circle Of Life", "GET", "/dir/index.html", "dcd98b7102dd2f0e8b11d0f600bfb0c093", "00000001", "0a4f113b")
  if chk != "6629fae49393a05397450978507c4ef1" {
    your_calculation_is_incorrect();
  }
~~~~
Additionally, you should format your Exchange_Headers such as:

~~~~
  v.Key = proto.String("Authorization")
  v.Value = proto.String(`Digest username="Mufasa",realm="testrealm@host.com",nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093",uri="/dir/index.html",qop=auth,nc=00000001,cnonce="0a4f113b",response="6629fae49393a05397450978507c4ef1",opaque="5ccc069c403ebaf9f0171e9517f40e41"`)
~~~~

## Write-up

(TODO)

## Other write-ups and resources

* https://github.com/Blystad/googlectf_writeups/tree/master/networking/opabina_regalis_downgrade_attack
* [Nick Frost](https://blog.nfrost.me/2016/05/01/google-ctf-2016-downgrade-attack.html)
