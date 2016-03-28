#Volga CTF Quals 2016 tic-tac-toe writeup

###*Category:* PPC *Points:* 200

> An important step towards the strong AI is the ability of an artificial agent to solve a well-defined problem. A project by the name 'tic-tac-toe' was one of such test problems. It's still up...
>
> nc tic-tac-toe.2016.volgactf.ru 45679

## write-up

For this problem, I did a bit of playing against their AI normally It seemed as
though their AU cares more about making a specific setup to win than actually
stopping us. (I've seen it not stop me from getting three in a row on it's turn )

Knowing this, my script was very simple. There are two methods that are
essentially the same, one assesses for when you start, one for when the
opponent starts. It will: (in order of priority) make the winning move if there
is one, stop the opponent's winning move, or make a random move. This seemingly
unstrategic method will give you a score approximately 3 times that of their
AI. 

This code was written at 3 or 4 AM, so if anything needs clarified please
contact me (@bert88sta).

[tic-tac-toe.py](./tic-tac-toe.py)

## Other write-ups and resources

* <http://www.codehead.co.uk/volgactf2016-tic-tac-toe/>
