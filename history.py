#
#
# Copyright [2018] [Ant <ant@anthive.com>]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
import pyglet
import sys
import config as cfg


def HideInArrow (self):

#    print ("HideInArrow ", self.arrow_index)
    self.arrow_history_sprites[self.arrow_index][0].visible = False
    self.history_color_sprites[self.arrow_index][0].visible = False


def HideOutArrow (self):

#    print ("HideOutArrow ", self.arrow_index)
    self.arrow_history_sprites[self.arrow_index][1].visible = False
    self.history_color_sprites[self.arrow_index][1].visible = False


def HideBothArrows (self):

#    print ("HideBothArrows ", self.arrow_index)
    HideInArrow (self)
    HideOutArrow (self)


def UpdateAndShowArrow (self, image, spot, xy_coord, rotate, visible):

#    print ("Update Arrow  arrow_index ", self.arrow_index,
#        " spot, ", spot ," coord", xy_coord)

    self.arrow_history_sprites[self.arrow_index][spot].x = xy_coord[0]
    self.arrow_history_sprites[self.arrow_index][spot].y = xy_coord[1]
    self.arrow_history_sprites[self.arrow_index][spot].image = image
    self.arrow_history_sprites[self.arrow_index][spot].visible = visible

    self.history_color_sprites[self.arrow_index][spot].rotation = rotate
    self.history_color_sprites[self.arrow_index][spot].x = xy_coord[0]
    if (rotate == 0.0):
        self.history_color_sprites[self.arrow_index][spot].y = xy_coord[1]
    else:
        self.history_color_sprites[self.arrow_index][spot].y = xy_coord[1] + cfg.half_img_pix
    self.history_color_sprites[self.arrow_index][spot].visible = visible


def HistoryNext (self):

    self.arrow_index = (self.arrow_index + 1) % self.history_limit


def HistoryAndMarbleShift (self):

    # we need to rotate both the arrows and marbles together
    self.color_batch_list.append(self.color_batch_list.pop(0))
    self.marble_sprites.append(self.marble_sprites.pop(0))


