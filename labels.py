import pyglet
import copy
from time import sleep


def AddLabels (self):

    if (len(self.widget_labels) == 0):
        self.widget_count_list = copy.deepcopy(self.widget_pile_list_counts)
        y_pos = self.img_pix * (self.game_rows)
        for i in range(self.game_rows+1):
            x_pos = self.img_pix * (self.game_cols+3)
            for j in range(self.control_cols):
                if ((i % 2) == 0):
                    try:
                        count_str = str(self.widget_count_list.pop(0))
                        self.widget_labels.append(pyglet.text.Label(
                            count_str,
                            font_name='Sans Regular',
                            font_size=28,
                            bold=True,
                            color=[245, 0, 0, 255],
                            width=self.img_pix, height=self.img_pix,
                            x=x_pos+34, y=y_pos+24,
                            anchor_x='center', anchor_y='center',
                            batch=self.text_batch))
                    except:
                        break
                x_pos += self.img_pix
            y_pos -= self.img_pix
    else:
        del self.widget_labels
        self.widget_labels = []
