# Break In 2016 - I have the power

**Category:** Web
**Points:** 100
**Solves:** 30
**Description:**

> Go to the right places and don't make any mistakes.
>
> (Right Places is a link to the contest page)

## Write-up

by [ParthKolekar](https://github.com/ParthKolekar)

The request handler source code (in python) is as follows

    def is_power2(num):
        return num != 0 and ((num & (num - 1)) == 0)

    def challenges(request, param):
        FLAG = 'Flag: TriColour'
        if 'seq_count' not in request.session:
            request.session['seq_count'] = []
        elif request.session['seq_count'] == 'Done':
            return HttpResponse(FLAG)
        if len(request.session['seq_count']) > 9:
            request.session['seq_count'] = 'Done';
            return HttpResponse(FLAG)
        try:
            l = request.session['seq_count']
            i = int(param)
            if is_power2(i):
                if i not in l:
                    l.append(i)
                    request.session['seq_count'] = l 
                    return HttpResponse("+1, " + str(len(l)))
                else:
                    return HttpResponse("+0, " + str(len(l)))
        except ValueError:
            pass
        request.session['seq_count'] = []
        return HttpResponse("+0, 0")

Reading the source it is obvious what you have to do to get the flag.
You have to make a request having a param having a value which is a 
power of two. 

On making a request with param not a power of two, the id resets. 
The link in the question statement was a request to this controller with 
the parameter 1.

This is shown by the output 

    +0, 0

If you have entered a number which is a power of 2, then the response is 
either 

    +1, <number of power of 2 entered>

if the number has not been given already or 

    +0, <number of power of 2 entered>

if the number given is already given.

On giving any 9 numbers, the flag is unlocked and the session is edited to
always give you the flag.

## Other write-ups and resources

* none yet
