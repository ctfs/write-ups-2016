# CSAW CTF 2016 Quals: Moms_Spaghetti

**Category:** Pwn
**Points:** 500
**Solves:**
**Description:**

ohai

So this challenge is based on a real bug I found in a thing one time reversing.
The bug is tricky. Do you see it? I can totally give a write-up / break down.

The environment will be important because heap mastery is required, and I have
only proven it against Ubuntu 16.04 (or whatever latest is) 64bit.

The challenge itself is intentionally 32bit because I wanted to recreate the 
exact. I have included a proof of concept exploit. It's not 100% reliable, but
so far it hasn't crashed on failure (because of the nature of the bug), and 
has usually only fails on the first try (if at all), probably something to do
with the system being cranky about issuing memory until the first round of
grooming. The exploit executes a command to cat flag.txt and then request its
output to a webserver (though the contestants can get creative).

The service runs on port 24242, and needs to be able to connect out to 
contestants. This is important. The reason why: to groom the heap, I opted for
threads. The service accepts connections, fork()s, then the client can 
specify a port and a count of threads to connect back to them. This way the 
clients don't interfere with each other's memory space etc.

Please put the attached flag.txt into running directory of the service. Also
you probably don't want to recompile if we want it reproducibly exploitable 
(with a poc to show the haters then they hate).

-raid

## Write-up

(TODO)

## Other write-ups and resources

* https://pastebinthehacker.blogspot.de/2016/09/csaw-2016-pwn-500-momspaghetti-draft.html?m=1
* http://pastebin.com/GEwz7WqZ
* https://github.com/eaglePwn/CTFwriteup/blob/master/csaw2016/mom_spagetti/solve_pl.py
* http://ctfhacker.com/pwn/2016/09/19/csaw-moms-spaghetti.html
