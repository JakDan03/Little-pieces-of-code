# find every place attacked by the opponent
def under_attack(board, number_opp, king_find=True, knight_find=True, rook_find=True):
    attacked_places = []

    # white pieces
    if number_opp == 1:

        # king
        if king_find:
            for i in [board.index("♔") - 1, board.index("♔") + 1]:
                if i in range(8):
                    if board[i] != "♘" and board[i] != "♖":
                        attacked_places.append(i)
        # knight
        if knight_find:
            if "♘" in board:
                for i in [board.index("♘") - 2, board.index("♘") + 2]:
                    if i in range(8):
                        if board[i] != "♔" and board[i] != "♖":
                            attacked_places.append(i)
        # rook
        if rook_find:
            if "♖" in board:
                # left side
                pos = board.index("♖") - 1
                while board[pos] == " ":
                    attacked_places.append(pos)
                    pos -= 1
                if board[pos] != "♘" and board[pos] != "♔":
                    attacked_places.append(pos)
                # right side
                pos = board.index("♖") + 1
                while board[pos] == " ":
                    attacked_places.append(pos)
                    pos += 1
                if board[pos] != "♘" and board[pos] != "♔":
                    attacked_places.append(pos)

    # black pieces
    else:
        # king
        if king_find:
            for i in [board.index("♚") - 1, board.index("♚") + 1]:
                if i in range(8):
                    if board[i] != "♞" and board[i] != "♜":
                        attacked_places.append(i)
        # knight
        if knight_find:
            if "♞" in board:
                for i in [board.index("♞") - 2, board.index("♞") + 2]:
                    if i in range(8):
                        if board[i] != "♚" and board[i] != "♜":
                            attacked_places.append(i)
        # rook
        if rook_find:
            if "♜" in board:
                # left side
                pos = board.index("♜") - 1
                while board[pos] == " ":
                    attacked_places.append(pos)
                    pos -= 1
                if board[pos] != "♞" and board[pos] != "♚":
                    attacked_places.append(pos)
                # right side
                pos = board.index("♜") + 1
                while board[pos] == " ":
                    attacked_places.append(pos)
                    pos += 1
                if board[pos] != "♞" and board[pos] != "♚":
                    attacked_places.append(pos)

    return attacked_places


# what choices bot has?
def bot_choices(board, number, check=False):
    choices = []

    # white pieces
    if number == 1:

        # king
        for i in [board.index("♔") - 1, board.index("♔") + 1]:
            if i in range(7):
                if board[i] != "♘" and board[i] != "♖":
                    hyp_board = board[:]
                    hyp_board[hyp_board.index("♔")] = " "
                    hyp_board[i] = "♔"
                    attacked = under_attack(hyp_board, 1 + number % 2)
                    if i not in attacked:
                        choices.append(("♔", i))
        # knight
        if "♘" in board:
            for i in [board.index("♘") - 2, board.index("♘") + 2]:
                if i in range(7):
                    if board[i] != "♔" and board[i] != "♖":
                        hyp_board = board[:]
                        hyp_board[hyp_board.index("♘")] = " "
                        hyp_board[i] = "♘"
                        if hyp_board.index("♔") not in under_attack(hyp_board, 1 + number % 2, king_find=False,
                                                                    knight_find=False):
                            choices.append(("♘", i))
        # rook
        if "♖" in board:
            # left side
            pos = board.index("♖") - 1
            while board[pos] == " ":
                choices.append(("♖", pos))
                pos -= 1
            if board[pos] != "♘" and board[pos] != "♔":
                choices.append(("♖", pos))
            # right side
            pos = board.index("♖") + 1
            while board[pos] == " ":
                choices.append(("♖", pos))
                pos += 1
            if board[pos] != "♘" and board[pos] != "♔":
                choices.append(("♖", pos))

        # if there is a check, verify your moves if they prevent from this check
        if check:
            l = len(choices)
            for i in range(l):
                piece_hyp, move_hyp = choices[i][0], choices[i][1]
                hyp_board = board[:]
                hyp_board[hyp_board.index(piece_hyp)] = " "
                hyp_board[move_hyp] = piece_hyp
                if hyp_board.index("♔") not in under_attack(hyp_board, 1 + number % 2, king_find=False):
                    choices.append(choices[i])
            choices = choices[l:] if len(choices) != l else []

    # black pieces
    else:

        # king
        for i in [board.index("♚") - 1, board.index("♚") + 1]:
            if i in range(8):
                if board[i] != "♞" and board[i] != "♜":
                    hyp_board = board[:]
                    hyp_board[hyp_board.index("♚")] = " "
                    hyp_board[i] = "♚"
                    attacked = under_attack(hyp_board, 1 + number % 2)
                    if i not in attacked:
                        choices.append(("♚", i))
        # knight
        if "♞" in board:
            for i in [board.index("♞") - 2, board.index("♞") + 2]:
                if i in range(8):
                    if board[i] != "♚" and board[i] != "♜":
                        hyp_board = board[:]
                        hyp_board[hyp_board.index("♞")] = " "
                        hyp_board[i] = "♞"
                        if hyp_board.index("♚") not in under_attack(hyp_board, 1 + number % 2, king_find=False,
                                                                    knight_find=False):
                            choices.append(("♞", i))
        # rook
        if "♜" in board:
            # left side
            pos = board.index("♜") - 1
            while board[pos] == " ":
                choices.append(("♜", pos))
                pos -= 1
            if board[pos] != "♞" and board[pos] != "♚":
                choices.append(("♜", pos))
            # right side
            pos = board.index("♜") + 1
            while board[pos] == " ":
                choices.append(("♜", pos))
                pos += 1
            if board[pos] != "♞" and board[pos] != "♚":
                choices.append(("♜", pos))

        # if there is a check, verify your moves if they prevent from this check
        if check:
            l = len(choices)
            for i in range(l):
                piece_hyp, move_hyp = choices[i][0], choices[i][1]
                hyp_board = board[:]
                hyp_board[hyp_board.index(piece_hyp)] = " "
                hyp_board[move_hyp] = piece_hyp
                if hyp_board.index("♚") not in under_attack(hyp_board, 1 + number % 2, king_find=False):
                    choices.append(choices[i])
            choices = choices[l:] if len(choices) != l else []

    return choices

