import numpy as np

# definitions of winning and forking (used by a bot)
def if_win(board, moves_available, sign):
    for i in range(len(moves_available)):
        if [board[moves_available[i][0]][j] for j in range(3) if j != moves_available[i][1]] == [sign for i in range(2)] or [board[j][moves_available[i][1]] for j in range(3) if j != moves_available[i][0]] == [sign for i in range(2)]:
            return moves_available[i]
        if moves_available[i][0]==moves_available[i][1]:
            if [board[j][j] for j in range(3) if j != moves_available[i][0]] == [sign for i in range(2)]:
                return moves_available[i]
        if np.abs(moves_available[i][0]-moves_available[i][1]) == 2:
            if [board[j][2-j] for j in range(3) if j != moves_available[i][0]] == [sign for i in range(2)]:
                return moves_available[i]
    return False

def if_fork(board, moves_available, sign):
    for i in range(len(moves_available)):
        row_shapes = [board[moves_available[i][0]][j] for j in range(3) if j != moves_available[i][1]]
        col_shapes = [board[j][moves_available[i][1]] for j in range(3) if j != moves_available[i][0]]
        if moves_available[i] == (1, 1):
            main_diagonal = [board[j][j] for j in range(3) if j != moves_available[i][0]]
            opp_diagonal = [board[j][2-j] for j in range(3) if j != moves_available[i][0]]
            check_lines = [row_shapes, col_shapes, main_diagonal, opp_diagonal]
        elif np.abs(moves_available[i][0]-moves_available[i][1]) != 1:
            diagonal = [board[j][j] for j in range(3) if j != moves_available[i][0]] if moves_available[i][0]==moves_available[i][1] else [board[j][2-j] for j in range(3) if j != moves_available[i][0]]
            check_lines = [row_shapes, col_shapes, diagonal]
        else: check_lines = [row_shapes, col_shapes]
        checks = 0
        for j in range(len(check_lines)):
            if sign in check_lines[j] and " " in check_lines[j]: checks += 1
        if checks > 1: return moves_available[i]
    return False

# how our bot is making a choice?
def bot_choice(board, bot_sign, player_sign, move):
    
    # all available moves
    moves_available = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    
    # first move - middle (60% chance) or corner (40% chance)
    if move == 1:
        if np.random.choice([True, False], p=[.6, .4]): return (1, 1)
        else: return (np.random.choice([0, 2]), np.random.choice([0, 2]))
    
    # second move - if it's possible - move to a middle, if not - always to a corner
    elif move == 2:
        if (1, 1) in moves_available: return (1, 1)
        else: return (np.random.choice([0, 2]), np.random.choice([0, 2]))
    
    # third move - bot wins if bot middle and opponent side or if bot corner and opponent not middle
    elif move == 3:
        moves_unavailable = [(i, j, board[i][j]) for i in range(3) for j in range(3) if (i, j) not in moves_available]
        bot_move = moves_unavailable[0] if moves_unavailable[0][2] == bot_sign else moves_unavailable[1]
        moves_unavailable.remove(bot_move)
        player_move = moves_unavailable[0]
        if (bot_move[0], bot_move[1]) == (1, 1) and np.abs(player_move[0] - player_move[1]) == 1:
            return (np.random.choice([0, 2]), np.random.choice([0, 2]))
        elif np.abs(bot_move[0] - bot_move[1]) != 1 and (bot_move[0], bot_move[1]) != (1, 1) and (player_move[0], player_move[1]) != (1, 1):
            if np.abs(player_move[0] - player_move[1]) == 1:
                winning_moves = [(1, 1)]
                corners = [(i, j) for i in range(0, 3, 2) for j in range(0, 3, 2) if (i, j) in moves_available]
                if np.abs(bot_move[0] - bot_move[1]) == 2 and (bot_move[1], bot_move[0]) in corners: corners.remove((bot_move[1], bot_move[0]))
                elif bot_move[0] == bot_move[1] and (np.abs(bot_move[0]-2),np.abs(bot_move[1]-2)) in corners: corners.remove((np.abs(bot_move[0]-2),np.abs(bot_move[1]-2)))
                for i in range(len(corners)):
                    if not((player_move[0] == bot_move[0] == corners[i][0]) or (player_move[1] == bot_move[1] == corners[i][1])):
                        winning_moves.append(corners[i])
            else:
                winning_moves = [moves_available[i] for i in range(len(moves_available)) if np.abs(moves_available[i][0] - moves_available[i][1]) != 1 and moves_available[i] != (1, 1)]
                winning_moves = [winning_moves[i] for i in range(len(winning_moves)) if (winning_moves[i][0] == bot_move[0]) or (winning_moves[i][1] == bot_move[1])]
            return winning_moves[np.random.randint(len(winning_moves))]
        
        # if player defend correctly against a corner, 40% of the time corner which may end up in a double fork for a bot
        elif np.abs(bot_move[0] - bot_move[1]) != 1 and (player_move[0], player_move[1]) == (1, 1):
            if np.random.choice([True, False], p=[.4, .6]): return (np.abs(bot_move[0]-2),np.abs(bot_move[1]-2))
    
    # last move - play the only available one
    elif move == 9: return moves_available[0]
    
    # else - follow Newell and Simon strategy
    else:
        
        # check if you can win
        res = if_win(board, moves_available, bot_sign)
        if res: return res
        
        # chech if the opponent can win and if he can - block him
        res = if_win(board, moves_available, player_sign)
        if res: return res
                
        # chech if bot has a fork - a double attack
        res = if_fork(board, moves_available, bot_sign)
        if res: return res
        
        # if the opponent may double fork (after his first corner move), bot has to play side
        if move==4:
            main_diagonal = [board[j][j] for j in range(3)]
            opp_diagonal = [board[j][2-j] for j in range(3)]
            if main_diagonal == [player_sign, bot_sign, player_sign] or opp_diagonal == [player_sign, bot_sign, player_sign]:
                winning_moves = [(0, 1), (1, 0), (1, 2), (2, 1)]
                return winning_moves[np.random.randint(len(winning_moves))]
        
        # check if player has a fork
        res = if_fork(board, moves_available, player_sign)
        if res: return res
        
        # if player make first two moves on facing sides, bot plays a corner and win
        if move==4:
            row_shapes = [board[1][j] for j in range(3)]
            col_shapes = [board[j][1] for j in range(3)]
            if row_shapes == [player_sign, bot_sign, player_sign] or col_shapes == [player_sign, bot_sign, player_sign]:
                return (np.random.choice([0, 2]), np.random.choice([0, 2]))
            
    # in any other cases - move randomly
    return moves_available[np.random.randint(len(moves_available))]

