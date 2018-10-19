import os
import sys
import copy
import json
from pathlib import Path
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import Gdk

from board import DrawBoard


setting = Gio.Settings.new("org.gtk.Settings.FileChooser")
setting.set_boolean("sort-directories-first", True)


# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

this.this_fn_to_open = None
this.this_fn_to_save = None
this.home = Path.home()
this.data_path = this.home / Path(".local/share/ngfp")
this.config_path = this.home / Path(".config/ngfp")
this.saved_dir = None


def add_filters(dialog):

    filter_json = Gtk.FileFilter()
    filter_json.set_name("json files")
    filter_json.add_pattern("*.json")
    dialog.add_filter(filter_json)

    filter_gfp = Gtk.FileFilter()
    filter_gfp.set_name("gfp files")
    filter_gfp.add_pattern("*.gfp")
    dialog.add_filter(filter_gfp)


class MyOpenWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="File Open", has_focus=False)

        self.set_border_width (20)
        self.set_default_size (300,100)
        self.set_position (Gtk.WindowPosition.MOUSE)

        self.dialog = Gtk.FileChooserDialog("Please choose a file", self,
        Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            "Select", Gtk.ResponseType.OK))

        add_filters(self.dialog)
        self.dialog.set_border_width (20)
        self.dialog.set_default_size (300,100)
        self.dialog.set_position (Gtk.WindowPosition.MOUSE)

        self.dialog.show_all()
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            this.this_fn_to_open = self.dialog.get_filename()
            print("File selected: " + self.dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        self.dialog.destroy()
        self.quit(self)

    def quit (self, widget, event=None):
        #return True # prevent closing
        return False # close


class MySaveAsWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="File Save As", has_focus=False)

        self.set_border_width (20)
        self.set_default_size (300,100)
        self.set_position (Gtk.WindowPosition.MOUSE)

        self.dialog = Gtk.FileChooserDialog("Save your game as", self,
        Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            "Select", Gtk.ResponseType.OK))

        add_filters(self.dialog)
        self.dialog.set_border_width (20)
        self.dialog.set_default_size (300,100)
        self.dialog.set_position (Gtk.WindowPosition.MOUSE)

        self.dialog.set_do_overwrite_confirmation(self.dialog)

        if (this.this_fn_to_save == None):
            self.dialog.set_current_name(str(this.data_path / Path("save.json")))
        else:
            self.dialog.set_filename(this.this_fn_to_save)

        self.dialog.show_all()
        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            this.this_fn_to_save = self.dialog.get_filename()
            print("File selected: " + self.dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        self.dialog.destroy()
        self.quit(self)

    def quit (self, widget, event=None):
        #return True # prevent closing
        return False # close


def ShowAbout (self):

    print ("ngfp is running in directory ", str(Path.cwd()))
    print ("ngfp saves game files to : ", str(this.data_path))
    print ("ngfp keeps configuration data in : ", str(this.config_path))


def Load_GFPSave_Version_1 (self, lines_in):

    line = lines_in.pop(0)
    line = lines_in.pop(0)
    board_dimensions_strings = line.split()
    new_board_rows = int(board_dimensions_strings[0])
    new_board_cols = int(board_dimensions_strings[1])

    # remember the lists are numbered from bottom left in pyglet
    # so board[0][0] is the 1st item of the last line, which is why 
    # we reverse them
    guess_lines = lines_in[:new_board_cols]
    marker_lines = lines_in[new_board_cols:new_board_cols*2]
    board_lines = lines_in[new_board_cols*2:new_board_cols*3]

    new_board = []
    for i in reversed(range(len(board_lines))):
        line_str = board_lines[i]
        for item_ind in line_str.split():
            new_board.append([int(item_ind), 0])

    board_ind = 0
    for i in reversed(range(len(guess_lines))):
        line_str = guess_lines[i]
        for item_ind in line_str.split():
            new_board[board_ind][1] = int(item_ind)
            board_ind += 1

    del self.board
    self.board = copy.deepcopy(new_board)
    self.game_rows = new_board_rows
    self.game_cols = new_board_cols

    counters_str = lines_in[len(lines_in)-1]
    new_counters = []
    for i in counters_str.split():
       new_counters.append(int(i))

    del self.widget_pile_list_counts 
    self.widget_pile_list_counts = copy.deepcopy(new_counters)


def Load_NGFPSave_Version_1 (self, lines_in):

    self.game_rows = lines_in[1][0]
    self.game_cols = lines_in[1][1]

    del self.board
    self.board = copy.deepcopy(lines_in[2])

    del self.widget_pile_list_counts 
    self.widget_pile_list_counts = copy.deepcopy(lines_in[3])


def LoadSavedGameFromFile (self):

    print ("LoadSavedGameFromFile...")

    this.this_fn_to_open = None
    this.saved_dir = str(Path.cwd())
    print ("Keep track of current directory : ", this.saved_dir)
    if (this.data_path.exists() != True):
        print ("Creating : ", str(this.data_path))
        this.data_path.mkdir(mode=0o700, parents=True, exist_ok=False)
    print ("Changing directory to : ", str(this.data_path))
    os.chdir(str(this.data_path))
    win = MyOpenWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.hide()

    print ("Going back to directory : ", this.saved_dir)
    os.chdir(this.saved_dir)

    if (this.this_fn_to_open == None):
        print ("LoadSavedGameFromFile...  No file selected...")
        return

    print ("File selected : ", this.this_fn_to_open)
    if (this.this_fn_to_open[-4:] == ".gfp"):
        try:
            with open(this.this_fn_to_open) as filein:
                lines_in = filein.readlines()
            Load_GFPSave_Version_1 (self, lines_in)
            self.show_board = 2  # reinitialize sprites and lists
            DrawBoard (self)
            return
        except:
            print ("LoadSavedGameFromFile : ", this.this_fn_to_open, "didn't load...")
    elif (this.this_fn_to_open[-5:] == ".json"):
        try:
            with open(this.this_fn_to_open) as filein:
                lines_in = json.load(filein)
            Load_NGFPSave_Version_1 (self, lines_in)
            self.show_board = 2  # reinitialize sprites and lists
            DrawBoard (self)
            return
        except:
            print ("LoadSavedGameFromFile : ", this.this_fn_to_open, "didn't load...")

    # we shouldn't ever get here
    print ("File extension needs to be .json, .gfp or .gfp...")


def SaveGameToFile (self):

    print ("SaveGameToFile ...")

    this.saved_dir = str(Path.cwd())
    print ("Keep track of current directory : ", this.saved_dir)
    if (this.data_path.exists() != True):
        print ("Creating : ", str(this.data_path))
        this.data_path.mkdir(mode=0o700, parents=True, exist_ok=False)
    print ("Changing directory to : ", str(this.data_path))
    os.chdir(str(this.data_path))

    win = MySaveAsWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.hide()

    print ("Saving Game to File : ", this.this_fn_to_save)
    with open(this.this_fn_to_save, mode="w") as fileout:
 
        json.dump([["NGFP_Save\n", 1], [self.game_rows, self.game_cols], self.board, self.widget_pile_list_counts], fileout, indent = 4, separators=(',', ': '))

    print ("Going back to directory : ", this.saved_dir)
    os.chdir(this.saved_dir)


def DoDialogControlAction (self, x, x_rec, y, y_rec, win_pos):

    print ("DoDialogControlAction ", x, x_rec, y, y_rec, win_pos)

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
        self.show_board = (self.show_board + 1) % 2
    elif (menu_index == 3):
        # Load Saved Game
        LoadSavedGameFromFile (self)
    elif (menu_index == 4):
        # Save Current Game
        SaveGameToFile (self)
    elif (menu_index == 5):
        # About This Game
        ShowAbout (self)
    else:
        pass


