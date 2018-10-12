import pyglet


def DrawBordersAndBackgrounds (self):

    # draw four blue corner squares
    y_pos = 0
    x_pos = 0
    x_pos_right = self.img_pix * (self.game_cols+1)
    self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos))
    self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, x = x_pos_right, y = y_pos))
    y_pos = self.img_pix * (self.game_rows+1)
    self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos))
    self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, x = x_pos_right, y = y_pos))

    # draw white game border
    self.white_active_squares = []
    self.white_active_squares_position = []
    y_pos = self.img_pix
    x_pos = 0
    x_pos_right = self.img_pix * (self.game_cols+1)
    for y in range(self.game_rows):
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos))
        self.white_active_squares.append((self.window_cols * (y_pos // self.img_pix)))
        self.white_active_squares_position.append([x_pos,y_pos])
        self.dir_left.append((self.window_cols * (y_pos // self.img_pix)))
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, x = x_pos_right, y = y_pos))
        self.white_active_squares.append((self.window_cols * (y_pos // self.img_pix))+self.game_cols+1)
        self.white_active_squares_position.append([x_pos_right,y_pos])
        self.dir_right.append((self.window_cols * (y_pos // self.img_pix))+self.game_cols+1)
        y_pos += self.img_pix
    y_pos = 0
    x_pos = self.img_pix
    y_pos_up = self.img_pix * (self.game_rows+1)
    for x in range(self.game_cols):
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos))
        self.white_active_squares.append(x+1)
        self.white_active_squares_position.append([x_pos,y_pos])
        self.dir_down.append(x+1)
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos_up))
        self.white_active_squares.append(((self.window_rows-1) * self.window_cols)+x+1)
        self.white_active_squares_position.append([x_pos,y_pos_up])
        self.dir_up.append(((self.window_rows-1) * self.window_cols)+x+1)
        x_pos += self.img_pix
#    print ("White active squares", self.white_active_squares)
#    print ("White active square positions", self.white_active_squares_position)
#    print ("Left white active squares", self.dir_left)
#    print ("Right white active squares", self.dir_right)
#    print ("Up white active squares", self.dir_up)
#    print ("Down white active squares", self.dir_down)

    # draw vertical green controls
    self.control_active_squares = []
    self.control_active_squares_position = []
    x_pos = self.img_pix * (self.game_cols+2)
    y_pos = self.img_pix * (self.game_rows+1)
    win_pos = self.window_squares - (self.control_cols + 1)
    control_counter = 0
    for y in range(self.game_rows+2):
        self.green_sprites.append( pyglet.sprite.Sprite( self.green_bg_image, batch=self.green_batch, x = x_pos, y = y_pos))
        if (control_counter in range(len (self.control_images))):
            self.control_sprites.append( pyglet.sprite.Sprite( self.control_images[control_counter], batch=self.control_batch, x = x_pos, y = y_pos))
            self.control_active_squares.append(win_pos)
            self.control_active_squares_position.append([x_pos,y_pos])
            win_pos -= self.window_cols
            control_counter += 1
        y_pos -= self.img_pix
#    print ("Control active squares", self.control_active_squares)
#    print ("Control active square positions", self.control_active_squares_position)

    # put down the widget piles.  for any empty spots use 
    #    the light gray background.  alternate rows of
    #    widgets and gray background.
    # 
    # first get the list of which ones and put them on 
    #   their own list.
    widget_list = list(self.widget_pile_list)

    self.widget_active_squares = []
    self.widget_active_squares_position = []
    y_pos = self.img_pix * (self.game_rows+1)
    win_pos = self.window_squares - self.control_cols
    for x in range((self.game_rows+2)//2):
        x_pos = self.img_pix * (self.game_cols+3)
        for y in range(self.control_cols):
            try:
                spr_index = widget_list.pop(0)
                self.spr_mv_list[spr_index][2].batch = self.fixed_batch
                self.spr_mv_list[spr_index][2].x = x_pos
                self.spr_mv_list[spr_index][2].y = y_pos
                self.fixed_sprites.append( self.spr_mv_list[spr_index][2])
                self.widget_active_squares.append(win_pos+y)
                self.widget_active_squares_position.append([x_pos,y_pos])
            except:
                self.fixed_sprites.append( pyglet.sprite.Sprite( self.gray_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos))
            x_pos += self.img_pix
            if spr_index < 33:
                spr_index += 1
        y_pos -= self.img_pix*2
        win_pos -= self.window_cols*2
#    print ("Widget active squares", self.widget_active_squares)
#    print ("Widget active square positions", self.widget_active_squares_position)

    # then fill in the rest of the rows with the 
    # gray background.
    y_pos = self.img_pix * self.game_rows
    for x in range(self.game_rows+1):
        x_pos = self.img_pix * (self.game_cols+3)
        for y in range(self.control_cols):
            self.fixed_sprites.append( pyglet.sprite.Sprite( self.gray_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos))
            x_pos += self.img_pix
        y_pos -= self.img_pix*2


