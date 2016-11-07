# IceCTF-2016 : toke-45

**Category:** Web
**Points:** 45
**Description:**

I have a feeling they were pretty high when they made this website...

## Writeup

The use of the word `toke` hints the challenge may refer to tokens used in web authentication. By creating an user and logging it, use browser developer tools to record the post requests being sent. In the response header of the HTTP response should be `Set-Cookie: jwt_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmbGFnIjoiSWNlQ1RGe2pXN190MEszbnNfNFJlX25PX3AxNENFX2ZPUl81M0NyRTdTfSIsInVzZXIiOiJhemEifQ.Zfl286kFvhPrNJG-dtoTjbPU7OxlUdTW_XKEL679uU0;`. JWT stands for JSON Web Tokens, which are comprised of a base64 encoded hash algorithms, a payload which is base64 encoded content, then finally a signature, a hashed concatenation of the header and payload. Taking the web token collected from the POST request, split it into 3 parts, seperated by the `.` in the token. Base64 decoding (there are websites taht will do this for you) the first part of the token (header) outputs `{"alg":"HS256","typ":"JWT"}`. Then base64 decode the second part, which returns `{"flag":"IceCTF{jW7_t0K3ns_4Re_nO_p14CE_fOR_53CrE7S}","user":"aza"}`.

## Other write-ups and resources

* https://github.com/WCSC/writeups/tree/master/icectf-2016/Toke
* [RawSec](https://rawsec.ml/en/IceCTF-45-Toke-Web/)
* [Japanese](https://ctftime.org/writeup/3814)
* https://github.com/Idomin/CTF-Writeups/blob/master/IceCTF/Toke-Web-45
* https://github.com/grocid/CTF/tree/master/IceCTF/2016#toke-45-p
* https://youtu.be/ACsakftX2L4
* https://gitlab.com/Babache/writeups/tree/master/CTF/IceCTF2k16/Stage-2/Toke
