import numpy as np
import random

debug = False
COLUMNS = 7
ROWS = 6
global difficulty
difficulty = 10
gameselect = 0


def difChoose():
    global dHits
    global tHits
    global rHits
    global lHits
    global vHits

def newgame():
    board = np.zeros((ROWS,COLUMNS)) 
    return board

def column_check(c = 0):
    i = 0
    Error = 0
    tempB = True
    for i in range(6):
        try:
            if board[i,c] != 0:  # If the current cell is not 0
                if i == 0:  # Special case for the first row
                    tempB = False
                    return 8  # Return 8 if the first row is non-zero, for an error message
                else:
                    i -= 1
                    tempB = False
                    return i  # Return the row index where the first non-zero entry is found
        except IndexError:
            Error += 1
    return 5 


def turn_input(turn):
    move = 0
    temp = True
    while temp:
        try:
            move = int(input("\nP" + str(turn) + ": Choose what column to place the checker (1-7): "))
            if 1 <= move <= 7:
                move -= 1
                if column_check(move) == 8:
                    print("Column is full, please choose another. ")
                else:
                    return move
            else:
                print("Please input an integer between the designated values (1-7): ")  # Exit the loop if input is a valid integer

        except ValueError:
            print("Invalid input. Please enter an integer.")

def move_check(c = 0, turn = 1):
    lrow = column_check(c)
    if turn == 1:
        board[(lrow), c] = 1
    else:
        board[(lrow), c] = 2

def win_check(turn = 1):

    # Check horizontal rows
    for r in range(ROWS):
        for c in range(COLUMNS - 3):  # Check only up to 3 positions before the last column
            if board[r,c] == turn:
                if board[r,c] == board[r,c + 1] == board[r,c + 2] == board[r,c + 3]:
                    return True

    # Check vertical columns
    for c in range(COLUMNS):
        for r in range(ROWS - 3):  # Check only up to 3 positions before the last row
            if board[r,c] == turn:
                if board[r,c] == board[r + 1,c] == board[r + 2,c] == board[r + 3,c]:
                    return True

    # Check diagonal (top-left to bottom-right)
    for r in range(ROWS - 3):  # Ensure we have enough rows for a diagonal
        for c in range(COLUMNS - 3):  # Ensure we have enough columns for a diagonal
            if board[r,c] == turn:
                if board[r,c] == board[r + 1,c + 1] == board[r + 2,c + 2] == board[r + 3,c + 3]:
                    return True

    # Check diagonal (top-right to bottom-left)
    for r in range(ROWS - 3):  # Ensure we have enough rows for a diagonal
        for c in range(3, COLUMNS):  # Ensure we have enough columns for a diagonal
            if board[r,c] == turn:
                if board[r,c] == board[r + 1,c - 1] == board[r + 2,c - 2] == board[r + 3,c - 3]:
                    return True

    # No 4 identical values in a row, column, or diagonal
    return False



