#Volga CTF Quals 2016 amazing writeup

###*Category:* PPC *Points:* 250

> An important step towards the strong AI is the ability of an artificial agent to solve a well-defined problem. A project by the name 'amazing' was one of such test problems. It's still up...
>
> nc amazing.2016.volgactf.ru 45678

## write-up

This was an exceptionally fun problem. I'd like to give you an overview
of my code so it's understandable :)

I used a recursive algorithm to solve this. The algorithm is called every time
you have more than one move to make. You aren't allowed to go backwards, so it
is only called when you have two *new* directions to go. The newly forked
algorithms will return False if they hit a dead end or if all of the sub
branches return false. If it hits "#" then it returns the value to make that
move so the algorithm can "see" what's next. Finally, the winning condition is
that you are in the bottom right of the map, so it test to see if you are
there.

I tried to document my code well enough, feel free to contact me (@bert88sta).

[maze.py](./maze.py)
## Other write-ups and resources

* <https://github.com/EspacioTeam/write-ups/tree/master/2016/volga/Amazing>
