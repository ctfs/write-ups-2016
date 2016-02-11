# Break In 2016 - Knock Knock

**Category:** Networking
**Points:** 200
**Author:** ParthKolekar
**Solves:** 5
**Description:**

> Find the flag.
> Note: port-scanning is permitted for this question.
> Note: Sending heavy load with intent to crash server is not.
> Note: The Mail Server is not involved with this contest. 
>
> Hint: Like the base, it DROP
> Hint: A key port involved with this question is 1XXX.

# Write-up

The solution of this is to send a tcp packet to port 1143. This changes
the state of the web-server, and then you send a request to 
    
     https://felicity.iiit.ac.in:80/da3fcd1c-dee7-4c27-8523-82db5a4e1c8f

This prints out 
    
     flag: 7cc4c7e83e122b5f67d17585628f182f95b41581

Which is our flag.

# Extended Write-up

(TODO)

# Other write-ups and resources 

* none yet
