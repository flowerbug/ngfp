import pyglet
import sys
import copy
from history import UpdateAndShowArrow, HistoryNext


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


def ShowWhiteInArrow (self, win_pos):

    win_pos_index = self.white_active_squares.index(win_pos)
    SWI_xy_coordinates = copy.deepcopy(self.white_active_squares_position[win_pos_index])
    print ("SW In Arrow XY coordinates", SWI_xy_coordinates)
    rotate = 0.0
    if (win_pos in self.dir_left):             # if we've clicked on the left side it
        self.start_direction = MoveRight(self) # means we're going right
        SWI_xy_coordinates[0] += self.half_img_pix
        image = self.arrow_images[1]
    elif (win_pos in self.dir_right):          # if we've clicked on the right side it
        self.start_direction = MoveLeft(self)  # means we're going left
        image = self.arrow_images[0]
    elif (win_pos in self.dir_up):             #  etc.
        self.start_direction = MoveDown(self)
        image = self.arrow_images[3]
        rotate = 90.0
    else:
        self.start_direction = MoveUp(self)
        SWI_xy_coordinates[1] += self.half_img_pix
        image = self.arrow_images[2]
        rotate = 90.0
    UpdateAndShowArrow(self, image, 0, SWI_xy_coordinates, rotate)


def ShowWhiteOutArrow (self, win_pos):

    if (self.stop_direction == None):
        print ("SW Out Arrow __No__ Arrow Out")
    else:
        win_pos_index = self.white_active_squares.index(win_pos)
        SWO_xy_coordinates = copy.deepcopy(self.white_active_squares_position[win_pos_index])
        print ("SW Out Arrow XY coordinates", SWO_xy_coordinates)
        rotate = 0.0
        if (win_pos in self.dir_left):             # if on the left side it
            self.stop_direction = MoveLeft(self)   # means we're going left
            image = self.arrow_images[0]
        elif (win_pos in self.dir_right):          # if on the right side it
            self.stop_direction = MoveRight(self)  # means we're going right
            SWO_xy_coordinates[0] += self.half_img_pix
            image = self.arrow_images[1]
        elif (win_pos in self.dir_up):             #  etc.
            self.stop_direction = MoveUp(self)
            SWO_xy_coordinates[1] += self.half_img_pix
            image = self.arrow_images[2]
            rotate = 90.0
        else:
            self.stop_direction = MoveDown(self)
            image = self.arrow_images[3]
            rotate = 90.0
        UpdateAndShowArrow(self, image, 1, SWO_xy_coordinates, rotate)


def MarbleInMotion (self, x_rec, y_rec, win_pos):

    start_pos = win_pos
    self.start_direction = None
    self.stop_direction = None
    ShowWhiteInArrow (self, win_pos)
    print ("Starting to move marble from ", start_pos, "in direction ", self.start_direction)

    tick_count = 0  #  we better have some limit just in case of long loops
    current_pos = start_pos + self.start_direction
    current_direction = self.start_direction
    print ("First move marble from ", current_pos, "in direction ", current_direction)
    while (
        (current_pos in self.guess_active_squares) and 
        (tick_count < 100) and 
        (current_pos != None)):
        tick_count += 1
        new_dir = MirrorMagic (self, current_pos, current_direction)
        if (new_dir != None):
            print ("Moved: Tick, CP, CD ", tick_count, current_pos, current_direction)
            current_pos += new_dir
            current_direction = new_dir
            self.stop_direction = current_direction
        else:
            print ("Didn't Move: Tick, CP, CD ", tick_count, current_pos, current_direction)
            self.stop_direction = None

    print ("Last moved marble at ", current_pos, "in direction ", current_direction)
    if (tick_count >= 100):
        print ("Exceeded tick_count of 100")
    elif (current_direction == None):
        print ("No Arrow Out...")
    else:
        ShowWhiteOutArrow (self, current_pos)
    HistoryNext (self)


def DoLeftClickWhiteAction (self, x, x_rec, y, y_rec, win_pos):

    MarbleInMotion (self, x_rec, y_rec, win_pos)