# board printing
def board_print(board):
    print("-" * (40 - board.count(" ")))
    l = ""
    for i in range(8): l += "| " + board[i] + " "
    l += "|"
    print(l)
    print("-" * (40 - board.count(" ")))


# chess 1d gameplay - player vs player
def chess1d():
    # starting board
    board_play = ["♔", "♘", "♖", " ", " ", "♜", "♞", "♚"]
    board_print(board_play)

    # white always goes first
    moving_player = 1
    check = False
    board_states = []

    # the game
    while True:

        # inform about checks
        if check: print("Check!")

        # stalemate - player has no moves and there is no check
        if bot_choices(board_play, moving_player) == [] and not check:
            print("Stalemate!")
            print("White has no moves") if moving_player == 1 else print("Black has no moves")
            break

        # if some position repeats three times during a game - we have a stalemate
        if board_states.count(board_play) == 3:
            print("Stalemate!")
            print("The same position has repeated three times")
            break

        # if the only pieces left are kings, it's definitely a draw
        if board_play.count(" ") == 6:
            print("Stalemate!")
            print("The are only kings on the board")
            break

        # who is moving
        print("White moves") if moving_player == 1 else print("Black moves")

        # taking a move from the player
        move, place = "", -1
        while move not in ["k", "n", "r"] or place not in range(8):
            move = str(input("King - k, knight - n, rook - r: "))
            place = int(input("Which position (1-8): ")) - 1

        # converting the move into a piece
        if moving_player == 1:
            if move == "k":
                piece = "♔"
            elif move == "n":
                piece = "♘"
            elif move == "r":
                piece = "♖"
        else:
            if move == "k":
                piece = "♚"
            elif move == "n":
                piece = "♞"
            elif move == "r":
                piece = "♜"

        # combine move and place in a tuple and find if the move is legal and if it is - make it
        move_and_place = (piece, place)
        if move_and_place in bot_choices(board_play, moving_player, check=check):
            board_play[board_play.index(piece)] = " "
            board_play[place] = piece
            board_print(board_play)
            board_states.append(board_play[:])
            # checks
            king = "♚" if moving_player == 1 else "♔"
            if board_play.index(king) in under_attack(board_play, moving_player, king_find=False):
                check = True

                # checkmate
                if bot_choices(board_play, 1 + moving_player % 2, check=check) == []:
                    print("Checkmate!")
                    print("White wins!") if moving_player == 1 else print("Black wins!")
                    break

            # if there is no more check - deny it
            else:
                check = False
            moving_player = 1 + moving_player % 2

        # if the move is illegal, inform that the move is illegal
        else:
            print("This move is unavailable for you!")
            board_print(board_play)

chess1d()