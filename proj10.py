#######################################################################
# Project 10
# this project is the game Nine Men's Morris
# Two player game
# players take alternating turns
#goal of the game is to get three in a row or column(mill)
#every time a player gets a mill they can remove opponents piece
# once there are 18 pieces on the board phase 2 begins
#in phase 2 players can move their own pieces to open spaces
#game is won when opponent has three or less pieces
######################################################################

import NMM  # This is necessary for the project
import functools

BANNER = """

    __        _____ _   _ _   _ _____ ____  _ _ _
    \ \      / /_ _| \ | | \ | | ____|  _ \| | | |
     \ \ /\ / / | ||  \| |  \| |  _| | |_) | | | |
      \ V  V /  | || |\  | |\  | |___|  _ <|_|_|_|
       \_/\_/  |___|_| \_|_| \_|_____|_| \_(_|_|_)

"""

RULES = """

  _   _ _              __  __            _       __  __                 _
 | \ | (_)_ __   ___  |  \/  | ___ _ __ ( )___  |  \/  | ___  _ __ _ __(_)___
 |  \| | | '_ \ / _ \ | |\/| |/ _ \ '_ \|// __| | |\/| |/ _ \| '__| '__| / __|
 | |\  | | | | |  __/ | |  | |  __/ | | | \__ \ | |  | | (_) | |  | |  | \__ \
 |_| \_|_|_| |_|\___| |_|  |_|\___|_| |_| |___/ |_|  |_|\___/|_|  |_|  |_|___/

    The game is played on a grid where each intersection is a "point" and
    three points in a row is called a "mill". Each player has 9 pieces and
    in Phase 1 the players take turns placing their pieces on the board to 
    make mills. When a mill (or mills) is made one opponent's piece can be 
    removed from play. In Phase 2 play continues by moving pieces to 
    adjacent points. 
    
    The game is ends when a player (the loser) has less than three 
    pieces on the board.

"""

MENU = """

    Game commands (first character is a letter, second is a digit):
    
    xx        Place piece at point xx (only valid during Phase 1 of game)
    xx yy     Move piece from point xx to point yy (only valid during Phase 2)
    R         Restart the game
    H         Display this menu of commands
    Q         Quit the game
    
"""
def comparePointsByNumbers(point1, point2):
    '''this function takes two points and returns numbers
    in order to assist with sorting'''
    point1_letter = point1[0]
    point1_number = point1[1]
    point2_letter = point2[0]
    point2_number = point2[1]
    if point1_number > point2_number:
        return 1
    elif point1_number < point2_number:
        return -1
    else:
        if point1_letter > point2_letter:
            return 1
        elif point1_letter < point2_letter:
            return -1
        else:
            return 0

def count_mills(board, player):
    """
        counts the number of mills in the board for given player.
        Takes board and player and returns a count of mills.
    """
    boarddict = board.points  # dictionary containing all pieces and players in board
    MILLS = [["a1", "d1", "g1"], ["b2", "d2", "f2"],
             ["c3", "d3", "e3"], ["a4", "b4", "c4"], ["e4", "f4", "g4"],
             ["c5", "d5", "e5"], ["b6", "d6", "f6"], ["a7", "d7", "g7"],
             ["a1", "a4", "a7"], ["b2", "b4", "b6"], ["c3", "c4", "c5"],
             ["d1", "d2", "d3"], ["d5", "d6", "d7"], ["e3", "e4", "e5"],
             ["f2", "f4", "f6"],
             ["g1", "g4", "g7"]]  # list of list of every possible mill
    playervalues = []  # initialize player values list
    count = 0  # initialize count
    count2 = 0  # initialize second count
    millcount = 0  # initialize mill count
    newlist = []  # initialize first newlist
    newlist2 = []  # initialize second new list
    newlist3 = []  # initialize third new list
    # for loop adding pieces associated with player to a list
    for k, v in boarddict.items():
        if v == player:
            playervalues.append(k)
    newlist_sorted_by_letter = sorted(playervalues)  # sorted list of player values
    newlist_sorted_by_numbers = sorted(playervalues, key=functools.cmp_to_key(comparePointsByNumbers))
    while count < len(playervalues) - 2:
        newlist.append(
            newlist_sorted_by_numbers[count:count + 3])  # add list of three to newlist
        count += 1  # increse count by 3

    while count2 < len(playervalues) - 2:
        newlist2.append(
            newlist_sorted_by_letter[count2:count2 + 3])  # add list of three to newlist2
        count2 += 1  # decrease count by 3
    # go through each list in new list
    for l in newlist:
        if l in MILLS and l not in newlist3:
            millcount += 1  # add one of each mill to newlist3 and count
            newlist3.append(l)
    for l in newlist2:
        if l in MILLS and l not in newlist3:
            millcount += 1
            newlist3.append(l)

    return millcount  # return mill count


