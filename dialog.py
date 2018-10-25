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
import config as cfg


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


class MyConfigWindow(Gtk.ApplicationWindow):


    def __init__(self, app):
        Gtk.Window.__init__(self, title="Ngfp Configuration", application=app)
        self.set_border_width (30)
        self.set_default_size(600, 600)
        self.set_position (Gtk.WindowPosition.CENTER)

        # adjustments (initial value, min value, max value,
        # step increment - press cursor keys to see!,
        # page increment - click around the handle to see!,
        # page size - not used here)
        adj_width = Gtk.Adjustment(cfg.game_cols, 8, 20, 1, 1, 0)
        adj_height = Gtk.Adjustment(cfg.game_rows, 8, 20, 1, 1, 0)
        adj_density = Gtk.Adjustment(cfg.density, 0, 100, 1, 1, 0)
        adj_density_fuzz = Gtk.Adjustment(cfg.density_fuzz, 0, (100 - cfg.density), 1, 1, 0)

        # a horizontal scale
        self.h1_scale = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj_width)
        # of integers (no digits)
        self.h1_scale.set_digits(0)
        # that can expand horizontally if there is space in the grid (see
        # below)
        self.h1_scale.set_hexpand(False)
        # that is aligned at the top of the space allowed in the grid (see
        # below)
        self.h1_scale.set_valign(Gtk.Align.START)

        # we connect the signal "value-changed" emitted by the scale with the callback
        # function left_scale_moved
        self.h1_scale.connect("value-changed", self.left_scale_moved)

        # 2nd horizontal scale
        self.h2_scale = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj_height)
        # of integers (no digits)
        self.h2_scale.set_digits(0)
        # that can expand horizontally if there is space in the grid (see below)
        self.h2_scale.set_hexpand(False)

        # we connect the signal "value-changed" emitted by the scale with the callback
        # function left_scale_moved
        self.h2_scale.connect("value-changed", self.left_scale_moved)

        # 3rd horizontal scale
        self.h3_scale = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj_density)
        # of integers (no digits)
        self.h3_scale.set_digits(0)
        # that can expand horizontally if there is space in the grid (see below)
        self.h3_scale.set_hexpand(False)

        # we connect the signal "value-changed" emitted by the scale with the callback
        # function left_scale_moved
        self.h3_scale.connect("value-changed", self.left_scale_moved)

        # 4th horizontal scale
        self.h4_scale = Gtk.Scale(
            orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj_density_fuzz)
        # of integers (no digits)
        self.h4_scale.set_digits(0)
        # that can expand horizontally if there is space in the grid (see below)
        self.h4_scale.set_hexpand(False)

        # we connect the signal "value-changed" emitted by the scale with the callback
        # function left_scale_moved
        self.h4_scale.connect("value-changed", self.left_scale_moved)

        # the four labels needed on the left side
        self.l1_label = Gtk.Label()
        self.l1_label.set_text(cfg.property_labels[0])
        self.l2_label = Gtk.Label()
        self.l2_label.set_text(cfg.property_labels[1])
        self.l3_label = Gtk.Label()
        self.l3_label.set_text(cfg.property_labels[2])
        self.l4_label = Gtk.Label()
        self.l4_label.set_text(cfg.property_labels[3])

        # and then the bottom label for the left side
        self.bottom_label_left = Gtk.Label()
        self.bottom_label_left.set_text("Move the scale handles...")
        self.bottom_label_left.set_width_chars (21)

        # a grid to attach the widgets
        self.grid = Gtk.Grid ()
        self.grid.set_row_homogeneous (True)
        self.grid.set_column_spacing (2)
        self.grid.set_row_spacing (20)

        # do the left side first
        self.grid.add (self.h1_scale)
        self.grid.attach_next_to (self.l1_label, self.h1_scale, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to (self.h2_scale, self.l1_label, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to (self.l2_label, self.h2_scale, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to (self.h3_scale, self.l2_label, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to (self.l3_label, self.h3_scale, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to (self.h4_scale, self.l3_label, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to (self.l4_label, self.h4_scale, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to (self.bottom_label_left, self.l4_label, Gtk.PositionType.BOTTOM, 1, 1)

        class_pack = []
        class_label = []
        class_pic_pack = []
        class_pic_left = []
        class_pic_right = []
        class_adj = []
        self.class_scale = []

        # ok, now the right side
        pic_ind = 0
        j = 0
        col = 1
        for i in range(len(cfg.widget_class_labels)):
            class_pack.append (Gtk.Box (orientation=Gtk.Orientation.VERTICAL))
            class_label.append (Gtk.Label (cfg.widget_class_labels[i]))
            class_pack[i].pack_start (class_label[i], True, False, 0)
            class_label[i].set_width_chars (15)
            class_pic_pack.append (Gtk.Box (spacing=50))
            class_pic_pack[i].set_halign (Gtk.Align.CENTER)
            class_pic_left.append (Gtk.Image.new_from_file(cfg.pic_list[cfg.config_percent_list[pic_ind]]))
            pic_ind += 1
            class_pic_right.append (Gtk.Image.new_from_file(cfg.pic_list[cfg.config_percent_list[pic_ind]]))
            pic_ind += 1
            class_pic_pack[i].pack_start (class_pic_left[i], False, False, 0)
            class_pic_pack[i].pack_start (class_pic_right[i], False, False, 0)
            class_pack[i].pack_start (class_pic_pack[i], True, True, 0)
            class_adj.append (Gtk.Adjustment (cfg.class_weights[i], 0, 100, 1, 1, 0))
            self.class_scale.append (Gtk.Scale (orientation=Gtk.Orientation.HORIZONTAL, adjustment=class_adj[i]))
            self.class_scale[i].set_digits(0)
            class_pack[i].pack_start (self.class_scale[i], True, False, 0)
            self.grid.attach (class_pack[i], col, j, 1, 3)

            # we connect the signal "value-changed" emitted by the scale with the callback
            # function right_scale_moved
            self.class_scale[i].connect("value-changed", self.right_scale_moved)

            if ((i + 1) > 3):
                j = 4
                col = (i + 1) % 4 + 1
            else:
                col += 1

        new_game_button = Gtk.Button.new_with_label("New Game")
        new_game_button.connect("clicked", self.on_new_game_clicked) 
        self.grid.attach (new_game_button, 4, 4, 1, 1)

        save_button = Gtk.Button.new_with_label("Save Config")
        save_button.connect("clicked", self.on_save_clicked)
        self.grid.attach (save_button, 4, 5, 1, 1)

        load_button = Gtk.Button.new_with_label("Load Config")
        load_button.connect("clicked", self.on_load_clicked)
        self.grid.attach (load_button, 4, 6, 1, 1)

        cancel_button = Gtk.Button.new_with_label("Cancel")
        cancel_button.connect("clicked", self.on_cancel_clicked)
        self.grid.attach (cancel_button, 4, 7, 1, 1)

        restore_button = Gtk.Button.new_with_label("Defaults")
        restore_button.connect("clicked", self.on_restore_clicked)
        self.grid.attach (restore_button, 4, 8, 1, 1)

        self.add(self.grid)


    # any signal from the left property scales is signaled to the
    # bottom_label_left text of which is changed and also the
    # respective config parameters
    def left_scale_moved(self, event):
        width = int(self.h1_scale.get_value())
        height = int(self.h2_scale.get_value())
        density = int(self.h3_scale.get_value())
        density_fuzz = int(self.h4_scale.get_value())
        if (width != cfg.game_cols):
            cfg.new_game_cols = width
        if (height != cfg.game_rows):
            cfg.new_game_rows = height
        if (density != cfg.density):
            cfg.new_density = density
        if (density_fuzz != cfg.density_fuzz):
            cfg.new_density_fuzz = density_fuzz
        self.bottom_label_left.set_text("W " + str(width) + " H " + str(height) + " D " + str(density) + " F " + str(density_fuzz))


    # any signals from the right class scales is signaled to
    # update the config class_weights
    def right_scale_moved(self, event):
        for i in range(len(self.class_scale)):
            new_value = int(self.class_scale[i].get_value())
            print ("NV ", new_value)
            if (new_value != cfg.new_class_weights[i]):
                cfg.new_class_weights[i] = new_value
        print ("C ", cfg.class_weights)
        print ("N ", cfg.new_class_weights)
        for i in range(len(self.class_scale)):
            new_value = int(self.class_scale[i].get_value())
            print ("NV ", new_value)
            if (new_value != cfg.new_class_weights[i]):
                cfg.new_class_weights[i] = new_value
        print ("C ", cfg.class_weights)
        print ("N ", cfg.new_class_weights)
        print ("D ", cfg.default_class_weights)


    def on_new_game_clicked(self, widget):
        print ("New Game")


    def on_save_clicked(self, widget):
        print ("Save Config")


    def on_load_clicked(self, widget):
        print ("Load Config")


    def on_cancel_clicked(self, widget):
        print ("Cancel")
        self.destroy ()
        print ("C ", cfg.class_weights)
        print ("N ", cfg.new_class_weights)
        print ("D ", cfg.default_class_weights)


    def on_restore_clicked(self, widget):
        print ("Restore Defaults")
        cfg.RestoreDefaults (self)
        self.h1_scale.set_value(cfg.game_cols)
        self.h2_scale.set_value(cfg.game_rows)
        self.h3_scale.set_value(cfg.density)
        self.h4_scale.set_value(cfg.density_fuzz)
        for i in range(len(cfg.default_class_weights)):
            self.class_scale[i].set_value (cfg.default_class_weights[i])
        print ("C ", cfg.class_weights)
        print ("N ", cfg.new_class_weights)
        print ("D ", cfg.default_class_weights)


class MyConfigApplication(Gtk.Application):


    def __init__(self):
        Gtk.Application.__init__(self)


    def do_activate(self):
        win = MyConfigWindow(self)
        win.show_all()


    def do_startup(self):
        Gtk.Application.do_startup(self)


def ConfigGame (self):

    print ("ConfigGame dialog ...")

    app = MyConfigApplication()
    app.run()


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
        ConfigGame (self)
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


