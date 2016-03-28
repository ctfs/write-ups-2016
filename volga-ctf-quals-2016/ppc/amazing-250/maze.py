from pwn import *

def assess_maze(maze,psn,made_moves):
    potentials= []
    make_moves=""

    # Assess adjacents until # is reached?
    while True:

        #Winning Condition:
        if psn[1]>len(maze[0]):
            return [make_moves + "r","Win"]

        """ DETERMINE POTENTIAL MOVES """
        #TEND Right and Downwards
        #Right
        if maze[psn[0]][psn[1]+2] == "#": return [make_moves,psn,"#"]
        if maze[psn[0]][psn[1]+2] == "|": pass
        if maze[psn[0]][psn[1]+2] == " ": potentials.append("r")
        #Down
        if maze[psn[0]+1][psn[1]] == "#": return [make_moves,psn,"#"]
        if maze[psn[0]+1][psn[1]] == "-": pass
        if maze[psn[0]+1][psn[1]] == " ": potentials.append("d")
        # Up
        if maze[psn[0]-1][psn[1]] == "#": return [make_moves,psn,"#"]
        if maze[psn[0]-1][psn[1]] == "-": pass
        if maze[psn[0]-1][psn[1]] == " ": potentials.append("u")
        #Left
        if maze[psn[0]][psn[1]-2] == "#":return [make_moves,psn,"#"]
        if maze[psn[0]][psn[1]-2] == "|": pass
        if maze[psn[0]][psn[1]-2] == " ": potentials.append("l")

        """ DON'T BACKTRACK """
        #Remove the option to go backwards from the list of moves
        if len(made_moves)>0:
            if reverser[made_moves[-1]] in potentials:
                potentials.remove(reverser[made_moves[-1]])

        """ MAKE SINGLE MOVES """
        #This makes moves when there is only one choice.
        if len(potentials)==1:
            make_moves+=potentials[0]
            made_moves+=potentials[0]
            if potentials[0]=="d":
                psn[0]+=2
            if potentials[0]=="r":
                psn[1]+=4
            if potentials[0]=="u":
                psn[0]-=2
            if potentials[0]=="l":
                psn[1]-=4

        """ TEST BRANCHES """
        #Branches will return either a False (Dead End)
        #Or the set of moves to be made until the next branch
        if len(potentials)>1:
            branch = False
            for x in potentials:
                if x=="u":
                    result = assess_maze(maze,[psn[0]-2,psn[1]],"u")
                elif x=="d":
                    result = assess_maze(maze,[psn[0]+2,psn[1]],"d")
                elif x=="l":
                    result = assess_maze(maze,[psn[0],psn[1]-4],"l")
                elif x=="r":
                    result = assess_maze(maze,[psn[0],psn[1]+4],"r")
                if result[0]!=False:
                    branch=True
                    make_moves+=x
                    made_moves+=x
                    make_moves+=result[0]
                    made_moves+=result[0]
                    psn = result[1]
                    return [make_moves,psn]
            if branch==False:
                return [False,False]
        """ RETURN FALSE IF NO MOVES """
        if len(potentials)==0:
            return [False,False]
        potentials = []
    return [make_moves,psn]

reverser = {"u":"d","d":"u","l":"r","r":"l"}
HOST,PORT = "amazing.2016.volgactf.ru" ,45678
r=remote(HOST,PORT)
for x in range(4): r.recvline()
for x in range(30):
    r.recvline()
    r.recvline()
    made_moves=""
    real_moves=[""]
    posn=[1,2]
    while True:
        print r.recvline()
        maze = []
        for x in range(41):
            a=r.recvline().rstrip("\n")
            maze.append(a)
        print "-----------REAL-----------"
        for x in maze: print x
        print "REAL MOVES: " + str(real_moves)
        assessment = assess_maze(maze,posn,real_moves[-1])
        moves=assessment[0]
        real_moves.append(moves)
        r.sendline(moves)
        if assessment[1]!="Win": posn=assessment[1]
        else: break

print r.recvline()
print r.recvline()
print r.recvline()
print r.recvline()
