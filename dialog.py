import os
import copy
from board import DrawBoard


def LoadSavedGameFromFile (self):

    print ("LoadSavedGameFromFile...")

    with open("save.ngfp") as filein:
        lines = filein.readlines()

    print (lines)

    print (lines[0], lines[1])
    line = lines.pop(0)
    line = lines.pop(0)
    board_dimensions_strings = line.split()
    print (board_dimensions_strings)
    new_board_rows = int(board_dimensions_strings[0])
    new_board_cols = int(board_dimensions_strings[1])
    print (new_board_rows, new_board_cols)

    # remember the lists are numbered from bottom left in pyglet
    # so board[0][0] is the 1st item of the last line, which is why 
    # we reverse them
    guess_lines = lines[:new_board_cols]
    marker_lines = lines[new_board_cols:new_board_cols*2]
    board_lines = lines[new_board_cols*2:new_board_cols*3]

    print ("Board ", board_lines)
    new_board = []
    for i in reversed(range(len(board_lines))):
        line_str = board_lines[i]
        for item_ind in line_str.split():
            new_board.append([int(item_ind), 0])

    print ("Guesses ", guess_lines)
    board_ind = 0
    for i in reversed(range(len(guess_lines))):
        line_str = guess_lines[i]
        for item_ind in line_str.split():
            new_board[board_ind][1] = int(item_ind)
            board_ind += 1

    print ("New Board ", new_board)

    del self.board
    self.board = copy.deepcopy(new_board)

    print ("Markers ", marker_lines)

    counters_str = lines[len(lines)-1]
    new_counters = []
    for i in counters_str.split():
       new_counters.append(int(i))
    print ("Widget Counters ", new_counters)

    del self.widget_pile_list_counts 
    self.widget_pile_list_counts = copy.deepcopy(new_counters)

    self.show_board = 2  # reinitialize sprites and lists
    DrawBoard (self)


def SaveGameToFile (self):

   print ("SaveGameToFile, doesn't work yet...")


def DoDialogControlAction (self, x, x_rec, y, y_rec, win_pos):

#    print ("DoDialogControlAction ", x, x_rec, y, y_rec, win_pos)

    menu_index = self.control_active_squares.index(win_pos)

    # simple menu selection
    if (menu_index == 0):
        # New Game Dialog
        pass
    elif (menu_index == 1):
        # Check Board
        pass
    elif (menu_index == 2):
        # Flip to Other Board
        pass
    elif (menu_index == 3):
        # Load Saved Game
        LoadSavedGameFromFile (self)
        pass
    elif (menu_index == 4):
        # Save Current Game
        SaveGameToFile (self)
        pass
    elif (menu_index == 5):
        # About This Game
        pass
    else:
        pass