# tic tac toe mechanism
def tictactoe(nick1, nick2, bot):
    
    # players' names
    nicks = [nick1, nick2]
    player1_shape = ""
    while player1_shape != "o" and player1_shape != "x":
        player1_shape = str(input(nick1 + ", choose player one shape - insert 'o' or 'x': "))
    player2_shape = "x" if player1_shape == "o" else "o"

    # who starts?
    rand = np.random.randint(1, 3)

    # board
    board = [[' ' for i in range(3)] for j in range(3)]

    # function printing a board
    def print_board():
        for i in range(5):
            print(" " + board[int(i/2)][0] + " |" + " " + board[int(i/2)][1] + " |" + " " + board[int(i/2)][2] + " ") if i%2==0 else print(11*"–")

    # start of the game
    print(nicks[rand-1] + " begins!")

    # gameplay
    turn = 1
    while turn <= 9:
        if turn != 1: print(nicks[rand-1] + " - your turn!")
        print_board()
        if bot and nicks[rand-1] == "bot":
            row, col = bot_choice(board, player2_shape, player1_shape, turn)
        else:
            row, col = -1, -1
            while row not in [0, 1, 2] or col not in [0, 1, 2]:
                row = int(input("Row: "))-1
                col = int(input("Column: "))-1
        if board[row][col] != " ": 
            print("Choose another place!")
            continue
        board[row][col] = player1_shape if rand == 1 else player2_shape
        if turn >= 5:
            if [board[row][i] for i in range(3)] == [board[row][col] for i in range(3)] or [board[i][col] for i in range(3)] == [board[row][col] for i in range(3)]:
                print(nicks[rand-1] + " wins!")
                print_board()
                break
            if row==col or np.abs(row-col) == 2:
                if [board[i][i] for i in range(3)] == [board[row][col] for i in range(3)] or [board[i][2-i] for i in range(3)] == [board[row][col] for i in range(3)]:
                    print(nicks[rand-1] + " wins!")
                    print_board()
                    break
            if turn == 9:
                print("Tie!")
                print_board()
        turn+=1
        rand = 1+rand%2

# game activator
print("Welcome to tic tac toe game! If you want to play with a friend, type 'friendly' and if you want to try a bot, write 'bot'")
print("But it's actually impossible to beat him!")
print("Unless...")
mode = ""
while mode != "friendly" and mode != "bot":
    mode = str(input("Choose a gamemode: "))
if mode == "bot":
    player_nick = str(input("Enter your name: "))
    tictactoe(player_nick, "bot", bot=True)
else:
    player1 = str(input("Enter player 1 name: "))
    player2 = str(input("Enter player 2 name: "))
    tictactoe(player1, player2, bot=False)
