import pyglet
from pyglet.window import mouse

from my_init import MyInitStuff
from background import DrawBordersAndBackgrounds
from randboard import InitRandomBoardItems
from board import DrawBoard
from labels import AddLabels
from active import ActiveAreaAction


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
        self.window_cols = (self.game_cols+1+self.control_cols)
        self.window_squares = self.window_rows*self.window_cols

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

        # put the cube and gcube someplace.
        # i may not need these eventually so not going to make this
        # a function for now...
        y_pos = 0
        x_pos = img_pix*6
        self.gcube = pyglet.sprite.Sprite( self.gcube_image, batch=self.pointer_bottom_batch, group=self.background, x = x_pos, y = y_pos)
        self.top_sprites.append(self.gcube)
        y_pos = 0
        x_pos = img_pix*5
        self.cube = pyglet.sprite.Sprite( self.cube_image, batch=self.pointer_top_batch, group=self.foreground, x = x_pos, y = y_pos)
        self.top_sprites.append(self.cube)

        self.picked_up = False
        self.picked_up_sprite = []

        self.alive = 1


    def on_draw(self):
        self.render()


    def on_close(self):
        self.alive = 0


    def on_mouse_press(self, x, y, button, modifiers):
        img_pix = self.img_pix
        if button == mouse.LEFT:
            print('The LEFT mouse button was pressed.', x, x // img_pix, y, y // img_pix)
            ActiveAreaAction(self, x, y)
            self.cube.x = (x // img_pix) * img_pix
            self.cube.y = (y // img_pix) * img_pix
        elif button == mouse.MIDDLE:
            print('The MIDDLE mouse button was pressed.', x, x // img_pix, y, y // img_pix)
        elif button == mouse.RIGHT:
            print('The RIGHT mouse button was pressed.', x, x // img_pix, y, y // img_pix)
            self.gcube.x = (x // img_pix) * img_pix
            self.gcube.y = (y // img_pix) * img_pix


    def on_mouse_release(self, x, y, button, modifiers):
        print ("The mouse was released")


    def on_mouse_motion(self, x, y, dx, dy):
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
            print ("The 'F1' key was pressed")
            # after the initial showing of the background we
            # don't ever need to see the background again so 
            # only toggle between the game board and the guess 
            # board (0 or 1)...
            self.show_board = (self.show_board + 1) % 2


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
    window.game_board_x_limit, window.game_board_y_limit
    )

