import pyglet


def DrawBoard (self):

    # make previous sprites invisible
    if (self.show_board == 2):
        # may eventually need to change this
        #     to clear in between new games...
        pass
    elif (self.show_board == 0):
        for j in range(len(self.board_sprites)):
            self.board_sprites[j].visible = True
        for j in range(len(self.guess_sprites)):
            self.guess_sprites[j].visible = False
    else:
        for j in range(len(self.board_sprites)):
            self.board_sprites[j].visible = False
        for j in range(len(self.guess_sprites)):
            self.guess_sprites[j].visible = True

    # draw game grid
    y_pos = self.img_pix*self.game_rows
    self.game_board_y_limit = y_pos + self.img_pix
    game_loc = 0
    for x in range(self.game_rows):
        x_pos = self.img_pix
        for y in range(self.game_cols):
            if (self.show_board == 2):
                if (not(self.board_initialized)):
                    self.fixed_sprites.append( pyglet.sprite.Sprite( self.game_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos, y = y_pos))
            elif (self.show_board == 0):
                board_position = (self.game_rows * x) + y
                image = self.spr_mv_list[self.board[board_position][self.show_board]][1][0]
                if (not(self.board_initialized)):
                    self.board_sprites.append( pyglet.sprite.Sprite( image, batch=self.variable_board_batch, group=self.background, x = x_pos, y = y_pos))
                else:
                    self.board_sprites.update( pyglet.sprite.Sprite( image, batch=self.variable_board_batch, group=self.background, x = x_pos, y = y_pos))
            else:
                board_position = (self.game_rows * x) + y
                image = self.spr_mv_list[self.board[board_position][self.show_board]][1][0]
                if (not(self.board_initialized)):
                    self.guess_sprites.append( pyglet.sprite.Sprite( image, batch=self.variable_guess_batch, group=self.background, x = x_pos, y = y_pos))
                else:
                    self.guess_sprites.update( pyglet.sprite.Sprite( image, batch=self.variable_guess_batch, group=self.background, x = x_pos, y = y_pos))
            x_pos += self.img_pix
            game_loc += 1
        y_pos -= self.img_pix
    self.game_board_x_limit = x_pos
    if (not(self.board_initialized)):
        self.board_initialize = True

