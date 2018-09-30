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


def WidgetPutClear (self):

    self.picked_up = False
    self.picked_up_from = 0
    self.picked_up_window_square = -1
    self.picked_up_widget = 0
    self.picked_up_widget_index = 0
    self.picked_up_sprite.image = self.white_bg_image
    self.picked_up_sprite.x = 0
    self.picked_up_sprite.y = 0
    self.picked_up_sprite.visible = False
   
    self.picked_up_sprite_snap_back_x = 0
    self.picked_up_sprite_snap_back_y = 0

    # put the cube home
    self.cube.x = 0
    self.cube.y = 0
    self.cube.visible = True


def WidgetPick (self, x, x_rec, y, y_rec, win_pos, pick_from, widget_index, widget_spr_index):

    self.picked_up = True
    self.picked_up_from = pick_from
    self.picked_up_window_square = win_pos
    self.picked_up_widget = widget_spr_index
    self.picked_up_widget_index = widget_index
    self.picked_up_sprite.image = self.spr_mv_list[widget_spr_index][1][0]
    self.picked_up_sprite.x = x - self.half_img_pix - 4
    self.picked_up_sprite.y = y - self.half_img_pix - 4
    self.picked_up_sprite.visible = True
   
    self.picked_up_sprite_snap_back_x = x_rec
    self.picked_up_sprite_snap_back_y = y_rec
  
    # something in progress hide cube
    self.cube.visible = False


def DoWidgetAction (self, x, x_rec, y, y_rec, win_pos):

    widget_index = self.widget_active_squares.index(win_pos)
    widget_spr_index = self.widget_pile_list[widget_index]
    print ("widget_index ", widget_index, " what is count?", self.widget_pile_list_counts[widget_index])
    print ("widget_spr_index ", widget_spr_index)
    if ((self.picked_up_from == 0) or (self.picked_up_from == 1)):
        if (self.widget_pile_list_counts[widget_index] == 0):
            print ("Widget count is zero, nothing to do...")
        elif (self.picked_up == True):
            if (win_pos == self.picked_up_window_square):

                WidgetPutClear (self)
                print ("Dropped ", widget_index)
            else:

                WidgetPick (self, x, x_rec, y, y_rec, win_pos, 1, 
                    widget_index, widget_spr_index)
                print ("Picked up other widget ", widget_index)
        else:
            WidgetPick (self, x, x_rec, y, y_rec, win_pos, 1, 
                widget_index, widget_spr_index)
            print ("Picked up ", widget_index)
    elif (self.picked_up_from == 2):
        print ("widget to put back", self.picked_up_widget)
        WidgetPutClear (self)


def GuessPut (self, x, x_rec, y, y_rec, win_pos, board_index):

    self.guess_sprites[board_index].image = self.spr_mv_list[self.picked_up_widget][1][0]
    self.board[board_index][1] = self.picked_up_widget
    if (self.picked_up_from == 1):
        self.widget_pile_list_counts[self.picked_up_widget_index] -= 1

    WidgetPutClear (self)


def GuessPick (self, x, x_rec, y, y_rec, win_pos, board_index):

    self.picked_up = True
    self.picked_up_from = 2
    self.picked_up_window_square = win_pos
    self.picked_up_widget = self.board[board_index][1]
    self.picked_up_sprite.image = self.guess_sprites[board_index].image
    self.guess_sprites[board_index].image = self.game_bg_image
    self.board[board_index][1] = 0
    self.picked_up_widget_index = self.widget_lookup_table[self.picked_up_widget] - 1
    self.widget_pile_list_counts[self.picked_up_widget_index] += 1
    self.picked_up_sprite.x = x - self.half_img_pix - 4
    self.picked_up_sprite.y = y - self.half_img_pix - 4
    self.picked_up_sprite.visible = True
   
    self.picked_up_sprite_snap_back_x = x_rec
    self.picked_up_sprite_snap_back_y = y_rec


def DoGuessAction (self, x, x_rec, y, y_rec, win_pos):

    guess_board_index = self.board_to_window_index.index(win_pos)
    print ("Clicked on square ", guess_board_index)

    if (self.picked_up_from == 1):
        if (self.board[guess_board_index][1] != 0):
            print ("Guess board square not empty...")
        else:
            GuessPut (self, x, x_rec, y, y_rec, win_pos, guess_board_index)
            print ("Put it on the board")
    else:
        if (self.board[guess_board_index][1] == 0):
            print ("Guess board is empty...  Nothing to move or remove...")
        else:
            GuessPick (self, x, x_rec, y, y_rec, win_pos, guess_board_index)
            self.picked_up_from = 1
            print ("Moving or Removing...")


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
        else:
            self.picked_up_sprite.x = x_rec
            self.picked_up_sprite.y = y_rec
            self.picked_up_sprite.visible = False
    else:
        pass


