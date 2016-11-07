# CSAW CTF 2016 Quals: Music_To_My_Ears

**Category:** Recon
**Points:**
**Solves:**
**Description:**

Yo fam have you listened to my mixtape?

`user:1245880440:playlist:7bUFR2ujh1p3GfArxM0dHE`

Hint: The recon spans multiple sites.

Hint: ![img](http://www.souljuicin.com/wp-content/uploads/2014/12/resized_425x282_red-beet.jpg)

## Write-up
=== Logical Steps ===
Determine these are components of spotify uri and search for playlist "spotify:user:1245880440:playlist:7bUFR2ujh1p3GfArxM0dHE"
=====================

#### Spotify
First letter of every song makes this:
"Checkout the last radio station"

### Logical Steps
"Last radio station" meants last.fm. This is a well known music site as well.

Last.fm:
In profile description:
https://www.youtube.com/playlist?list=PLeN5vwEfTqeDGL7tdudze3tU3T-K7Kvbr

Yo:checkout-my:mixtape-I:put:it:in-the:cloud
Encoded as:
Char :: BPM :: Song
Y    :: 89  :: 3 Days Grace - Everything About You
o    :: 111 :: Arcade Fire - Reflektor
':'  :: 58  :: Prince - Purple Rain
c    :: 99  :: D12 - Ain't Nuttin' But Music
h    :: 104 :: Eminem - The Real Slim Shady
e    :: 101 :: JR JR - As Time Goes
c    :: 99  :: OneRepublic - Something I Need
k    :: 107 :: A-Ha - I Call Your Name
o    :: 111 :: Goo Goo Dolls - Slide
u    :: 117 :: Aaron Carter	- Aaron's Party (come Get It)
t    :: 116 :: Guns N' Roses - Sweet Child O' Mine
'-'  :: 45  :: K-Ci & JoJo - Girl
m    :: 109 :: Mac Miller - Knock Knock
y    :: 121 :: R.E.M. - Orange Crush
':'  :: 58  :: Elliott Yamin - Wait For You
m    :: 109 :: The xx - VCR
i    :: 105 :: ABBA - Take A Chance On Me
x    :: 120 :: Baha - Men	Best Years Of Our Lives
t    :: 116 :: Daft Punk ft. Pharrell Williams - Get Lucky
a    :: 97  :: Shaggy Feat. Janet Jackson - Luv Me, Luv Me
p    :: 112 :: Steppenwolf - Magic Carpet Ride
e    :: 101 :: Grouplove - Ways To Go
'-'  :: 45  :: Pesado - No Te La Vas A Acabar
I    :: 73  :: Desiigner - Panda
':'  :: 58  :: Alt-J - Tessellate
p    :: 112 :: Kenny Chesney - Somewhere With You
u    :: 117 :: Nick Jonas - Jealous
t    :: 116 :: No Doubt - Hella Good
':'  :: 58  :: DJ Khaled ft. Chris Brown, Lil Wayne & Big Sean	How Many Times
i    :: 105 :: Coldplay - Birds
t    :: 116 :: Death Cab For Cutie - Title & Registration
':'  :: 58  :: Boyz II Men - You're Not Alone
i    :: 105 :: The Glitch Mob - We Can Make The World Stop
n    :: 110 :: One Direction - Little Things
'-'  :: 45  :: Tori Amos - Spark
t    :: 116 :: The Black Keys - Your Touch
h    :: 104 :: Flo Rida - Whistle
e    :: 101 :: Notorious B.I.G. ft. Puff Daddy & Lil Kim - Notorious B.I.G.
':'  :: 58  :: Usher - Moving Mountains
c    :: 99  :: Lupe Fiasco ft. Trey Songz - Out Of My Head
l    :: 108 :: Ed Sheeran - Photograph
o    :: 111 :: The Red Jumpsuit Apparatus - Remember Me
u    :: 117 :: Justin Timberlake - Sexyback
d    :: 100 :: Backstreet Boys - Quit Playing Games (with My Heart)

### Logical Steps
If you google `yo checkout my mixtape I put in the cloud`, soundcloud.com is the first result.

#### Soundcloud:
Going to `https://soundcloud.com/breadchris` you get:

`Dude, checkout my rss feed. That is where the true fresh beats are.`

### an0n0ps.xyz:
`chiptune.wav` has two alternating tones that can be interpreted as binary data.

`01100110011011000110000101100111 01111011011000110110100000110001 01110000011101000111010101101110 01100101010111110011010100110011 
01110110011001010111001001111101` = `flag{ch1ptune_53ver}`

## Other write-ups and resources

* [RawSec](https://rawsec.ml/en/CSAW-2016-10-Music-to-my-ears-Recon/
