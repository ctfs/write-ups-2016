# CSAW CTF 2016 Quals: Eric_Zhi_Liang

**Category:** Recon
**Points:** 10
**Solves:**
**Description:**

We tried very hard to find Eric last year. You're going to have to try just as hard this year, since not even his friends can find him.

We heard Eric has his own subreddit. Can you find Eric for us?

## Write-up

Find the subreddit [r/ericliang](https://www.reddit.com/r/ericliang).

[theRealEricLiang](https://www.reddit.com/user/theRealEricLiang) is a moderator for the subreddit. Wading through his posts, he went to a [NYC Hackster Meetup](https://www.reddit.com/r/creativecoding/comments/51fas9/has_anyone_worked_with_the_intel_edison/).

Looking for "nyc meetup hackster intel edison" on Google, the first result is a [Meetup event](http://www.meetup.com/Hackster-NYC/events/232881069/).

His Meetup event profile picture matches his GitHub profile picture; so it is the right Eric Liang. His introduction is "I love fanfiction and Allen Lau!".

Allen Lau is a founder of Wattpad, which is a site where users can post their stories. Searching for Eric Liang on Wattpad, 20 people show up, but there is the one and only [Eric Zhi Liang](https://www.wattpad.com/user/ericZhiLiang) with a Missing Poster. The flag is on the left of his profile.


## Flag
`flag{i_readbear_fanfix}`

## Other write-ups and resources

* https://utdcsg.github.io/csaw-quals16/recon/ericzhilang.html
* [Jhin Su](https://github.com/JhinSu/CSAW-2016-Write-Ups/tree/master/Recon/Eric-Zhi-Liang)
