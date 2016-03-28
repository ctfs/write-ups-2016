from pwn import *
import random

def parse_board(board):
    board=board.split("\n")[0:len(board.split("\n"))-1]
    for x in board:
        if "-+-" in x:
            board.remove(x)
    board = [x.split("|") for x in board]
    for x in range(3):
        for y in range(3):
            if "X" not in board[x][y] and "O" not in board[x][y]: board[x][y] = "-"
            if "X" in board[x][y]: board[x][y] = "X"
            if "O" in board[x][y]: board[x][y] = "O"
    return board

def assess_board1(board):
    # Always get the center:
    if board[1][1] == "-": return 4


    # Check To See if the game has been won:
    all_rows = ["".join(board[x]) for x in range(3)]
    for x in range(3):
        vert = "".join([row[x] for row in board])
        all_rows.append( vert)
    diag = [board[0][0],board[1][1],board[2][2]]
    all_rows.append( "".join(diag))
    diag = "".join([board[2][0],board[1][1],board[0][2]])
    all_rows .append( "".join(diag))
    if "XXX" in all_rows or "OOO" in all_rows:
        print "assess_board1"
        return "Game"
    draw = True
    for x in all_rows:
        if "-" in x:
            draw = False
    if draw: return "Tie"
    """ ASSESS FOR WIN FIRST """
    global win
    # Assess Rows:
    for x in range(3):
        row = board[x]
        row = "".join(row)
        if row == "O-O" or row == "OO-" or row == "-OO": 
            win = True
            return 3*x + row.index("-")

    # Asess columns:
    for x in range(3):
        row = [row[x] for row in board]
        row = "".join(row)
        if row == "O-O" or row == "OO-" or row == "-OO":
            win = True
            return 3*row.index("-") + x

    # Asess Diagnols:
    row = [board[0][0],board[1][1],board[2][2]]
    row = "".join(row)
    if row == "OO-": 
        win = True
        return 8
    if row == "O-O":
        win = True
        return 4
    if row == "-OO": 
        win = True
        return 0
    row = [board[2][0],board[1][1],board[0][2]]
    row = "".join(row)
    if row == "OO-":
        win = True
        return 2
    if row == "O-O":
        win = True
        return 4
    if row == "-OO":
        win = True
        return 6

    """ ASSESS FOR LOSS SECOND """

    # Assess Rows:
    for x in range(3):
        row = board[x]
        row = "".join(row)
        if row == "X-X" or row == "XX-" or row == "-XX": return 3*x + row.index("-")

    # Asess columns:
    for x in range(3):
        row = [row[x] for row in board]
        row = "".join(row)
        if row == "X-X" or row == "XX-" or row == "-XX": return 3*row.index("-") + x

    # Asess Diagnols:
    row = [board[0][0],board[1][1],board[2][2]]
    row = "".join(row)
    if row == "XX-": return 8
    if row == "X-X": return 4
    if row == "-XX": return 0
    row = [board[2][0],board[1][1],board[0][2]]
    row = "".join(row)
    if row == "XX-": return 2
    if row == "X-X": return 4
    if row == "-XX": return 6

    # The middle space will always be taken:
    # Generate a valid random move:
    x,y=1,1
    while board[x][y] != "-":
        x = random.randrange(0,3)
        y = random.randrange(0,3)
    return 3*x + y


def assess_board2(board):
    # Always get the center:
    if board[1][1] == "-": return 4


    # Check To See if the game has been won:
    all_rows = ["".join(board[x]) for x in range(3)]
    for x in range(3):
        vert = "".join([row[x] for row in board])
        all_rows.append( vert)
    diag = [board[0][0],board[1][1],board[2][2]]
    all_rows.append( "".join(diag))
    diag = "".join([board[2][0],board[1][1],board[0][2]])
    all_rows .append( "".join(diag))
    if "XXX" in all_rows or "OOO" in all_rows:
        #print r.recvline()
        print "assess_board2"
        return "Game"
    draw = True
    for x in all_rows:
        if "-" in x:
            draw = False
    if draw: return "Tie"
    """ ASSESS FOR WIN FIRST """
    global win
    # Assess Rows:
    for x in range(3):
        row = board[x]
        row = "".join(row)
        if row == "X-X" or row == "XX-" or row == "-XX":
            win = True
            return 3*x + row.index("-")

    # Asess columns:
    for x in range(3):
        row = [row[x] for row in board]
        row = "".join(row)
        if row == "X-X" or row == "XX-" or row == "-XX":
            win = True
            return 3*row.index("-") + x

    # Asess Diagnols:
    row = [board[0][0],board[1][1],board[2][2]]
    row = "".join(row)
    if row == "XX-":
        win = True
        return 8
    if row == "X-X":
        win = True
        return 4
    if row == "-XX":
        win = True
        return 0
    row = [board[2][0],board[1][1],board[0][2]]
    row = "".join(row)
    if row == "XX-":
        win = True
        return 2
    if row == "X-X":
        win = True
        return 4
    if row == "-XX":
        win = True
        return 6

    """ ASSESS FOR LOSS SECOND """

    # Assess Rows:
    for x in range(3):
        row = board[x]
        row = "".join(row)
        if row == "O-O" or row == "OO-" or row == "-OO": return 3*x + row.index("-")

    # Asess columns:
    for x in range(3):
        row = [row[x] for row in board]
        row = "".join(row)
        if row == "O-O" or row == "OO-" or row == "-OO": return 3*row.index("-") + x

    # Asess Diagnols:
    row = [board[0][0],board[1][1],board[2][2]]
    row = "".join(row)
    if row == "OO-": return 8
    if row == "O-O": return 4
    if row == "-OO": return 0
    row = [board[2][0],board[1][1],board[0][2]]
    row = "".join(row)
    if row == "OO-": return 2
    if row == "O-O": return 4
    if row == "-OO": return 6

    # The middle space will always be taken:
    # Generate a valid random move:
    x,y=1,1
    while board[x][y] != "-":
        x = random.randrange(0,3)
        y = random.randrange(0,3)
    return 3*x + y


HOST,PORT = "95.213.237.91",45679
r=remote(HOST,PORT)
print r.recvline()
print r.recvline()
r.sendline("T0pK3K")
print r.recvline()
r.recvuntil("Round")

for gamenum in range(500):
    print r.recvline()
    game = r.recvline()
    print game
    win=False
    for move in range(5):
        board=""
        for x in range(5): 
            board += r.recvline()
        board_list = parse_board(board)
        if gamenum%2==0: send = (assess_board1(board_list))
        elif gamenum%2==1: send = (assess_board2(board_list))
        r.recvline() 
        if  send=="Game":
            print "Loss"
            break
        elif send == "Tie":
            print "Tie"
            break
        r.sendline(str(send))
        if win:
            print "WIN"
            break
print r.recvline()
print r.recvline()
print r.recvline()
