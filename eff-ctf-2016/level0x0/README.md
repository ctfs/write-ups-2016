# EFF Capture the Flag @ Enigma 2016 - Level 0 The Social Notwork

** Description:

> X-net founder, M1k3y has gained access to "Transbay Interlink", the private social network that bay area police departments use for sharing information. See if you can find any useful information.
>
> https://level0x0.eff-ctf.org/

## Write-up

When we visit the website we get redirected to: https://level0x0.eff-ctf.org/home/M1k3y

We see that we have an unread message from the "Us Department of National Security": https://level0x0.eff-ctf.org/user/M1k3y/message/1

The url for our private message contains our username `M1k3y`. So we could try to change it to another username `usdhs` - https://level0x0.eff-ctf.org/user/usdhs/message/1

which gives us access to the secret message from "Us Department of National Security" which contains the flag `constitutionalrights`

## Other write-ups and resources

* <https://youtube.com/watch?v=LlSI6ErrbDI?t=38s>
