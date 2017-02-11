# NCL 2016 Preseason : Browser-History-Analysis-230

__Category__: Log Analysis

__Points__: 230

## Write-up

<a href="https://jhalon.github.io/images/ncl8.png"><img src="https://jhalon.github.io/images/ncl8.png"></a>

For this challenge we are provided the following file: [NCL-2016-Pre-Firefox.sqlite](https://jhalon.github.io/download/NCL-2016-Pre-Firefox.sqlite)

You must download the file and open it up in a SQL database to solve the challenge. I used the [SQLite Viewer](http://inloop.github.io/sqlite-viewer/) online to access this information.

Once you have the SQL Database uploaded you will be presented with a page like so.

<a href="https://jhalon.github.io/images/sql1.png"><img src="https://jhalon.github.io/images/sql1.png"></a>

Once you are there, we need to navigate to the users browser history. So we will select __moz_palces__ from the dropdown.

<a href="https://jhalon.github.io/images/sql2.png"><img src="https://jhalon.github.io/images/sql2.png"></a>

You will be presented with the screen below... When you arrive at that screen, we will now be able to look for the answers to our questions.

<a href="https://jhalon.github.io/images/sql3.png"><img src="https://jhalon.github.io/images/sql3.png"></a>

--

__What did the user search for on craigslist?__

Looking for "__craiglist__" in the __url__ column, we see that line 244 will provide us with the answer.

<a href="https://jhalon.github.io/images/sql4.png"><img src="https://jhalon.github.io/images/sql4.png"></a>

__Answer: bitcoin__

--

__What was the current price of bitcoin when the user was browsing?__

All we have to look for here is a price in dollars. Line 246 will provide us that answer.

<a href="https://jhalon.github.io/images/sql10.png"><img src="https://jhalon.github.io/images/sql10.png"></a>

__Answer: 239.5__

--

__What Bitcoin exchange did the user log in to?__

The keyword here is "exchange" so we are looking for a site you can buy and sell Bitcoin, which will be in line 250.

<a href="https://jhalon.github.io/images/sql5.png"><img src="https://jhalon.github.io/images/sql5.png"></a>

__Answer: coinbase__

--

__What is the email that was used to log into the exchange?__

Since we don't see any login data - let's look for known emails. Line 268 shows us that he is logging into a gmail account. We can assume that he is using this to verify his bitcoin exchange.

<a href="https://jhalon.github.io/images/sql6.png"><img src="https://jhalon.github.io/images/sql6.png"></a>

__Answer: b1gbird@gmail.com__

--

__What was the ID of the Bitcoin transaction that the user looked at?__

Keyword here is "transaction" so let's just look for that in the title - and line 292 should provide us with the answer.

<a href="https://jhalon.github.io/images/sql7.png"><img src="https://jhalon.github.io/images/sql7.png"></a>

__Answer: 5274cfba585a4b5681527a37f95c76340428916bb7480cef6c545f0a28dcd2d7__

--

__What was the total value of all the inputs of the Bitcoin transaction?__

For this one, we have to grab and navigate to the [URL](https://blockchain.info/tx/5274cfba585a4b5681527a37f95c76340428916bb7480cef6c545f0a28dcd2d7) from our previous answer in line 292.

Our answer will be in the __Inputs and Outputs__ section of the website.

<a href="https://jhalon.github.io/images/sql8.png"><img src="https://jhalon.github.io/images/sql8.png"></a>

__Answer: 0.22616302__

--

__To which IP address did the majority of the Bitcoins in the transaction go?__

For this one - back at the website - just click __Visualize__ and you will be redirected to a map like page. Click the first transaction up top and you will get the IP Address.

<a href="https://jhalon.github.io/images/sql9.png"><img src="https://jhalon.github.io/images/sql9.png"></a>

__Answer: 176.223.201.198__

--

## Other Write-ups and Resources

* https://jhalon.github.io/ncl-log-analysis/
