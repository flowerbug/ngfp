import os
import copy
import json
from board import DrawBoard

def Load_GFPSave_Version_1 (self, lines_in):

    print (lines_in)

    print (lines_in[0], lines_in[1])
    line = lines_in.pop(0)
    line = lines_in.pop(0)
    board_dimensions_strings = line.split()
    print (board_dimensions_strings)
    new_board_rows = int(board_dimensions_strings[0])
    new_board_cols = int(board_dimensions_strings[1])
    print (new_board_rows, new_board_cols)

    # remember the lists are numbered from bottom left in pyglet
    # so board[0][0] is the 1st item of the last line, which is why 
    # we reverse them
    guess_lines = lines_in[:new_board_cols]
    marker_lines = lines_in[new_board_cols:new_board_cols*2]
    board_lines = lines_in[new_board_cols*2:new_board_cols*3]

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
    self.game_rows = new_board_rows
    self.game_cols = new_board_cols

    print ("Markers ", marker_lines)

    counters_str = lines_in[len(lines_in)-1]
    new_counters = []
    for i in counters_str.split():
       new_counters.append(int(i))
    print ("Widget Counters ", new_counters)

    del self.widget_pile_list_counts 
    self.widget_pile_list_counts = copy.deepcopy(new_counters)


def Load_NGFPSave_Version_1 (self, lines_in):

    print ("Load_NGFPSave_Version_1...")
    print (lines_in)

    self.game_rows = lines_in[1][0]
    self.game_cols = lines_in[1][1]

    del self.board
    self.board = copy.deepcopy(lines_in[2])

    del self.widget_pile_list_counts 
    self.widget_pile_list_counts = copy.deepcopy(lines_in[3])


def LoadSavedGameFromFile (self):

    print ("LoadSavedGameFromFile...")

    # for now, if the first file exists assume 
    # it's the first one we want to use
    try:
        with open("save.ngfp") as filein:
            lines_in = filein.readlines()
        Load_GFPSave_Version_1 (self, lines_in)
        self.show_board = 2  # reinitialize sprites and lists
        DrawBoard (self)
    except:
        try:
            with open("save.json") as filein:
                lines_in = json.load(filein)
            Load_NGFPSave_Version_1 (self, lines_in)
            self.show_board = 2  # reinitialize sprites and lists
            DrawBoard (self)
        except:
            print ("Files save.ngfp and save.json are missing...")


def SaveGameToFile (self):

    print ("SaveGameToFile...")

    with open("save.json", mode="w") as fileout:

        json.dump([["NGFP_Save\n", 1], [self.game_rows, self.game_cols], self.board, self.widget_pile_list_counts], fileout, indent = 4, separators=(',', ': '))


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


