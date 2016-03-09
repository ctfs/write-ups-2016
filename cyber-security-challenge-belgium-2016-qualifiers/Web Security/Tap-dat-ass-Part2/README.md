# Cyber Security Challenge 2016: Tap dat ass part 2


**Category:** Web Security  
**Points:** 80  
**Challenge designer:** Tom Van Goethem  
**Description:**  
> The second part will be slightly harder. We know that one of the hard-working PhD students from the University of Leuven wanted to test the challenge. However, the idiot registered with the second flag in his nickname. Hopefully your 31337 h4x0r sk1llz are sufficient to retrieve this flag!
> 
> Note: this challenge is built with some of the latest and coolest HTML features. If it does not work in your browser, try using the latest Chrome version.

[File Here](challenge-source-files/src.zip)

>Hint: WebSockets are so much fun! You should try it out for yourself!

## Write-up
Looking at the queries that are being made, we see that there is one that sort-of stands out since it's the only one that uses a user-defined escape function (`escapeStr`):

```js
connection.query('UPDATE difficulties SET difficulty = ' + escapeStr(param.difficulty) + " WHERE playerId = '" + escapeStr(param.playerId + "'"), function(err, result) {
    console.log('Updated difficulty for ' + param.playerId + ' to ' + param.difficulty);
    connection.release();
});
```

Looking at the `escapeStr` definition, we can see that it removes certain characters from the input, including quotes. This means that we can't escape the string sequence for `playerId`. However, since the program expects the `param.difficulty` to be numerical, it did not encode the value with strings. This means that we should inject our exploit in `param.difficulty`.
Another difficulty will be that the injectable parameter is in an `UPDATE` query, errors are not returned to the user, and finally the parameter is cast to an `INT` (because of the type of the column).
As a first part of the exploit, we will need to update the difficulty. That's actually quite easy, as we already did that in Part 1. Next, we'll need to bypass a simple (a wrong) check that the provided value is an integer (as we'll obviously need to inject a string to do the SQL injection): `parseInt(param.difficulty) > 0`.
Interestingly, `parseInt` will return a value other than `0` when the string starts with a numerical value. Great. So then we know that we have to start the `difficulty` parameter with a numerical value.

From the queries in app.js, it seems that `difficulties` only has two columns: `playerId` and `difficulty`. Since we can only retrieve the value of the `difficulty` column (since `playerId` is only used in `WHERE` clauses), we will have to use that one to extract content.
It's also important to note that when we set two columns with the same name in an `UPDATE` query, MySQL will use the latter value. This means that we can do inject like `1, difficulty = 1337`, which will result in `difficulty` being set to `1337`.

The challenge description hints that the flag is somewhere in the highscores, located in a player's name. To be able to extract it, we will need to use a subquery to extract it, something like `1, difficulty = (SELECT playerName FROM highscores LIMIT 1)`. However, that will probably result in 0, as the value is implicitly cast to an integer. To bypass this, we can use the MySQL functions `HEX` and `CONV`. First, we convert the string to a hexadecimal representation using `HEX`, and then we convert this value to a decimal representation using `CONV`: `1, difficulty = (SELECT CONV(HEX(playerName), 16, 10) FROM highscores LIMIT 1)`. To prevent integer overflow, we'll have to use `SUBSTRING`, so our exploit then becomes `1, difficulty = (SELECT CONV(HEX(SUBSTRING(playerName, 1, 4), 16, 10) FROM highscores LIMIT 1)`.

After this, all we have to do is set up the WebSocket connection, make the appropriate calls, and convert the integer value back to their string representation. The complete solution can be found [here](challenge-source-files/part2.js) (should be run in your browser console).
 
##Solution
sql\_injection\_taps\_asses\_all\_the\_time
## Other write-ups and resources
