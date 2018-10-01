import pyglet
from time import sleep


def DrawBoard (self):

    if (self.show_board == 2):

        self.guess_active_squares = []
        self.guess_active_squares_position = []
        self.board_to_window_index = []

        # draw game grid
        # print ("draw show board 2", self.show_board, self.board_initialized)
        y_pos = self.img_pix
#       win_pos = ((self.window_rows - 2) * self.window_cols) + 1
        win_pos = self.window_cols + 1

        self.game_board_y_limit = y_pos + self.img_pix
        for x in range(self.game_rows):
            x_pos = self.img_pix
            for y in range(self.game_cols):
                board_position = (self.game_rows * x) + y
                if (self.show_board == 2):
                    if (self.board_initialized == False):
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
        self.game_board_x_limit = x_pos
        self.board_initialized = True
        self.show_board = 1
        print ("Active guess squares", self.guess_active_squares)
        print ("Active guess square positions", self.guess_active_squares_position)
        print ("board_to_window_index", self.board_to_window_index)

    elif (self.show_board == 0):
        for j in range(len(self.board_sprites)):
            self.board_sprites[j].visible = True
        for j in range(len(self.guess_sprites)):
            self.guess_sprites[j].visible = False
        #print ("draw show board 0", len(self.board_sprites), len(self.guess_sprites), self.show_board, self.board_initialized)
    else:
        for j in range(len(self.board_sprites)):
            self.board_sprites[j].visible = False
        for j in range(len(self.guess_sprites)):
            self.guess_sprites[j].visible = True
        #print ("draw show board 1", len(self.board_sprites), len(self.guess_sprites), self.show_board, self.board_initialized)

