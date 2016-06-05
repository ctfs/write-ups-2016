# tjctf-2016 : cipher-font-50

**Category:** Web**Points:** 50
**Description:** This webpage contains a flag!

## Write-up

By attempting to copy and paste the text displayed on the webpage, it is obvious the displayed characters are not the true text of the page. However, upon closer inspection, each displayed character represents a single text character. For example, the actual character '(' is - as a result of the font - displayed as a 'w'. Following the same pattern, the actual character '[' is displayed as 'L'. The fastest  way to decrypt this large chunk of text would be to write a program that substitutes characters from the copied text to the character they display as. Pasting the text from the page into the program and having it substitute characters would produce you with a string identical to that which is displayed on the challenge's web page. Then, before your program ends, have it print out that new string hashed with MD5. Last, surround that hash value with the traditional tjctf{} format and you will end up with `tjctf{232bd3180db2e7261ad2d94b725c9008}`

## Other write-ups and resources

* [MilWestA - CTFtime.org](https://ctftime.org/writeup/3451)
