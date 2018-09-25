import pyglet

def DrawBordersAndBackgrounds (self):

        # draw four blue corner squares
        y_pos = 0
        x_pos = 0
        x_pos_right = self.img_pix * (self.game_cols+1)
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos, y = y_pos))
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos_right, y = y_pos))
        y_pos = self.img_pix * (self.game_rows+1)
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos, y = y_pos))
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos_right, y = y_pos))



        # draw white game border
        y_pos = self.img_pix
        x_pos = 0
        x_pos_right = self.img_pix * (self.game_cols+1)
        for y in range(self.game_rows):
          self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos, y = y_pos))
          self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos_right, y = y_pos))
          y_pos += self.img_pix
        y_pos = 0
        x_pos = self.img_pix
        y_pos_up = self.img_pix * (self.game_rows+1)
        for x in range(self.game_cols):
          self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos, y = y_pos))
          self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos, y = y_pos_up))
          x_pos += self.img_pix
    
        # draw vertical green controls
        y_pos = 0
        x_pos = 0
        x_pos_right = self.img_pix * (self.game_cols+2)
        for y in range(self.game_rows+2):
          self.fixed_sprites.append( pyglet.sprite.Sprite( self.green_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos_right, y = y_pos))
          y_pos += self.img_pix

        # put down the widget piles.  for any empty spots use 
        #    the light gray background.  alternate rows of
        #    widgets and gray background.
        # 
        # first get the list of which ones and put them on 
        #   their own list.
        widget_list = list(self.widget_pile_list)

        y_pos = self.img_pix * (self.game_rows+1)
        for x in range(self.game_rows+1):
            x_pos = self.img_pix * (self.game_cols+3)
            for y in range(self.control_cols):
                try:
                    spr_index = widget_list.pop(0)
                    self.spr_mv_list[spr_index][2].batch = self.fixed_batch
                    self.spr_mv_list[spr_index][2].group = self.background
                    self.spr_mv_list[spr_index][2].x = x_pos
                    self.spr_mv_list[spr_index][2].y = y_pos
                    self.fixed_sprites.append( self.spr_mv_list[spr_index][2])
                except:
                    self.fixed_sprites.append( pyglet.sprite.Sprite( self.gray_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos, y = y_pos))
                x_pos += self.img_pix
                if spr_index < 33:
                   spr_index += 1
            y_pos -= self.img_pix*2

        # then fill in the rest of the rows with the 
        # gray background.
        y_pos = self.img_pix * self.game_rows
        for x in range(self.game_rows+1):
            x_pos = self.img_pix * (self.game_cols+3)
            for y in range(self.control_cols):
                self.fixed_sprites.append( pyglet.sprite.Sprite( self.gray_bg_image, batch=self.fixed_batch, group=self.background, x = x_pos, y = y_pos))
                x_pos += self.img_pix
            y_pos -= self.img_pix*2

