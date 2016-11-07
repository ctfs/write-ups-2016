# sCTF 2016 Q1 : i-cant-get-no-satisfaction-130

**Category:** Prog-Lang
**Points:** 130
**Solves:** 55
**Description:**

I've got another task for you involving my little language, Prop!

It consists of the following expressions (denoted `e`):

* Boolean constants, written `true` and `false`.
* Boolean variables, written as any alphabetical string.
* Implies, written `e -> e`.
* Equivalence, written `e <-> e`.
* Negation, written `!e`.
* And, written `e && e`.
* Or, written `e || e`.
You can also parenthesize any expressions or subexpressions (so, you can write `(a || b) && c)`. Here's another example program:

    (a || b) && c && d && (!d || b) || (b -> c) && (d <-> a)

This time, I've determined that the attached program is satisfiable, but I want to know the actual values that make this program satisfiable. Can you find me a satisfying model, please? When you've found one, submit a GET request to our [server](http://problems3.2016q1.sctf.io:11420/). Any missing keys are considered false.

Here's an example request:

    http://problems3.2016q1.sctf.io:11420/?a=true&b=true&c=false

This request would treat `a` and `b` as `true` and `c` and the rest of the variables as `false`. Thus, it's only necessary to assign the true keys to the value true.


SHA512 Solution Hash(es):
* bb5d6f98cc3b4d722893b98d6cdb112c675da0cf1c09310a824a2b6131297f193b530e2e812281cf3b0274daaa78633fb61f33e8b118bea42325a3a12c934b30

**Hint**
You'll probably want to figure out how conjunctive normal form is defined...

## Write-up

(TODO)

## Other write-ups and resources

* [0x90r00t](https://0x90r00t.com/2016/04/19/sctf-2016-code-130-i-cant-get-no-satisfaction-write-up/)
