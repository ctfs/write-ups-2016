# ABCTF 2016 : the-big-kahuna-120

**Category:** Ppc
**Points:** 120
**Solves:** 133
**Description:**

What's the smallest amount of steps (additions, deletions, and replacing) it would take to make the string "massivegargantuanhugeepicginormous" into "tinysmallmicroscopicinvisible"? Don't guess too many times or we will disqualify you. Remember to wrap your answer in abctf{}.

[HINT] Dynamic programming. It's a thing that exists. Example: "Cat" to "That" would take 2 steps, as you replace the "C" with an "h" an add a "T" to the front.


## Write-up

Just use your favourite algorithm for finding the [edit distance](https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance) to obtain the answer of 28.

That yields the flag: `ABCTF{28}`

## Other write-ups and resources

* none yet
