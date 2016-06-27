# sCTF 2016 Q1 : can-nerds-fly-100

**Category:** Prog-Lang
**Points:** 100
**Solves:** 12
**Description:**

UPDATED: This problem now uses a grading server instead of asking for the size of the CNF.

I've got a task for you involving a program language I've created! It's called Prop (short for Proposition), and as you might expect, it's a simple language for propositional logic. It consists of the following expressions (denoted `e`):

* Boolean constants, written `true` and `false`.
* Boolean variables, written as any alphabetical string.
* Implies, written `e -> e`.
* Equivalence, written `e <-> e`.
* Negation, written `!e`.
* And, written `e && e`.
* Or, written `e || e`.
You can also parenthesize any expressions or subexpressions (so, you can write `(a || b) && c)`. Here's another example program:

    (a || b) && c && d && (!d || b) || (b -> c) && (d <-> a)

So, what I'd like from you is for you to calculate the conjunctive normal form (CNF) of the attached program. You can submit the CNF [here](http://problems4.2016q1.sctf.io:11426/).


SHA512 Solution Hash(es):
* 3b491cd03f456e40d0166acce6be897ac9e2f2c3e5fabfc7a0d980ef07bf92eb1bc4b16228accf60d111e28a1dd

**Hint**
You'll probably want to figure out how conjunctive normal form is defined...

## Write-up

(TODO)

## Other write-ups and resources

* none yet
