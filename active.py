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


def DoWhiteAction (self, x, x_rec, y, y_rec, win_pos):

    ShowWhiteInArrow (self, x_rec, y_rec, win_pos)
    MarbleInMotion (self, x_rec, y_rec, win_pos)
    ShowWhiteOutArrow (self, x_rec, y_rec, win_pos)


def DoWidgetAction (self, x, x_rec, y, y_rec, win_pos):

    widget_index = self.widget_active_squares.index(win_pos)
    widget_spr_index = self.widget_pile_list[widget_index]
    print ("widget_index ", widget_index, " what is count?", self.widget_pile_list_counts[widget_index])
    print ("widget_spr_index ", widget_spr_index)
    if (self.widget_pile_list_counts[widget_index] == 0):
        print ("Widget count is zero, nothing to do...")
        pass
    elif (self.picked_up):
        if (win_pos == self.picked_up_window_square):
            self.picked_up_window_square = -1
            self.picked_up = False
            self.picked_up_widget = 0
            self.picked_up_widget_index = 0
            self.picked_up_sprite.visible = False
            self.picked_up_sprite.image = self.white_bg_image
            self.picked_up_sprite_snap_back = 0
            self.picked_up_sprite_snap_back = 0
            print ("Dropped ", widget_index)
            self.cube.visible = True
        else:
            self.picked_up_window_square = win_pos
            self.picked_up_sprite.image = self.spr_mv_list[widget_spr_index][1][0]
            self.picked_up_sprite.x = x - self.half_img_pix - 4
            self.picked_up_sprite.y = y - self.half_img_pix - 4
            self.picked_up_sprite_snap_back = x_rec
            self.picked_up_sprite_snap_back = y_rec
            self.picked_up_sprite.visible = True
            self.picked_up_widget = widget_spr_index
            self.picked_up_widget_index = widget_index
            print ("Picked up other item ", widget_index)
            self.cube.visible = False
    else:
        self.picked_up_window_square = win_pos
        self.picked_up = True
        self.picked_up_sprite.image = self.spr_mv_list[widget_spr_index][1][0]
        self.picked_up_sprite.x = x - self.half_img_pix - 4
        self.picked_up_sprite.y = y - self.half_img_pix - 4
        self.picked_up_sprite_snap_back = x_rec
        self.picked_up_sprite_snap_back = y_rec
        self.picked_up_sprite.visible = True
        self.picked_up_widget = widget_spr_index
        self.picked_up_widget_index = widget_index
        print ("Picked up ", widget_index)
        self.cube.visible = False


def DoGuessAction (self, x, x_rec, y, y_rec, win_pos):

    if (self.picked_up == True):
        guess_board_index = self.board_to_window_index.index(win_pos)
        if (self.board[guess_board_index][1] != 0):
            print ("Guess board square not empty...")
        else:
            guess_index = self.guess_active_squares.index(win_pos)
            print ("guess_index ", guess_index)
            print ("picked_up_widget ", self.picked_up_widget)
            self.guess_sprites[guess_index].image = self.spr_mv_list[self.picked_up_widget][1][0]
            self.board[guess_index][1] = self.picked_up_widget
            self.widget_pile_list_counts[self.picked_up_widget_index] -= 1
            self.picked_up = False
            self.picked_up_sprite.visible = False
            print ("Put it there")
    else:
        pass


def ActiveAreaAction (self, x, x_rec, y, y_rec, win_pos):

    this.square = win_pos
    if (self.show_board == 1):
        if (win_pos in self.white_active_squares):
            print ("selected ", win_pos, " which is an active White square.")
            DoWhiteAction (self, x, x_rec, y, y_rec, win_pos)
        elif (win_pos in self.widget_active_squares):
            print ("selected ", win_pos, " which is an active Widget square.")
            DoWidgetAction (self, x, x_rec, y, y_rec, win_pos)
        elif (win_pos in self.guess_active_squares):
            print ("selected ", win_pos, " which is an active Guess square.")
            DoGuessAction (self, x, x_rec, y, y_rec, win_pos)
        else:
            pass


def ActiveAreaMouseAction (self, x, x_rec, y, y_rec, win_pos):

    if (self.show_board == 1):
        if (win_pos in self.widget_active_squares):
            if (this.square != win_pos):
                print ("moved over ", win_pos, " which is an active Widget square.")
                this.square = win_pos
            self.picked_up_sprite.x = x - self.half_img_pix - 4
            self.picked_up_sprite.y = y - self.half_img_pix - 4
            self.picked_up_sprite.visible = True
        elif (win_pos in self.guess_active_squares):
            if (this.square != win_pos):
                print ("moved over ", win_pos, " which is an active Guess square.")
                this.square = win_pos
            self.picked_up_sprite.x = x - self.half_img_pix - 4
            self.picked_up_sprite.y = y - self.half_img_pix - 4
            self.picked_up_sprite.visible = True
            self.possible_place_guess_x = x_rec
            self.possible_place_guess_y = y_rec
            self.possible_place = False
        else:
            self.picked_up_sprite.x = x_rec
            self.picked_up_sprite.y = y_rec
            self.picked_up_sprite.visible = False
    else:
        pass


