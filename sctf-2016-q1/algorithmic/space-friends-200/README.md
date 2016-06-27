# sCTF 2016 Q1 : space-friends-200

**Category:** Algorithmic
**Points:** 200
**Solves:** 43
**Description:**

UPDATE: The flag format changed slightly. The extra semicolon after the network4 answer has been removed.

We have a lot of friends because we're super popular, but unfortunately we have to split our set of friends into two halves so they can go into war with each other. That's just life, unfortunately.

We have a set of `N` friends, and `M` pairwise connections between friends. Each connection goes both ways, so if, for example, Aariss Weiron is friends with Bendelman, then Bendelman is also friends with Aariss Weiron. Each connection also has an associated weight, representing how close the two friends are, which is a positive integer value. No two pairs of friends with a connection have the same weight.

Our objective is to somehow divide our set of friends into two 'equal' halves. We also want to put friends who are pretty close to each other into the same set. We formally define the problem as follows:

> We have a set of friends of even size, some with bi-directional pairwise connections. Each connection has a positive integer weight, and each connection has a distinct weight. Our objective is to divide our friends into two sets of equal size with this property: The largest connection-weight that crosses between the two sets should be as small as possible. Compute this connection-weight for each friend network given. A crossing connection is one such that the two friends it connects are in different sets.
Each friend network is in the following format:

The first line has two numbers: `N` (guaranteed to be even) and `M` (number of connections). `M` lines follow this line. Each one represents a connection and has three tokens. The first two are the friends it connects, and the last one is the weight of the connection.

The flag format is the following:


    sctf{<network_1_answer>;<network_2_answer>;<network_3_answer>;<network_4_answer>}

Include the `sctf{}` part and the semicolons.

Note: To be eligible for prizes, you must send your team name and the code you used to solve this problem to adunna@sctf.io

SHA512 Solution Hash(es):
* a35ed0f78278701c1f5d188c799a48caabce8bf27fe28f4acfd5db779a60a3bebf956541bb7085fb09dc39cf3cadb580e479a17807e6863b6d01443fb1087a73

**Hint**
Fun graph theory :)

## Write-up

(TODO)

## Other write-ups and resources

* https://github.com/marodere/ctf/tree/master/2016/sctf/spacefriends
