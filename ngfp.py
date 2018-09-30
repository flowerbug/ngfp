import pyglet
from pyglet.window import mouse

from my_init import MyInitStuff
from background import DrawBordersAndBackgrounds
from randboard import InitRandomBoardItems
from board import DrawBoard
from labels import AddLabels
from active import ActiveAreaAction, ActiveAreaMouseAction


class main(pyglet.window.Window):

    def __init__ (
            self,
            width=64*16,
            height=64*10,
            fps=False,
            *args,
            **kwargs):

        # to start with, i'm not sure yet how this works when
        # i want to change it during the game...
        #    width=(game_cols+control_cols+3)*img_pix
        #    height=(game_rows+2)*img_pix

        super(main, self).__init__(width, height, *args, **kwargs)

        # some of these will come from the configuration file 
        # when i get that working.  until then this will have
        # to do...
        game_cols = 8
        game_rows = 8
        board_squares = game_rows*game_cols
        control_cols = 5
        img_pix = 64

        self.game_rows = game_rows
        self.game_cols = game_cols
        self.board_squares = self.game_rows*self.game_cols
        self.control_cols = control_cols
        self.img_pix = img_pix
        self.window_rows = (self.game_rows+2)
        self.window_cols = (self.game_cols+self.control_cols+3)
        self.window_squares = self.window_rows*self.window_cols

        # temporary to help with testing things out
        self.use_test_board = True

        MyInitStuff (self)

        if (self.use_test_board):
            print (self.test_board)
        else:
            print (self.board)
        print (self.pic_list)
        print (self.spr_mv_list)

        InitRandomBoardItems (self)

        DrawBordersAndBackgrounds (self)
        DrawBoard (self)

        # put the gcube and cube someplace.
        # i may not need these eventually so not going to make this
        # a function for now...
        x_pos = self.img_pix * (self.game_cols+1)
        y_pos = 0
        self.gcube = pyglet.sprite.Sprite( self.gcube_image, batch=self.pointer_bottom_batch, x = x_pos, y = y_pos)
        self.top_sprites.append(self.gcube)
        x_pos = 0
        y_pos = 0
        self.cube = pyglet.sprite.Sprite( self.cube_image, batch=self.pointer_top_batch, x = x_pos, y = y_pos)
        self.top_sprites.append(self.cube)

        self.picked_up = False
        self.picked_up_window_square = -1
        self.picked_up_sprite = pyglet.sprite.Sprite( self.game_bg_image, batch=self.pointer_top_batch, x = 0, y = 0)
        self.picked_up_sprite.visible = False
        self.picked_up_sprite.opacity = 150

        self.alive = 1


    def on_draw(self):
        self.render()


    def on_close(self):
        self.alive = 0


    def on_mouse_press(self, x, y, button, modifiers):

        img_pix = self.img_pix
        x_win = x // img_pix
        x_rec = x_win * img_pix
        y_win = y // img_pix
        y_rec = y_win * img_pix
        win_pos = (y_win * self.window_cols) + x_win
        
        if button == mouse.LEFT:
            print('The LEFT mouse button was pressed.', x, x_rec, x_win, y, y_rec, y_win, win_pos)
            ActiveAreaAction(self, x, x_rec, y, y_rec, win_pos)
        elif button == mouse.MIDDLE:
            print('The MIDDLE mouse button was pressed.', x, x_rec, x_win, y, y_rec, y_win, win_pos)
        elif button == mouse.RIGHT:
            print('The RIGHT mouse button was pressed.', x, x_rec, x_win, y, y_rec, y_win, win_pos)
            self.gcube.x = x_rec
            self.gcube.y = y_rec


    def on_mouse_release(self, x, y, button, modifiers):
        print ("The mouse was released")


    def on_mouse_motion(self, x, y, dx, dy):

        img_pix = self.img_pix
        x_win = x // img_pix
        x_rec = x_win * img_pix
        y_win = y // img_pix
        y_rec = y_win * img_pix
        win_pos = (y_win * self.window_cols) + x_win
        
        if (self.picked_up):
            ActiveAreaMouseAction(self, x, x_rec, y, y_rec, win_pos)
        else:
            pass


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass


    def on_mouse_leave(self, x, y):
        pass


    def on_mouse_enter(self, x, y):
        pass


    def on_key_press(self, symbol, modifiers):

        self.keys_held.append(symbol)
        if ((symbol == pyglet.window.key.ESCAPE) or (symbol == pyglet.window.key.Q)): # [ESC] or [Q]
            print ("The 'ESC' or 'Q' key was pressed")
            self.alive = 0
        elif symbol == pyglet.window.key.LEFT:
            if self.cube.x > 0:
                self.cube.x -= self.img_pix
            print ("The 'LEFT' key was pressed")
        elif symbol == pyglet.window.key.RIGHT:
            if self.cube.x < self.game_board_x_limit:
                self.cube.x += self.img_pix
            print ("The 'RIGHT' key was pressed")
        elif symbol == pyglet.window.key.UP:
            if self.cube.y < self.game_board_y_limit:
                self.cube.y += self.img_pix
            print ("The 'UP' key was pressed")
        elif symbol == pyglet.window.key.DOWN:
            if self.cube.y > 0:
                self.cube.y -= self.img_pix
            print ("The 'DOWN' key was pressed")
        elif symbol == pyglet.window.key.F1:
            print ("The 'F1' key was pressed, show board ", self.show_board)
            # after the initial showing of the background we
            # don't ever need to see the background again so 
            # only toggle between the game board and the guess 
            # board (0 or 1)...
            self.show_board = (self.show_board + 1) % 2
            if ((self.show_board == 0) and (self.picked_up == True)):
                self.picked_up_sprite.visible = False
            elif ((self.show_board == 1) and (self.picked_up == True)):
                self.picked_up_sprite.visible = True
            print ("The 'F1' key was pressed, show board changed to ", self.show_board)


    def on_key_release(self, symbol, modifiers):
        try:
            self.keys_held.pop(self.keys_held.index(symbol))
            print ("The key was released")
        except:
            pass


    def render(self):
        ## == Clear the frame
        self.clear()

        DrawBoard (self)

        AddLabels(self)

        self.fixed_batch.draw()
        self.fixed_board_batch.draw()
        self.variable_board_batch.draw()
        self.variable_guess_batch.draw()
        self.pointer_bottom_batch.draw()
        self.pointer_top_batch.draw()
        self.text_batch.draw()

        self.fps.draw()

        ## == And flip the current buffer to become the active viewed buffer.
        self.flip()


    def run(self):
        while self.alive == 1:
            self.render()

            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()


window = main()

"""
window.push_handlers(pyglet.window.event.WindowEventLogger())
"""

window.run()

game_x, game_y = window.get_location()

print (
    window.screen_width, window.screen_height,
    window.game_x_offset, window.game_y_offset,
    game_x, game_y,
    window.game_board_x_limit, window.game_board_y_limit,
    window.board
    )

