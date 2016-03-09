# Cyber Security Challenge 2016: The Smokescreen Challenge

**Category:** Network Security  
**Points:** 70  
**Challenge designer:** Jérôme Devigne  
**Description:**
> Start here: 52.17.52.40 . Don't aim too high.
> 
> Hints: 
>* “sometimes size DOES matter”
>* “knock knock! Who’s there?”
>* “diabolus in musica”


## Write-up
The challenge is centred on a server that has a bit of “security by obscurity” in place which will render traditional approach difficult if not even impossible. 

To get access to the server itself where the solution flag is stored, the exposure is very limited and it will be required to use a technique 
called ‘port knocking’ in order to remove the “smokescreen” and open an SSH access. In order to do this, there is a riddle to solve where instructions on what to do is literally hidden in plain sight. The final elements require some music theory knowledge in order to find the actual sequence.

####1) Initial discovery

Starting point is only an IP. Scanning for most used port will not reveal anything as only port TCP 440 is opened. A more thorough scan is required. Additionally, the open port will not show banners indicating a known service as it’s announcing “Mohawk net deliverer”.

-  TCP 440: port number itself is actually an hint to make the link with music theory topic as it’s the pitch frequency of the note A4 in hertz; which is also a common reference used for tuning musical instruments 
-  “Mohawk net deliverer” is an intended pun, the service being in reality an ‘apache web server’ (Mohawk is another Amerindian tribe (as apache), Net and web are more or less synonims, Deliverer is a non-existing English word that mimics server (to deliver and to serve being rather similar)

####2) The riddle

Visiting the website (on port TCP 440) with a web browser will reveal a very simple html page that looks like a private message left to Erik (one of the challenge organisers). The message proposes a songs playlist to be listened to during the challenge and is literally indicating what to do (see below).

- By observing the page under more scrutiny (by simple observation if you have really good eyes or looking at the source code for example), some words from the songs titles are actually written slightly bigger than the rest. This is true for all songs except one which is a bit more special (see next section).

Isolating these words gives: “Knockin stateless port order frequency first 8 sound 17 seconds devil music”. 
This actually tells to ‘knock (knockin) UDP (stateless) ports (port); the sequence (order) being the note (sound) frequency (frequency) of the first (first) 8 (8) notes from the ‘17 seconds devil music’.

To get access, challengers will need to set up a knock client and find a certain sequence of eight notes. The ’17 seconds devil music’ part refers to the only song that has not been used so far (which is mentioned in the text as being ‘specially selected’), a bit of googling (or knowledge) can reveal the
following:

- The song “Purple Haze” from Jimi Hendrix is known to be containing a specific music structure present in the first 17 seconds of the song (then repeated later in the song). This musical structure is  known as “diabolus in musica” which is a sequence of 2 notes with a frequency interval of exactly 3 tones; this structure was explicitly forbidden by the catholic church for centuries as it’s believed to be calling the devil and opening the doors of hell… 

####3) Parameters required

As stated above, the key is actually the 8 first notes from the first 17 seconds of the song Purple Haze from Jimi Hendrix. By looking for any guitar tab (partition) on the internet, the songs starts with 4 repetitions of 2 notes: Bm3 and Bm4 which have respectively a frequency of (in hertz, rounded): 233 Hz and 466 Hz.

- The sequence is (all in UDP, stateless): 233, 466, 233, 466, 233, 466, 233, 466

####4) Extra step of annoyance

Once using a correctly set up knock client (multiple implementation exist) with the above mentioned sequence, the server reveals an extra open port (TCP 666) where a SSH daemon is running.

- Hint: the playlist page refers to ‘while the kids are in hell’; open port is 666 is a reference to the “number of the beast” which is associated in biblical references to hell
- If the hint is not understood… an new complete TCP scan will reveal it.

But it’s not over yet… because there is only one user that has access to the server through SSH… The last sentence of the playlist page literally gives out the solution: `“this guy will unlock the full potential of u brain”`

- “this guy will unlock” = password is: ‘jimi hendrix’

- u brain = spelling mistake is voluntary and indicates user (u) is ‘brain’

####5) The loot

Finally, once connecting with a SSH client to the server on port 666 with the right credentials, challengers will get a message saying:

`Good job, the flag is "I_can_see_clearly_now_the_smokescreen_is_gone"`

## Solution
I\_can\_see\_clearly\_now\_the\_smokescreen\_is\_gone
## Other write-ups and resources
- None yet.
