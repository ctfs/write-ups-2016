# Hack.lu CTF 2016 : cthulhusoft-350

**Category:** Reversing
**Points:** 350 (-35)
**Solves:** 20
**Description:**

>Dear Stranger,
>We are Cthulu-Tek, developers of the infamous Cthulu Messenger, and we might have a small problem. Our CPO (chief praising officer) received an anonymous email containing highly sensitive >details about Cthulu - or at least it claimed so before encrypting all our data. Within this data was the routine for the key generation server for our Cthulu Messenger and since our backup >files suddenly disappeared, we don't have the routine anymore at all...
>It came to our attention, that you are a specialist for.. let's call it 'key generation routine recovering'. Please have a look at the application we provide you, extract the key generation >routine and generate keys for our customers at cthulhu.fluxfingers.net:1515.
>We make sure it will be worth it.

>- Cthulu-Tek

>Attachment: [cthulhusoft](cthulhusoft)
>Fingerprint: SHA256 D4:D9:8F:83:0E:20:2A:30:39:21:CB:06:76:E4:EF:BE:C5:CD:AB:71:1F:8C:7E:34:58:34:AC:82:E1:2C:2D:1D

## Hint

`openssl s_client -host cthulhu.fluxfingers.net -port 1515`

## Write-up

(TODO)

## Other write-ups and resources

* none yet
