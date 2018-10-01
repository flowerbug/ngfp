import pyglet
import sys

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

this.square = None


def MoveLeft (self):

    return (-1)


def MovingLeft (self, dir):

    return (dir == MoveLeft(self))


def MoveRight (self):

    return (1)


def MovingRight (self, dir):

    return (dir == MoveRight(self))


def MoveUp (self):

    return (self.window_cols)


def MovingUp (self, dir):

    return (dir == MoveUp(self))


def MoveDown (self):

    return (-self.window_cols)


def MovingDown (self, dir):

    return (dir == MoveDown(self))


def ReverseDir (self, dir):
    return (-dir)


def MirrorMagic (self, cur_pos, cur_dir):

    board_index = self.board_to_window_index.index(cur_pos)
    widget = self.board[board_index][0]
    print ("board index ", board_index, " widget ", widget)
    if (widget == 1):
        if (MovingLeft(self, cur_dir)):
            return (MoveUp(self))
        elif (MovingRight(self, cur_dir)):
            return (MoveDown(self))
        elif (MovingUp(self, cur_dir)):
            return (MoveLeft(self))
        else:
            return (MoveRight(self))
    elif (widget == 9):  # box
        return (ReverseDir(self, cur_dir))
    elif (widget == 10):  # sink
        return (None)
    else:
        return (cur_dir)


def ShowArrow (self, dir, xy_coord):

    self.arrow_sprites[dir].x = xy_coord[0]
    self.arrow_sprites[dir].y = xy_coord[1]
    self.arrow_sprites[dir].visible = True


def ShowWhiteInArrow (self, win_pos):

    win_pos_index = self.white_active_squares.index(win_pos)
    xy_coordinates = self.white_active_squares_position[win_pos_index]
    print ("XY coordinates", xy_coordinates)
    if (win_pos in self.dir_left):     # if we've clicked on the left side it
        self.start_direction = MoveRight(self) # means we're going right
        ShowArrow(self, 5, xy_coordinates)
    elif (win_pos in self.dir_right):        # if we've clicked on the right side it
        self.start_direction = MoveLeft(self)  # means we're going left
        ShowArrow(self, 4, xy_coordinates)
    elif (win_pos in self.dir_down):         #  etc.
        self.start_direction = MoveUp(self)
        ShowArrow(self, 6, xy_coordinates)
    else:
        self.start_direction = MoveDown(self)
        ShowArrow(self, 7, xy_coordinates)


def ShowWhiteOutArrow (self, win_pos):

    win_pos_index = self.white_active_squares.index(win_pos)
    xy_coordinates = self.white_active_squares_position[win_pos_index]
    print ("XY coordinates", xy_coordinates)
    if (win_pos in self.dir_left):           # if it is to the left side it
        self.start_direction = MoveRight(self) # means we're going left
        ShowArrow(self, 4, xy_coordinates)
    elif (win_pos in self.dir_right):        # if its on the right side it
        self.start_direction = MoveLeft(self)  # means we're going right
        ShowArrow(self, 5, xy_coordinates)
    elif (win_pos in self.dir_down):         #  etc.
        self.start_direction = MoveUp(self)
        ShowArrow(self, 7, xy_coordinates)
    else:
        self.start_direction = MoveDown(self)
        ShowArrow(self, 6, xy_coordinates)


def MarbleInMotion (self, x_rec, y_rec, win_pos):

    ShowWhiteInArrow (self, win_pos)
    start_pos = win_pos
    print ("Starting to move marble from ", start_pos, "in direction ", self.start_direction)

    tick_count = 0  #  we better limit just in case of long loops
    current_pos = start_pos + self.start_direction
    current_direction = self.start_direction
    print ("First move marble from ", current_pos, "in direction ", current_direction)
    while (
        (current_pos not in self.white_active_squares) and 
        (tick_count < 100) and (current_pos != None)):
        tick_count += 1
        new_dir = MirrorMagic (self, current_pos, current_direction)
        if (new_dir != None):
            print ("Moved: Tick, CP, CD ", tick_count, current_pos, current_direction)
            current_pos += new_dir
            current_direction = new_dir
        else:
            print ("Didn't Move: Tick, CP, CD ", tick_count, current_pos, current_direction)
            current_direction = None

    print ("Last move marble at ", current_pos, "in direction ", current_direction)
    if (current_direction != None):
        ShowWhiteOutArrow (self, current_pos)


def DoLeftClickWhiteAction (self, x, x_rec, y, y_rec, win_pos):

    MarbleInMotion (self, x_rec, y_rec, win_pos)


