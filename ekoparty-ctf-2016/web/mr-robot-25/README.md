# EKOPARTY CTF 2016 : mr-robot-25

**Category:** Web
**Points:** 25
**Solves:**
**Description:**

> Disallow it!

## Write-up

The two biggest clues in this challenge are the title and the description. If you were to search around about `robots`, `web`, and `disallow`, you should come across information regarding a domain's `robots.txt` file. You can read more about it [here](http://www.robotstxt.org/robotstxt.html) but generally it's a file stored in the root of most domains that search engines (like Google) read before `crawling` (adding pages from that to search result collections) the website. This file instructs the search engine what it can crawl. If you go to `https://ctf.ekoparty.org/robots.txt` you will be show the following raw text:

```
User-agent: *
Disallow: /static/wIMti7Z27b.txt
```

If you then go to that link `https://ctf.ekoparty.org/static/wIMti7Z27b.txt` you will find the flag: `EKO{robot_is_following_us}`

## Other write-ups and resources

* none yet
