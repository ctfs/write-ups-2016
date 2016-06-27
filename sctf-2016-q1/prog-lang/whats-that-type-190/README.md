# sCTF 2016 Q1 : whats-that-type-190

**Category:** Prog-Lang
**Points:** 190
**Solves:** 4
**Description:**
I've got this little program here that I've written in a language I've theoretically designed called L^3 (pronounced L-cubed, stands for "Little Lambda Language"). It's a pretty simple language. It's missing a lot of the features you're probably accustomed to, but that's okay. It has only the following:

* numeric constants (unsigned and unbounded), written as you'd expect (`0, 3, 42, 7418`).
* Identifiers, written either `α or β` (yes, there are only two possible identifiers!).
* Functions, written `λid. body` where id is any valid identifier and body is any valid expression.
* Function application, written `f x` where f is a function and x is any valid expression.
* Addition, written "a + b" where a and b are any valid expression that evaluates to a number.
* Parentheses are welcome around any expression.

So, here's an example program: `(λα. λβ. α + β) 4 5`

You may find it useful to know that the Unicode value of λ is U+03BB, the Unicode value of α is U+03B1, and the Unicode value of β is U+03B2.

My language is all well and good, but I'm way too busy to implement it. I just want to know quickly if this program I wrote is valid. Can you figure out the type of the attached program for me? That'll be an easy way to check! We write types like this:

* numbers have the type `num`
* Functions have the type `T1 -> T2` where T1 and T2 are any valid type.
* Top is a type that matches any type, written `⊤`. The Unicode value of ⊤ is U+22A4.
* Parentheses are welcome around any type or subtype.
* Function arrows are right-associative. That is, `num -> num -> num` is equivalent to `num -> (num -> num)`.
So, here's some example types:

    num -> ((num -> (num -> num)) -> num)
    ⊤ -> ⊤ -> num
When you've figured out the type of my program, just submit it to my [test server](http://problems3.2016q1.sctf.io:11422/). If you figure it out, I'll give you the flag.


SHA512 Solution Hash(es):
    * f669c49720b22a194d1a70b894134b95aa33b7ef05c59b5dd24019de189416d0ed791e2d3938b1987dc97ce892521373ccce886ca08cbf3b01a4490295245882

**Hint**
I think Hindley and Milner had something to say about this...


## Write-up

(TODO)

## Other write-ups and resources

* none yet
