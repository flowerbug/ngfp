import pyglet
import sys


def UpdateAndShowArrow (self, image, spot, xy_coord, rotate):

    print ("Update Arrow  arrow_index ", self.arrow_index,
        " spot, ", spot ," coord", xy_coord)

    self.arrow_history_sprites[self.arrow_index][spot].x = xy_coord[0]
    self.arrow_history_sprites[self.arrow_index][spot].y = xy_coord[1]
    self.arrow_history_sprites[self.arrow_index][spot].image = image
    self.arrow_history_sprites[self.arrow_index][spot].visible = True

    self.history_color_sprites[self.arrow_index][spot].rotation = rotate
    self.history_color_sprites[self.arrow_index][spot].x = xy_coord[0]
    if (rotate == 0.0):
        self.history_color_sprites[self.arrow_index][spot].y = xy_coord[1]
    else:
        self.history_color_sprites[self.arrow_index][spot].y = xy_coord[1] + self.half_img_pix
    self.history_color_sprites[self.arrow_index][spot].visible = True


def HistoryNext (self):

    self.arrow_index = (self.arrow_index + 1) % self.history_limit