def place_piece_and_remove_opponents(board, player, destination):
    """
        Takes board, player, and piece destination. Places the piece
        if it is valid and removes the opponents piece if a mill is formed.
    """
    boarddict = board.points  # dictionary of all the points in the board
    alllocations = []  # initialize list of all locations on the board
    openlocations = []  # initialize list of all open locations on the board
    initial_count = count_mills(board,
                                player)  # call count mills function to count mills before adding piece
    not_in_mills_before = set(points_not_in_mills(board, player))
    # for loop going through all items and player names in board
    for k, v in boarddict.items():
        alllocations.append(k)  # add location to list
        if v == ' ':  # if a piece is open
            openlocations.append(k)  # add to open locations list
            # if destination is available then assign player to it
    if destination in openlocations:
        boarddict[destination] = player
    else:
        raise RuntimeError('Invalid command: Destination point already taken')

    second_count = count_mills(board,
                               player)  # call count mills again after placing piece
    not_in_mills_after = set(points_not_in_mills(board, player))
    # if more mills than there were before
    if second_count > initial_count or\
            (second_count == initial_count and second_count != 0
             and len(not_in_mills_before.difference(not_in_mills_after)) > 0):
        print("A mill was formed!")  # printstatement
        print(board)
        player = get_other_player(
            player)  # call remove piece function to remove piece for other player
        remove_piece(board, player)


def move_piece(board, player, origin, destination):
    """
        add your function header here.
    """
    boarddict = board.points  # dictionary containing all board points and players
    valid_keys = boarddict.keys() #all keys in dictionary
    if origin not in valid_keys or destination not in valid_keys:
        raise RuntimeError('Invalid command')

    ADJACENCY = {"a1": ["d1", "a4"],
                 "d1": ["a1", "d2", "g1"], "g1": ["d1", "g4"],
                 "b2": ["b4", "d2"],
                 "d2": ["b2", "d1", "d3", "f2"], "f2": ["d2", "f4"],
                 "c3": ["c4", "d3"], "d3": ["c3", "d2", "e3"],
                 "e3": ["d3", "e4"],
                 "a4": ["a1", "a7", "b4"], "b4": ["a4", "b2", "b6", "c4"],
                 "c4": ["b4", "c3", "c5"], "e4": ["e3", "e5", "f4"],
                 "f4": ["e4", "f2", "f6", "g4"], "g4": ["f4", "g1", "g7"],
                 "c5": ["c4", "d5"], "d5": ["c5", "d6", "e5"],
                 "e5": ["d5", "e4"],
                 "b6": ["b4", "d6"], "d6": ["b6", "d5", "d7", "f6"],
                 "f6": ["d6", "f4"], "a7": ["a4", "d7"],
                 "d7": ["a7", "d6", "g7"],
                 "g7": ["d7", "g4"]}  # dictonary with adjacency of all points
    adjacencylist = ADJACENCY[origin]  # find adjacency of origin point
    if destination not in adjacencylist:
        raise RuntimeError(
            'Invalid command')  # error if destination isnt adjacent to origin
    else:
        if boarddict[origin] == player:
                board.clear_place(origin)  # remove origin piece
                place_piece_and_remove_opponents(board, player,
                                                 destination)  # place destination piece and check for mills
        else:
            raise RuntimeError("Invalid command: Origin point does not belong to player")


def points_not_in_mills(board, player):
    """
        Takes board and player and returns a set of all points not in mills.
    """
    boarddict = board.points  # dictionary with all board pieces and players
    MILLS = [["a1", "d1", "g1"], ["b2", "d2", "f2"],
             ["c3", "d3", "e3"], ["a4", "b4", "c4"], ["e4", "f4", "g4"],
             ["c5", "d5", "e5"], ["b6", "d6", "f6"], ["a7", "d7", "g7"],
             ["a1", "a4", "a7"], ["b2", "b4", "b6"], ["c3", "c4", "c5"],
             ["d1", "d2", "d3"], ["d5", "d6", "d7"], ["e3", "e4", "e5"],
             ["f2", "f4", "f6"],
             ["g1", "g4", "g7"]]  # list of list of all possible mills
    playervalues = []  # initialize player values list
    count = 0  # initialize count
    count2 = 0  # initialize second count
    newlist = []  # initialize new list
    newlist2 = []  # initilize second new list
    millset = set()  # intialize set

    for k, v in boarddict.items():
        if v == player:
            playervalues.append(k)  # add all of the players pieces to player values list
    newlist_sorted_by_letter = sorted(playervalues)  # create new list with player values sorted
    newlist_sorted_by_numbers = sorted(playervalues, key=functools.cmp_to_key(comparePointsByNumbers))

    # while count is less than the length of player values
    while count < len(playervalues) - 2:
        newlist.append(
            newlist_sorted_by_numbers[count:count + 3])  # add three values to new list
        count += 1  # increase count by 3
    allpoints = set(playervalues)  # create a set out of playervalues list
    # while count 2 is greater than 0
    while count2 < len(playervalues) - 2:
        newlist2.append(
            newlist_sorted_by_letter[count2:count2 + 3])  # add three values to newlist2
        count2 += 1  # decrease count by 3
        # for loop for each list in newlist
    for l in newlist:
        if l in MILLS:
            for v in l:
                millset.add(v)  # add value to millset if in MILLS
                # repeat process for newlist2
    for l in newlist2:
        if l in MILLS:
            for v in l:
                millset.add(v)
    diff = allpoints.difference(
        millset)  # set intersection to find points not in mills
    return diff  # return set


