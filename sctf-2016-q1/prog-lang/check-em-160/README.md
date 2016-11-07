# sCTF 2016 Q1 : check-em-160

**Category:** Prog-Lang
**Points:** 160
**Solves:** 7
**Description:**

UPDATED: This problem now uses a grading server instead of asking for the size of the CNF.

I've got this program in a language I've made called Imp (short for Imperative). It's a straightforward language. It probably amounts to a very simplified version of languages you already know. Let me tell you about it. It has all the following.

Arithmetic expressions (denoted `a`) featuring:

* Numeric constants (unsigned and unbounded), written as you'd expect (`0, 3, 42, 7418`).
* Identifiers, written as any alphabetical string.
* Addition, written `a + a`.
* Multiplication, written `a * a`.

Boolean expressions (denoted `b`) featuring:

* Boolean constants, written `true` and `false` respectively.
* Negation, written `!b`.
* And, written `b && b`.
* Or, written `b || b`.
* Less than, written `a < a`.
* Greater than, written `a > a`.
* Equals, written `a = a`.
* Less than or equal to, written `a <= a`.
* Greater than or equal to, written `a >= a`.

Statements (denoted `s`) featuring:

* Variable assignments, written `id <- a` where id is any alphabetical identifier.
* Sequencing, written `s; s`.
* If statements, written `if b then s else s`
* Skip, written `skip`
* Panic, written `panic`

In addition, the last line of the program contains a post-condition for the program written `{b}`.

So, here's an example program:

    y <- 4;
    if x < y then skip else panic;
    y <- x * 2;
    if y < x then panic else skip;
    z <- x + y
    {z = 3 * x && y = 2 * x}

I want to be able to use my program and ensure that it works, but in order to do so, I need to know under what conditions its safe to run it. Can you figure out the most permissive set of conditions that will ensure that my program completes with the specific post-condition? When you've figured it out, submit it to this server.


SHA512 Solution Hash(es):
* dd25a685f7772c596ce5f7ea6f31bea6d3f22caafdaf49ca65f4a942918b86ec04833b3faa1a7f98e29a1baed5da2ed1

**Hint**
I believe Wikipedia has something to say about predicate transformer semantics...


## Write-up

(TODO)

## Other write-ups and resources

* [0x90r00t](https://0x90r00t.com/2016/04/19/sctf-2016-code-130-i-cant-get-no-satisfaction-write-up/)
