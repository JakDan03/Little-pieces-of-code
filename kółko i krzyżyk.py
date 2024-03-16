import numpy as np

# mechanizmy sprawdzające
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

# jak wybiera bot?
def bot_choice(board, bot_sign, player_sign, move):
    
    # wszystkie możliwe ruchy w danym posunięciu
    moves_available = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    
    # pierwszy ruch (środek albo róg)
    if move == 1:
        if np.random.choice([True, False], p=[.4, .6]): return (1, 1)
        else: return (np.random.choice([0, 2]), np.random.choice([0, 2]))
    
    # drugi ruch - jeśli się da to zawsze na środek, jeśli nie to zawsze w róg
    elif move == 2:
        if (1, 1) in moves_available: return (1, 1)
        else: return (np.random.choice([0, 2]), np.random.choice([0, 2]))
    
    # trzeci ruch - mamy szansę wygrać jeśli my środek i przeciwnik bok albo jeśli my róg i przeciwnik nie środek
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
        
        # jeśli gracz dobrze się obronił przed rogiem to w 40% przypadków postaw w rogu tak, by zagrozić podwójnym forkiem
        elif np.abs(bot_move[0] - bot_move[1]) != 1 and (player_move[0], player_move[1]) == (1, 1):
            if np.random.choice([True, False], p=[.4, .6]): return (np.abs(bot_move[0]-2),np.abs(bot_move[1]-2))
    
    # ostatni ruch - rusz się na jedyne dostępne pole
    elif move == 9: return moves_available[0]
    
    # w pozostałych ruchach postępuj zgodnie z zasadami (hierarchią) Newella i Simona
    else:
        
        # sprawdź czy nie masz wygranej
        res = if_win(board, moves_available, bot_sign)
        if res: return res
        
        # sprawdź czy przeciwnik nie ma wygranej
        res = if_win(board, moves_available, player_sign)
        if res: return res
                
        # sprawdź czy nie masz forka - ruch, którym atakujesz z dwóch stron
        res = if_fork(board, moves_available, bot_sign)
        if res: return res
        
        # jeśli gracz zagraża podwójnym forkiem w przypadku, gdzie gracz zaczął z rogam, to postaw z boku
        if move==4:
            main_diagonal = [board[j][j] for j in range(3)]
            opp_diagonal = [board[j][2-j] for j in range(3)]
            if main_diagonal == [player_sign, bot_sign, player_sign] or opp_diagonal == [player_sign, bot_sign, player_sign]:
                winning_moves = [(0, 1), (1, 0), (1, 2), (2, 1)]
                return winning_moves[np.random.randint(len(winning_moves))]
        
        # sprawdź czy przeciwnik nie ma forka
        res = if_fork(board, moves_available, player_sign)
        if res: return res
        
        # jeśli gracz pierwsze dwa ruchy zrobił na przeciwległych bokach to wygrywasz stawiając na rogu
        if move==4:
            row_shapes = [board[1][j] for j in range(3)]
            col_shapes = [board[j][1] for j in range(3)]
            if row_shapes == [player_sign, bot_sign, player_sign] or col_shapes == [player_sign, bot_sign, player_sign]:
                return (np.random.choice([0, 2]), np.random.choice([0, 2]))
            
    # jeśli nie masz nic w zanadrzu to rusz się losowo
    return moves_available[np.random.randint(len(moves_available))]

# mechanimz gry kółko i krzyżyk
def tictactoe(nick1, nick2, bot):
    # nazwy graczy
    nicks = [nick1, nick2]
    gracz1_shape = ""
    while gracz1_shape != "o" and gracz1_shape != "x":
        gracz1_shape = str(input(nick1 + ", wybierz kształt - prowadź 'o' lub 'x': "))
    gracz2_shape = "x" if gracz1_shape == "o" else "o"

    # kto zaczyna?
    los = np.random.randint(1, 3)

    # plansza
    board = [[' ' for i in range(3)] for j in range(3)]

    # funkcja drukująca planszę
    def print_board():
        for i in range(5):
            print(" " + board[int(i/2)][0] + " |" + " " + board[int(i/2)][1] + " |" + " " + board[int(i/2)][2] + " ") if i%2==0 else print(11*"–")

    # rozpoczęcie gry
    print("Rozpoczyna " + nicks[los-1] + "!")

    # rozgrywka
    turn = 1
    while turn <= 9:
        if turn != 1: print(nicks[los-1] + " - twoja kolej!")
        print_board()
        if bot and nicks[los-1] == "bot":
            row, col = bot_choice(board, gracz2_shape, gracz1_shape, turn)
        else:
            row, col = -1, -1
            while row not in [0, 1, 2] or col not in [0, 1, 2]:
                row = int(input("Wiersz: "))-1
                col = int(input("Kolumna: "))-1
        if board[row][col] != " ": 
            print("To pole jest już zajęte!")
            continue
        board[row][col] = gracz1_shape if los == 1 else gracz2_shape
        if turn >= 5:
            if [board[row][i] for i in range(3)] == [board[row][col] for i in range(3)] or [board[i][col] for i in range(3)] == [board[row][col] for i in range(3)]:
                print("Wygrywa " + nicks[los-1] + "!")
                print_board()
                break
            if row==col or np.abs(row-col) == 2:
                if [board[i][i] for i in range(3)] == [board[row][col] for i in range(3)] or [board[i][2-i] for i in range(3)] == [board[row][col] for i in range(3)]:
                    print("Wygrywa " + nicks[los-1] + "!")
                    print_board()
                    break
            if turn == 9:
                print("Remis!")
                print_board()
        turn+=1
        los = 1+los%2

# start gry
print("Witaj w grze kółko i krzyżyk! Jeśli chcesz zagrać ze znajomym napisz 'friendly', a jeśli chcesz zagrać z botem napisz 'bot'")
print("Niemniej i tak nie jesteś w stanie go ograć:p")
mode = ""
while mode != "friendly" and mode != "bot":
    mode = str(input("Tryb gry: "))
if mode == "bot":
    gracz_nick = str(input("Podaj swój nick: "))
    tictactoe(gracz_nick, "bot", bot=True)
else:
    gracz1 = str(input("Podaj nick gracza 1: "))
    gracz2 = str(input("Podaj nick gracza 2: "))
    tictactoe(gracz1, gracz2, bot=False)