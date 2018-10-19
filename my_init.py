import pyglet
import copy
import random

from labels import AddLabels


def MyInitStuff (self):

    random.seed()

    display = pyglet.canvas.get_display()
    screen = display.get_default_screen()
    self.screen_width = screen.width
    self.screen_height = screen.height

    self.game_x_offset = (self.screen_width//2) - (((self.game_cols+self.control_cols+4)//2) * self.img_pix)
    self.game_y_offset = (self.screen_height//2) - (((self.game_rows+6)//2) * self.img_pix)

    self.x, self.y = self.get_location()
    self.set_location(self.x + self.game_x_offset, self.y + self.game_y_offset)

    self.half_img_pix = self.img_pix // 2

    # animation pixels moved (it must be a factor of img_pix otherwise
    #   the marble won't match with the grid of coordinates - i.e. there's
    #   no wiggle room in the collision detection)...
    self.tic_pix = self.img_pix // 2

    self.game_board_x_limit = 0
    self.game_board_y_limit = 0

    self.keys_held = []
    self.key = pyglet.window.key

    self.fps = pyglet.window.FPSDisplay(self)

    # batches for rendering
    self.fixed_batch = pyglet.graphics.Batch()
    self.green_batch = pyglet.graphics.Batch()
    self.control_batch = pyglet.graphics.Batch()
    self.fixed_board_batch = pyglet.graphics.Batch()
    self.variable_board_batch = pyglet.graphics.Batch()
    self.variable_guess_batch = pyglet.graphics.Batch()
    self.pointer_bottom_batch = pyglet.graphics.Batch()
    self.pointer_top_batch = pyglet.graphics.Batch()
    self.text_batch = pyglet.graphics.Batch()
    self.arrow_batch = pyglet.graphics.Batch()
    self.marble_batch = pyglet.graphics.Batch()

    # colors need precedence order for arrows
    #   we only use as many colors to mark arrows we keep in history
    self.history_limit = 6
    self.color_batch_list = []
    for i in range(self.history_limit):
        self.color_batch_list.append(pyglet.graphics.Batch())

    # lists of sprites
    self.fixed_sprites = []
    self.green_sprites = []
    self.control_sprites = []
    self.top_sprites = []
    self.arrow_history_sprites = []
    self.history_color_sprites = []
    self.marble_sprites = []
    self.text_sprites = []

    # to make sure we only do the background and fixed sprites once
    # and to set up certain tuples/lists once...
    self.board_initialized = False

    # which board to show, a toggle between 0, 1  when Key F1 is pressed
    # 0 - puzzle to solve
    # 1 - guesses placed
    # 2 - blank background
    #
    self.show_board = 2

    self.board = [[0 for i in range(2)] for j in range(self.board_squares)]

    if (self.use_test_board):
        self.test_board = [[0 for i in range(2)] for j in range(self.board_squares)]
        local_counts = [1, 1, 2, 4, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 4, 4, 1, 1]
#        local_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        if (self.board_squares >= 32):
#            for i in range(1):
#                self.test_board[i] = [i+32, 0]
            for i in range(32):
                self.test_board[i] = [i+1, 0]
            self.test_widget_pile_list_counts = copy.deepcopy(local_counts)
        else:
            self.test_widget_pile_list_counts = copy.deepcopy(local_counts[:self.board_squares])
            for i in range(self.board_squares):
                self.test_board[i] = [i+1, 0]
    else:
        self.test_board = []
        self.test_widget_pile_list_counts = []

    self.game_bg_image  = pyglet.image.load("png/mirrors/00_bg.png")
    self.white_bg_image = pyglet.image.load("png/backgrounds/wbg.png")
    self.blue_bg_image  = pyglet.image.load("png/backgrounds/bbg.png")
    self.green_bg_image = pyglet.image.load("png/backgrounds/lgbg.png")
    self.gray_bg_image  = pyglet.image.load("png/backgrounds/gbg.png")

    self.gcube_image = pyglet.image.load("png/misc/gcube.png")
    self.gcube = pyglet.sprite.Sprite(self.gcube_image, x=self.img_pix, y=0)
    self.cube_image  = pyglet.image.load("png/misc/cube.png")
    self.cube = pyglet.sprite.Sprite(self.cube_image, x=self.img_pix, y=0)

    self.pic_control_list = [
        "png/controls/picINew.png",
        "png/controls/picICheck.png",
        "png/controls/picIFlipBoards.png",
        "png/controls/picIOpen.png",
        "png/controls/picISave.png",
        "png/controls/picIAbout.png"
        ]

    self.control_images = []
    for i in range(len(self.pic_control_list)):
        self.control_images.append(pyglet.image.load(self.pic_control_list[i]))

    self.pic_marbles_list = [
        "png/marbles/red_marbles.png",
        "png/marbles/green_marbles.png",
        "png/marbles/blue_marbles.png",
        "png/marbles/yellow_marbles.png",
        "png/marbles/purple_marbles.png",
        "png/marbles/black_marbles.png"
        ]

    self.marble_images = []
    for i in range(len(self.pic_marbles_list)):
        self.marble_images.append(pyglet.image.load(self.pic_marbles_list[i]))

    self.pic_color_list = [
        "png/colors/red_half.png",
        "png/colors/green_half.png",
        "png/colors/blue_half.png",
        "png/colors/yellow_half.png",
        "png/colors/purple_half.png",
        "png/colors/black_half.png"
        ]

    self.color_images = []
    for i in range(len(self.pic_color_list)):
        self.color_images.append(pyglet.image.load(self.pic_color_list[i]))

    self.pic_arrow_list = [
        "png/arrows/picDLeftW.png",
        "png/arrows/picDRightW.png",
        "png/arrows/picDUpW.png",
        "png/arrows/picDDownW.png"
        ]

    self.arrow_images = []
    for i in range(len(self.pic_arrow_list)):
        self.arrow_images.append(pyglet.image.load(self.pic_arrow_list[i]))

    # arrow history list and current index, set up colors and marbles too...
    self.arrow_index = 0
    self.anim = []
    self.marble_seq = []
    for i in range(self.history_limit):

        spr_a = pyglet.sprite.Sprite(self.arrow_images[0], batch=self.arrow_batch)
        spr_a.visible = False
        spr_b = pyglet.sprite.Sprite(self.arrow_images[0], batch=self.arrow_batch)
        spr_b.visible = False
        self.arrow_history_sprites.append([spr_a, spr_b])

        spr_c = pyglet.sprite.Sprite(self.color_images[i], batch=self.color_batch_list[i])
        spr_c.visible = False
        spr_d = pyglet.sprite.Sprite(self.color_images[i], batch=self.color_batch_list[i])
        spr_d.visible = False
        self.history_color_sprites.append([spr_c, spr_d])

        self.marble_seq.append(pyglet.image.ImageGrid(self.marble_images[i], 1, 16))
        self.anim.append(pyglet.image.Animation.from_image_sequence(self.marble_seq[i], 0.02, True))
        spr_e = pyglet.sprite.Sprite(self.anim[i], batch=self.marble_batch)
        spr_e.visible = True
        spr_e.x = 0
        spr_e.y = 0
        spr_e.dx = 0
        spr_e.dy = 0
        self.marble_sprites.append(spr_e)

    self.pic_list = [
        "png/mirrors/00_bg.png",           # background
        "png/mirrors/01_normal.png",       # simple mirrors: left: \
        "png/mirrors/02_normal.png",       # simple mirrors: right: /
        "png/mirrors/03_flip2.png",        # simple flipping mirrors: left: \
        "png/mirrors/04_flip2.png",        # simple flipping mirrors: right: /
        "png/mirrors/05_flip4.png",        # quad flipping mirrors: left: \
        "png/mirrors/06_flip4.png",        # quad flipping mirrors: bounce: o
        "png/mirrors/07_flip4.png",        # quad flipping mirrors: right: /
        "png/mirrors/08_flip4.png",        # quad flipping mirrors: bounce: o
        "png/mirrors/09_block.png",        # box and sink: box: bounce: o  (reflect all)
        "png/mirrors/10_sink.png",         # box and sink: sink: grab: x  (absorb all)
        "png/mirrors/11_axial.png",        # axial mirrors: simple vertical: |
        "png/mirrors/12_axial.png",        # axial mirrors: simple horizontal: -
        "png/mirrors/13_axial2.png",       # axial mirrors: flipping vertical: ||
        "png/mirrors/14_axial2.png",       # axial mirrors: flipping horizontal: =
        "png/mirrors/15_rotator.png",      # rotators simple counterclockwise: left: \\
        "png/mirrors/16_rotator.png",      # rotators simple clockwise: right: //
        "png/mirrors/17_rotator2.png",     # rotators flipper clockwise: left: []
        "png/mirrors/18_rotator2.png",     # rotators flipper counterclockwise: right: ][
        "png/mirrors/19_half.png",         # 1-way mirrors: left: lower reflects: \<-
        "png/mirrors/20_half.png",         # 1-way mirrors: left: upper reflects: ->\
        "png/mirrors/21_half.png",         # 1-way mirrors: right: lower reflects: ->/
        "png/mirrors/22_half.png",         # 1-way mirrors: right: upper reflects: /<-
        "png/mirrors/23_half4.png",        # flipping 1-way mirrors: left: lower reflects: rotates clockwise: \\\<-
        "png/mirrors/24_half4.png",        # flipping 1-way mirrors: right: upper reflects: rotates clockwise: ///<-
        "png/mirrors/25_half4.png",        # flipping 1-way mirrors: left: upper reflects: rotates clockwise: ->\\\
        "png/mirrors/26_half4.png",        # flipping 1-way mirrors: right: lower reflects: rotates clockwise: ->///
        "png/mirrors/27_half4.png",        # flipping 1-way mirrors: left: upper reflects: rotates counterclockwise: ->\\\
        "png/mirrors/28_half4.png",        # flipping 1-way mirrors: right: upper reflects: rotates counterclockwise: ///<-
        "png/mirrors/29_half4.png",        # flipping 1-way mirrors: left: lower reflects: rotates counterclockwise: \\\<-
        "png/mirrors/30_half4.png",        # flipping 1-way mirrors: right: lower reflects: rotates counterclockwise: ->///
        "png/mirrors/31_move.png",         # moving mirror: left: -->\X\--> ---->\X\
        "png/mirrors/32_move.png",         # moving mirror: right: <--/X/<-- /X/<----
        "png/mirrors/33_bg.png"            # background
        ]

    self.spr_mv_list = []

    for i in range(len(self.pic_list)):
        image = pyglet.image.load(self.pic_list[i])
        sprite = pyglet.sprite.Sprite(image)
        self.spr_mv_list.append([0, image, sprite, 0, 0])

    # these flags are for the widget pile list
    #     position is taken from widget list location index
    #     when self.widget_pile_list_counts[position] != 0 then the index
    #        can be used to get the number from this list to index into
    #         self.spr_mv_list for the image or sprite or ...
    self.widget_pile_list = [1,2,3,5,9,10,11,12,13,15,16,17,19,20,21,22,23,27,31,32]
    for i in self.widget_pile_list:
        self.spr_mv_list[i][0] = 1
    self.widget_pile_list_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    # eventually we're going to have to index any widget no matter how it
    # is rotated...
    self.widget_lookup_table = [0, 1, 2, 
                                3, 3,
                                4, 4, 4, 4,
                                5, 6, 7, 8,
                                9, 9,
                                10, 11,
                                12, 12,
                                13, 14, 15, 16,
                                17, 17, 17, 17,
                                18, 18, 18, 18,
                                19, 20
                               ]

    # speaking of rotating, we need to know how many places it 
    #   rotates through - of course 0 means it doesn't rotate at all
    # note that this aligns with self.widget_lookup_table
    self.widget_rotate_modulus = [0,0,0,2,4,0,0,0,0,2,0,0,2,0,0,0,0,4,4,0,0]

    # this says what the next widget will be in the sequence if it isn't 0
    self.widget_next_widget = [
    #   0 1 2 3 4 5 6 7 8 9 0 1 2
        0,0,0,4,3,6,7,8,5,0,0,0,0,
        14,13,0,0,18,17,
        0,0,0,0,
    #   23-26 
        24, 25, 26, 23,
    #   27-30
        28, 29, 30, 27,
    #   31, 32
        0, 0]

    # these flags are for the configuration of each group percentages images list
    self.config_percent_list = [1,2,3,5,9,10,11,14,15,18,19,22,23,31]
    for i in self.config_percent_list:
        self.spr_mv_list[i][3] = 1

    self.widget_labels = []

    # 0 = nowhere, 1 = widget, 2 = board
    self.picked_up_from = 0
    self.picked_up = False

    # direction sets will make things easier later
    self.dir_left = []
    self.dir_right = []
    self.dir_up = []
    self.dir_down = []

    # some kind of limit to break out of loops
    self.tick_limit = 100 + (self.board_squares * 2)

    # we only need to do the Labels once
    AddLabels (self)
