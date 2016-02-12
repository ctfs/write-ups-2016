# Break In 2016 - Knock Knock

**Category:** Networking
**Points:** 200
**Author:** Parth Kolekar (aka SprinkleberryMuffin)
**Solves:** 5
**Description:**

> Find the flag.
>
>     <script>
>       setTimeout(function(){
>         $.ajax({
>           'url' : '',
>             success: function(){ window.location = '' },
>             headers: {Connection: 'close'},
>         });
>       }, 10000);
>     </script>
>
>
> Note: port-scanning is permitted for this question.
>
> Note: Sending heavy load with intent to crash server is not.
>
> Note: The Mail Server is not involved with this contest. 
>
> Hint: Like the base, it DROP
>
> Hint: A key port involved with this question is 1XXX.

## Write-up

The solution of this is to send a tcp packet to port 1143. This changes
the state of the web-server, and then you send a request to 
    
     https://felicity.iiit.ac.in:80/da3fcd1c-dee7-4c27-8523-82db5a4e1c8f

This prints out 
    
     flag: 7cc4c7e83e122b5f67d17585628f182f95b41581

Which is our flag.

## Extended Write-up

A little background on the server setup has to be given for this question.
The way that Felicity handles request is by a main [haproxy](http://www.haproxy.org/) load
balancer which forwards requests to internal nodes which are [lxc](https://linuxcontainers.org/) containers.

The main haproxy node is nicknamed `Yui`, all prefixed by `/contest` are sent to a contest portal
node nicknamed `Taiga`. This is a [nginx](http://nginx.org/) server. The main website is handled 
on a node nicknamed `Kurumi`. Kurumi is a [apache](http://httpd.apache.org/) server. 

The workflow is something like this 

    http://Yui:80/request -> Location: https://felicity.iiit.ac.in/request via haproxy
    https://Yui:443/contest -> http://Taiga:80/contest via haproxy
    https://Yui:443/default_url -> http://Kurumi:80/default_url via haproxy

    http://Taiga:80/contest -> contest data via nginx

    http://Kurumi:80/request -> main website data via apache

For this question a new node was introduced nicknamed `Mio`. This node had a ngnix server and 
[sslh](http://www.rutschle.net/tech/sslh.shtml) daemon which does the following.

    http://Mio:80/request -> http://Mio:8080/request via sslh
    http://Mio:8080/request -> Location: https://felicity.iiit.ac.in/request + X-Too-Insecure "Request Too Insecure" via nginx

    https://Mio:443/contest/breakin/question/1/1/ -> question data via nginx + X-Too-Secure "Request Too Secure"
    https://Mio:443/contest -> http://Taiga:80/contest via nginx +  X-Too-Secure "Request Too Secure"
    https://Mio:443/default_url -> http://Kurumi:80/default_url via nginx + X-Too-Secure "Request Too Secure"

    https://Mio:80/request -> https://Mio:8443/request via sslh
    https://Mio:8443/da3fcd1c-dee7-4c27-8523-82db5a4e1c8f -> flag data via nginx + X-Just-Right "https://felicity.iiit.ac.in:80/da3fcd1c-dee7-4c27-8523-82db5a4e1c8f"
    https://Mio:8443/contest -> http://Taiga:80/contest via nginx + X-Just-Right "https://felicity.iiit.ac.in:80/da3fcd1c-dee7-4c27-8523-82db5a4e1c8f"
    https://Mio:8443/default_url -> http://Kurumi:80/default_url via nginx + X-Just-Right "https://felicity.iiit.ac.in:80/da3fcd1c-dee7-4c27-8523-82db5a4e1c8f"
    
The node `Mio` is injected in the main workflow via iptables in Yui.
The iptables in Yui were set as follows. These are not the exact rules but provide an 
accurate enough representation

    *nat
    -A PREROUTING -m recent -m tcp -p tcp --dport 80 --rcheck --name FWPRT --rcheck --seconds 30 -j DNAT --to-destination Mio:80
    -A PREROUTING -m recent -m tcp -p tcp --dport 443 --rcheck --name FWPRT --rcheck --seconds 30 -j DNAT --to-destination Mio:443
    -A POSTROUTING -S Mio -j MASQUERADE

    *filter
    -A INPUT -m recent -m tcp -p tcp --name FWPRT --remove 
    -A INPUT -m recent -m tcp -p tcp --dport 1143 --name FWPRT --set -j DROP
    ...
    ... Doing what needs to be done in the felicity server
    ...
    -A INPUT -m tcp -p tcp -j REJECT --reject-with icmp-host-unreachable
    -A INPUT -m recent -p icmp --rcheck --name FWPRT -j REJECT --reject-with icmp-host-unreachable
    -A INPUT -p icmp -j REJECT --reject-with icmp-admin-prohabited

These are simple rules and in essence do the following

    Yui:80 -> if FWPRT then Mio:80 else Yui:80
    Yui:443 -> if FWPRT then Mio:443 else Yui:80
    Yui:1143 -> name set FWPRT + DROP packet
    Yui:default_port -> name unset FWPRT + REJECT with icmp-host-unreachable

    Yui(icmp) -> if FWPRT then REJECT with icmp-host-unreachable else icmp-admin-prohabited

The interesting points to note here are 

* On sending a tcp packet to 1143, the 80, 443 ports are transparently forwarded over to Mio.
* All tcp packets sent to any non important port result in this forwarding to go away.
* Once your time limit of 30s expires, the packet allowed to enter the filter chain which unsets name.
* Mio handles the requests identical to the workflow, so inserting it in the middle of the workflow has little to no visible effect.
* If you have set the FWPRT, then the requests come with a TTL of (TTL - 1) because of the extra hop.
* Instead of the sane tcp-rst which would allow a port scan to be completed quickly, we opted for icmp-host-unreachable. This marks all ports as filtered in nmap.

The icmp rules were simply added. There was no real importance of it in the question. The reject with icmp-host-unreachable makes [nmap](https://nmap.org/) 
slow. So slow that watching the nmap complete gave a time of 2hr to complete from my local network. A loop telnet, or netcat request over all ports works
much better and allows for the port scanning to be over in minutes if not seconds. As given in the hint, it *DROP*s the packets. 

The hidden message on the question (script) is to refresh the page repeatedly and attempt to break the keep-alive connection that exists
already. When you figure the hidden port 1143, and send it a packet, (which it drops), we hoped that the page refresh would kick in automatically and 
display the change in your page. In either case, it is a hint that the http server in involved in the contest, especially when adding this script 
makes a miserable job of being able to report comments on the contest page, since it reloads the page every 10 seconds. It was expected that people will 
keep this in mind when scanning for other ports, (since port knocking is usually on 3 ports). 

The [question data](question_data.html) shows "On the right path, you are". And this shows up as a result of sending a request to Mio:443 on the contest 
page url. (Which we hoped would happen automatically, if you kept a browser open on the contest page.). Even if this was not apparent, another hint was added
during the contest.

    After you get the Key Port, use your head.

This should make it very clear that you have to send a http/https request and check the headers which are sent back.

As noted above, the headers added are X-Too-Secure on https request to port 443, and X-Too-Insecure on http request on port 80. 
This is a play on words that suggest that you have to make a 'secure' request on 'insecure' port. 

Sending a https request on 80 reveals the header X-Just-Right with the correct url to get. This reveals the flag.

During performing these http,https requests it may be that your 30 seconds are up, and all the headers simply dissapear,
it was expected that you would repeat the tcp packet on port 1143 and get the forwarding back with yourself.

# Other write-ups and resources

* none yet
