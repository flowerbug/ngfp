import pyglet


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
    pass


def ActiveAreaAction (self, x_rec, y_rec, win_pos):

    if (win_pos in self.white_active_squares):
        print ("selected ", win_pos, " which is an active White square.")
        DoWhiteAction (self, x_rec, y_rec, win_pos)
    elif (win_pos in self.widget_active_squares):
        print ("selected ", win_pos, " which is an active Widget square.")
        DoWidgetAction (self, x_rec, y_rec, win_pos)
    else:
        pass

