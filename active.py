import pyglet
import sys

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

this.square = None


def ShowWhiteInArrow (self, x_rec, y_rec, win_pos):
    pass


def ShowWhiteOutArrow (self, x_rec, y_rec, win_pos):
    pass


def MarbleInMotion (self, x_rec, y_rec, win_pos):
    pass


def DoWhiteAction (self, x_rec, y_rec, win_pos):

    ShowWhiteInArrow (self, x_rec, y_rec, win_pos)
    MarbleInMotion (self, x_rec, y_rec, win_pos)
    ShowWhiteOutArrow (self, x_rec, y_rec, win_pos)


def DoWidgetAction (self, x_rec, y_rec, win_pos):

    widget_index = self.widget_active_squares.index(win_pos)
    if (self.picked_up):
        if (win_pos == self.picked_up_window_square):
            self.picked_up_window_square = -1
            self.picked_up = False
            self.picked_up_sprite.visible = False
            self.picked_up_sprite.image = self.white_bg_image
            print ("Dropped ", widget_index)
            self.cube.visible = True
        else:
            self.picked_up_window_square = win_pos
            self.picked_up_sprite.image = self.blue_bg_image
            self.picked_up_sprite.x = x_rec
            self.picked_up_sprite.y = y_rec
            self.picked_up_sprite.visible = True
            print ("Picked up other item ", widget_index)
            self.cube.visible = False
    else:
        self.picked_up_window_square = win_pos
        self.picked_up = True
        self.picked_up_sprite.image = self.green_bg_image
        self.picked_up_sprite.x = x_rec
        self.picked_up_sprite.y = y_rec
        self.picked_up_sprite.visible = True
        print ("Picked up ", widget_index)
        self.cube.visible = False


def ActiveAreaAction (self, x_rec, y_rec, win_pos):

    this.square = win_pos
    if (win_pos in self.white_active_squares):
        print ("selected ", win_pos, " which is an active White square.")
        DoWhiteAction (self, x_rec, y_rec, win_pos)
    elif (win_pos in self.widget_active_squares):
        print ("selected ", win_pos, " which is an active Widget square.")
        DoWidgetAction (self, x_rec, y_rec, win_pos)
    else:
        pass


def ActiveAreaMouseAction (self, x, x_rec, y, y_rec, win_pos):

    if (win_pos in self.widget_active_squares):
        if (this.square != win_pos):
            print ("moved over ", win_pos, " which is an active Widget square.")
            this.square = win_pos
        self.picked_up_sprite.x = x_rec
        self.picked_up_sprite.y = y_rec
        self.picked_up_sprite.visible = True
    else:
        self.picked_up_sprite.x = x_rec
        self.picked_up_sprite.y = y_rec
        self.picked_up_sprite.visible = False