def calc_weight(r = 0, c = 0, trigger = False, turn = 2):
    

    if r <= 2:
        vRng = 4
    else:
        vRng = (ROWS - 1) - r

    if c == 3:
        lRng = 4
        rRng = 4
    elif c < 3:
        lRng = c + 1
        rRng = 4
    elif c > 3:
        lRng = 4
        rRng = (COLUMNS - 1) - c
    
    
    tWeight = 0

    if debug:
        print("C = " + str(c + 1) + " | R = " + str(r + 1) + " | rRng = " + str(rRng) + " | lRng = " + str(lRng) + " | vRng = " + str(vRng))

    if r < 0 or r >= ROWS or c < 0 or c >= COLUMNS:
        return tWeight

    consec = 0
    global extra_hits
    extra_hits = 0
    for temp in range(1, rRng):  # Iterate through each column
        if board[r, c + temp] == turn:
            consec += 1
            if difficulty == 1:
                tWeight += 1    
            elif difficulty == 2:
                tWeight += 2
            elif difficulty == 3:
                tWeight += 3
            elif difficulty == 4:
                tWeight += 5
            elif difficulty >= 5:
                tWeight += 10
    if consec == 2:
        extra_hits += 5 * difficulty * consec
    elif consec == 3:
        extra_hits += 15 * difficulty * consec
            
    
    consec = 0
    for temp in range(1, lRng):  # Start from 1 to avoid checking the current column
        if c - temp >= 0:  # Ensure we don't go out of bounds
            if board[r, c - temp] == turn:  # Check if the piece is of the opponent's type (value 2)
                consec += 1
                if difficulty == 1:
                    tWeight += 1
                elif difficulty == 2:
                    tWeight += 2
                elif difficulty == 3:
                    tWeight += 3
                elif difficulty == 4:
                    extra_hits += 1
                    tWeight += 5
                elif difficulty >= 5:
                    extra_hits += 2
                    tWeight += 10
    if consec == 2:
        extra_hits += 5 * difficulty * consec
    elif consec == 3:
        extra_hits += 15 * difficulty * consec

    
    consec = 0
    if vRng == 1:
        vRng = 2  # Ensure vRng is at least 2 for the range to iterate

    for temp in range(vRng):  # Start from 0 to vRng-1 (inclusive)
        if 0 <= r + temp < len(board) and 0 <= c < len(board[0]):  # Check for valid indices
            if board[r + temp, c] == turn:
                consec += 1
                if difficulty == 1:
                    tWeight += 1
                elif difficulty == 2:
                    tWeight += 2
                elif difficulty == 3:
                    tWeight += 3
                elif difficulty == 4:
                    extra_hits += 1
                    tWeight += 5
                elif difficulty >= 5:
                    extra_hits += 2
                    tWeight += 10
    if consec == 2:
        extra_hits += 5 * difficulty * consec
    elif consec == 3:
        extra_hits += 15 * difficulty * consec
    
    consec = 0
    # 1. Check diagonal Top-left to Bottom-right (↖ → ↘)
    for temp in range(1, vRng + 1):  # Checking downward diagonally
        if r + temp < ROWS and c - temp >= 0:  # Ensure within bounds
            if board[r + temp, c - temp] == turn:  # Check opponent's piece
                consec += 1
                if difficulty == 1:
                    tWeight += 1
                elif difficulty == 2:
                    tWeight += 2
                elif difficulty == 3:
                    tWeight += 3
                elif difficulty == 4:
                    extra_hits += 1
                    tWeight += 5
                elif difficulty >= 5:
                    extra_hits += 2
                    tWeight += 10
    if consec == 2:
        extra_hits += 5 * difficulty * consec
    elif consec == 3:
        extra_hits += 15 * difficulty * consec    

    consec = 0
    for temp in range(1, vRng + 1):  # Checking upward diagonally
        if r - temp >= 0 and c + temp < COLUMNS:  # Ensure within bounds
            if board[r - temp, c + temp] == turn:  # Check opponent's piece
                consec += 1
                if difficulty == 1:
                    tWeight += 1
                elif difficulty == 2:
                    tWeight += 2
                elif difficulty == 3:
                    tWeight += 3
                elif difficulty == 4:
                    extra_hits += 1
                    tWeight += 5
                elif difficulty >= 5:
                    extra_hits += 2
                    tWeight += 10
    if consec == 2:
        extra_hits += 5 * difficulty * consec
    elif consec == 3:
        extra_hits += 15 * difficulty * consec    

    consec = 0
    # 2. Check diagonal Top-right to Bottom-left (↗ → ↙)
    for temp in range(1, vRng + 1):  # Checking downward diagonally
        if r + temp < ROWS and c + temp < COLUMNS:  # Ensure within bounds
            if board[r + temp, c + temp] == turn:  # Check opponent's piece
                consec += 1
                if difficulty == 1:
                    tWeight += 1
                elif difficulty == 2:
                    tWeight += 2
                elif difficulty == 3:
                    tWeight += 3
                elif difficulty == 4:
                    extra_hits += 1
                    tWeight += 5
                elif difficulty >= 5:
                    extra_hits += 2
                    tWeight += 10
        
    if consec == 2:
        extra_hits += 5 * difficulty * consec
    elif consec == 3:
        extra_hits += 15 * difficulty * consec        

    consec = 0
    for temp in range(1, vRng + 1):  # Checking upward diagonally
        if r - temp >= 0 and c - temp >= 0:  # Ensure within bounds
            if board[r - temp, c - temp] == turn:  # Check opponent's piece
                consec += 1
                if difficulty == 1:
                    tWeight += 1
                elif difficulty == 2:
                    tWeight += 2
                elif difficulty == 3:
                    tWeight += 3
                elif difficulty == 4:
                    tWeight += 5
                elif difficulty >= 5:
                    tWeight += 10

    if consec == 2:
        extra_hits += 5 * difficulty * consec
    elif consec == 3:
        extra_hits += 15 * difficulty * consec    
            

    

    if trigger:
        return extra_hits
    else:
        return tWeight


