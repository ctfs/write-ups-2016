# Break In 2016 - Oops

**Category:** web
**Points:** 50
**Solves:** 35
**Description:**

>     <style></style> (this line is escaped)
>     <script src="https://felicity.iiit.ac.in/contest/breakin/static/jquery.min.js"></script>

# Write-up

The content of the attached jquery.min.js has a line attached to it in the bottom. 
This line does 
    
    var content=ajax.fetchPage("http://example.com").toDOM();content.querySelector("h1").parentNode.childNodes[3].innerHTML.split(" ").slice(26).join(" ");

This is a straight forward question to open http://example.com nad the do split, slice and join operations on it's text. 

The related line on http://example.com was 

    This domain is established to be used for illustrative examples in documents. You may use this domain in examples without prior coordination or asking for permission.

On applying the split, slice, and join we end up with 

    asking for permission.

Which is the flag.

# Other write-ups and resources 

* None

