import pyglet
from time import sleep


def DrawBoard (self):

    if (self.show_board == 2):

        self.board_initialized = False

        try:
            del self.fixed_board_sprites
        except AttributeError:
            pass
        self.fixed_board_sprites = []
        try:
            del self.board_sprites
        except AttributeError:
            pass
        self.board_sprites = []
        try:
            del self.guess_sprites
        except AttributeError:
            pass
        self.guess_sprites = []

        try:
            del self.guess_active_squares
        except AttributeError:
            pass
        self.guess_active_squares = []
        try:
            del self.guess_active_squares_position
        except AttributeError:
            pass
        self.guess_active_squares_position = []
        try:
            del self.board_to_window_index
        except AttributeError:
            pass
        self.board_to_window_index = []

        # draw game grid
        print ("draw show board 2", self.show_board, self.board_initialized)
        y_pos = self.img_pix
        x_pos = self.img_pix
        self.game_board_x_lower_limit = x_pos
        self.game_board_y_lower_limit = y_pos
#       win_pos = ((self.window_rows - 2) * self.window_cols) + 1
        win_pos = self.window_cols + 1

        for x in range(self.game_rows):
            x_pos = self.game_board_x_lower_limit
            for y in range(self.game_cols):
                board_position = (self.game_rows * x) + y
                self.fixed_board_sprites.append( pyglet.sprite.Sprite( self.game_bg_image, batch=self.fixed_board_batch, x = x_pos, y = y_pos))
                image = self.spr_mv_list[self.board[board_position][0]][1]
                self.board_sprites.append( pyglet.sprite.Sprite( image, batch=self.variable_board_batch, x = x_pos, y = y_pos))
                image = self.spr_mv_list[self.board[board_position][1]][1]
                self.guess_sprites.append( pyglet.sprite.Sprite( image, batch=self.variable_guess_batch, x = x_pos, y = y_pos))
                self.guess_active_squares.append(win_pos)
                self.guess_active_squares_position.append([x_pos,y_pos])
                self.board_to_window_index.append(win_pos)
                x_pos += self.img_pix
                win_pos += 1
            y_pos += self.img_pix
            win_pos += (self.control_cols + 3)
        self.game_board_x_upper_limit = x_pos
        self.game_board_y_upper_limit = y_pos
        self.board_initialized = True
        self.show_board = 1
        print ("Guess active squares", self.guess_active_squares)
        print ("Guess active square positions", self.guess_active_squares_position)
        print ("board_to_window_index", self.board_to_window_index)
        print ("game board limits ", self.game_board_x_lower_limit, self.game_board_x_upper_limit,
            self.game_board_y_lower_limit, self.game_board_y_upper_limit)
        print ("board ", self.board)
        print ("widget_pile_list_counts ", self.widget_pile_list_counts)


    elif (self.show_board == 0):
        for j in range(len(self.board_sprites)):
            self.board_sprites[j].visible = True
        for j in range(len(self.guess_sprites)):
            self.guess_sprites[j].visible = False
#        print ("draw show board 0", len(self.board_sprites), len(self.guess_sprites), self.show_board, self.board_initialized)
    else:
        for j in range(len(self.board_sprites)):
            self.board_sprites[j].visible = False
        for j in range(len(self.guess_sprites)):
            self.guess_sprites[j].visible = True
#        print ("draw show board 1", len(self.board_sprites), len(self.guess_sprites), self.show_board, self.board_initialized)