def move_weight(turn):
    column_weights = [0] * COLUMNS

    c0r = column_check(0)
    c1r = column_check(1)
    c2r = column_check(2)
    c3r = column_check(3)
    c4r = column_check(4)
    c5r = column_check(5)
    c6r = column_check(6)
    column_places = [c0r,c1r,c2r,c3r,c4r,c5r,c6r]

    x = 0
    
    for x in range(len(column_places)):
        temp_weight = 0
        temp_weight += calc_weight(column_places[x], x)
        column_weights[x] = temp_weight
    
    tempc = -1
    visCol = 0
    
    while tempc < 6:
        tempc+=1
        visCol+=1
        if debug:
            print("Col: " + str(visCol) + "; W = " + str(calc_weight(column_check(tempc), tempc, True)) + " | ")
        
        column_weights[x] = (calc_weight(column_check(tempc), tempc) + calc_weight(column_check(tempc), tempc, True) + calc_weight(column_check(tempc), tempc, True, 1))
    
        

    
    return column_weights

def ai_turn():
    movelist = np.array([4])
    weights = move_weight(2)
    for x in range(6):
        for each in range(weights[x] + extra_hits):
            movelist = np.append(movelist, x)

    if len(movelist) > 1:
        movelist = np.delete(movelist, 0)
    aselect = random.randint(0,len(movelist))
    
    checker = True
    while checker:
        try:
            aselect = random.randint(0,len(movelist))
            if column_check(movelist[aselect]) == 8:
                aselect = random.randint(0,len(movelist))

            if column_check(movelist[aselect]) <= 5:
                checker = False
                print("Ai chose: " + str(movelist[aselect]))
        except IndexError:
            print("Ai picked a bad one, retrying...")

    if debug:
        print(movelist)
        print(aselect)

    return movelist[aselect]

board = newgame()
difChoose()

gameselect = input("\nEnter the number of players (1 = Multiplayer, 2 = Singleplayer): ")
while gameselect != "1" and gameselect != "2":
    gameselect = input("\nEnter the number of players (1 = Multiplayer, 2 = Singleplayer): ")


confirm = input("\nYou selected '" + gameselect + "' confirm? (Y or N): ")
confirm = confirm.upper()
while confirm != "Y" and confirm != "N":
    confirm = input("\nYou selected '" + gameselect + "' confirm? (Y or N): ")
    confirm = confirm.upper()

while True:
    try:
        difficulty_input = input("\nEnter the difficulty of AI (recommended: 1-10 | Challenge (10-20)): ")
        difficulty = int(difficulty_input)  # Attempt to convert input to integer
        if 1 <= difficulty <= 20:
            break
        else:
            print("Please input an integer between 1 and 20.")

    except ValueError:
        print("Invalid input. Please enter an integer.") 


game_state = False
turn = 1
winner = 0
while game_state == False:
    if gameselect == "1":
        # Game will ask for the first person to choose where they place their checker
        print(board)
        if turn == 1:
            move = turn_input(1)
            move_check(move, 1)
            if win_check(1):
                winner = 1
                game_state = True
            else:
                turn = 2

            #while move != "1" and move != "2" and move != "3" and move != "4" and move != "5" and move != "6" and move != "7"
        elif turn == 2: # Now for second player
            move = turn_input(2)
            move_check(move, 2)
            if win_check(2):
                winner = 2
                game_state = True
            else:
                turn = 1
    elif gameselect == "2":
        # Game will ask for the first person to choose where they place their checker
        print(board)
        if turn == 1:
            move = turn_input(1)
            move_check(move, 1)
            if win_check(1):
                winner = 1
                game_state = True
            else:
                turn = 2

            #while move != "1" and move != "2" and move != "3" and move != "4" and move != "5" and move != "6" and move != "7"
        elif turn == 2: # Now for second player

            if debug:
                print(move_weight(2))

            move = ai_turn()
            move_check(move, 2)
            if debug:
                print(move_weight(2))

            

            if win_check(2):
                winner = 2
                game_state = True
            else:
                turn = 1

if game_state:
    print(board)
    print("The winner is player " + str(winner) + "! Congratulations for winning!")
    


        