def placed(board, player):
    """
        Takes board and a player. Returns a list of all pieces placed
        by the player.
    """
    boarddict = board.points  # dictionary containing all pieces and players on board
    finallist = []  # initialize final list
    # go through each item in board and append all pieces associated with player in list
    for k, v in boarddict.items():
        if v == player:
            finallist.append(k)
    return finallist  # return final list


def remove_piece(board, player):
    """
        Takes board and player. Prompts user to enter piece to remove.
        Removes the piece from board if valid.
    """
    boarddict = board.points  # dictionary containing all pieces and players on board
    alllocations = []  # initialize all locations list
    placedpieces = placed(board,
                          player)  # call function to get a list of all pieces placed by player
    open_locations = points_not_in_mills(board,
                                         player)  # call function to get a list a points not in mills
    piece = input(
        'Remove a piece at :> ')  # prompt user for which piece to remove
    for k, v in boarddict.items():
        alllocations.append(k)  # append all pieces on board to list
    # check if piece is a piece on board
    while piece not in alllocations:
        print('Invalid command: Not a valid point Try again.')
        piece = input('Remove a piece at :> ')
    # check if piece is not already placed
    while piece not in placedpieces:
        print(
            'Invalid command: Point does not belong to player Try again.')
        piece = input('Remove a piece at :> ')
    # check if point is not already in a mill
    if open_locations != set():
        while piece not in open_locations:
            print('Invalid command: Point is in a mill \n Try again.')
            piece = input('Remove a piece at :> ')
    board.clear_place(piece)  # remove the piece from board


def is_winner(board, player):
    """
        Takes a board and a player. Returns true if
        the player is the winner and false if the
        player is not.
    """
    opponentcount = 0  # initialize opponent count
    boarddict = board.points  # dictionary containing all pieces and players on board
    # go through values in dict and increase count if it is the opponents piece
    for v in boarddict.values():
        if v != player and v != ' ':
            opponentcount += 1
    # if opponent has less than three pieces than return true
    if opponentcount < 3:
        return True
    # return false if opponent has three or more pieces
    else:
        return False

def get_other_player(player):
    """
    Get the other player.
    """
    return "X" if player == "O" else "O"


def main():
    # Loop so that we can start over on reset
    while True:
        # Setup stuff.
        print(RULES)
        print(MENU)
        board = NMM.Board()
        print(board)
        player = "X"
        placed_count = 0  # total of pieces placed by "X" or "O", includes pieces placed and then removed by opponent
        # PHASE 1
        print(player + "'s turn!")
        # placed = 0
        command = input("Place a piece at :> ").strip().lower()
        print()
        # Until someone quits or we place all 18 pieces...
        while command != 'q' and placed_count != 18 and command != 'r':
            try:
                if command == 'h':
                    print(MENU)
                    command = input("Place a piece at :> ").strip().lower()

                place_piece_and_remove_opponents(board, player, command)
                placed_count += 1
                player = get_other_player(player)
            # Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
            # Prompt again
            print(board)
            print(player + "'s turn!")
            if placed_count < 18:
                command = input("Place a piece at :> ").strip().lower()
            else:
                print(
                    "**** Begin Phase 2: Move pieces by specifying two points")
                command = input(
                    "Move a piece (source,destination) :> ").strip().lower()
            print()
        # Go back to top if reset
        if command == 'r':
            continue
        # PHASE 2 of game
        while command != 'q':
            # commands should have two points
            command = command.split()
            try:
                if command[0] and command[1] in board.points:
                    move_piece(board, player, command[0], command[1])
                    winner = is_winner(board, player)
                    player = get_other_player(player)
                    if winner is True:
                        print()
                        print(BANNER)
                        command = 'q'
                        break
                else:
                    print("Invalid command: Not a valid point")
                    print("Try again.")
            # Any RuntimeError you raise inside this try lands here
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
            except IndexError:
                print("Invalid number of points")
                print("Try again.")

            # Display and reprompt
            print(board)
            # display_board(board)
            print(player + "'s turn!")
            command = input(
                "Move a piece (source,destination) :> ").strip().lower()
            print()
        # If we ever quit we need to return
        if command == 'q':
            return


if __name__ == "__main__":
    main()
