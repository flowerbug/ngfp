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
import copy
import config as cfg


def AddLabels (self):

    w_limit = len(self.widget_pile_list_counts)-1
    w = 0

#    print ("WL len ", len(self.widget_labels))
#    print ("WPLC len ", len(self.widget_pile_list_counts))

    if (len(self.widget_labels) != 0):
#        print ("Removing Existing Widget Labels")
        for j in range(len(self.widget_labels)):
            self.widget_labels[j].visible = False
            self.widget_labels[j].delete()
        del self.widget_labels
        self.widget_labels = []

    y_pos = cfg.img_pix * (cfg.game_rows)
    for i in range(cfg.game_rows+1):
        x_pos = cfg.img_pix * (cfg.game_cols+3)
        for j in range(cfg.control_cols):
            if ((i % 2) == 0):
                if (w < w_limit):
                    count_str = str(self.widget_pile_list_counts[w])
                    self.widget_labels.append(pyglet.text.Label(
                        count_str,
                        font_name="Sans Regular",
                        font_size=28,
                        bold=True,
                        color=[245, 0, 0, 255],
                        width=cfg.img_pix, height=cfg.img_pix,
                        x=x_pos+34, y=y_pos+24,
                        anchor_x="center", anchor_y="center",
                        batch=self.text_batch))
                    w += 1
                x_pos += cfg.img_pix
        y_pos -= cfg.img_pix


def UpdateLabels (self):

#    print ("UPDTL WL len ", len(self.widget_labels))
#    print ("UPDTL WPLC len ", len(self.widget_pile_list_counts))

    for w in range(len(self.widget_labels)):
        self.widget_labels[w].text = str(self.widget_pile_list_counts[w])


