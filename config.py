from pathlib import Path, PurePath
import os
import configparser


"""
Example Code:


with open('config.json', 'r') as f:
    config = json.load(f)

secret_key = config['DEFAULT']['SECRET_KEY'] # 'secret-key-of-myapp'
ci_hook_url = config['CI']['HOOK_URL'] # 'web-hooking-url-from-ci-service'

"""


#   save game location and initial file
# you can always save/load other names, 
# this is just a suggestion...

filename_to_open = "save.json"
filename_to_save = None
if (os.name == "posix"):
    home = Path.home()
    data_path = home / Path(".local/share/ngfp")
else:
    print ("  Ngfp doesn't know where to set data_path for OS : ", os.name)
    print ("This is where a user would save their games.")


# configure location and file
config_filename = "config_ngfp.json"
if (os.name == "posix"):
    home = Path.home()
    config_path = home / Path(".config/ngfp")
else:
    print ("  Ngfp doesn't know where to set config_path for OS : ", os.name)
    print ("This is where the game saves configuration parameters.")


# save the current directory so we can get back
saved_dir = None


# current, default and changed parameters

game_cols = 8     # width
game_rows = 8     # height
density = 25      # percent of the board filled up modified by density_fuzz
density_fuzz = 10
class_weights = [100, 75, 5, 5, 5, 15, 5]

default_game_cols = 8     # width
default_game_rows = 8     # height
default_density = 25      # percent of the board filled up modified by density_fuzz
default_density_fuzz = 10
default_class_weights = [100, 75, 5, 5, 5, 15, 5]

new_game_cols = 8   # width
new_game_rows = 8   # height
new_density = 25    # percent of the board filled up modified by density_fuzz
new_density_fuzz = 10
new_class_weights = [100, 75, 5, 5, 5, 15, 5]


# labels for configuration dialog

property_labels = [
    "Width",
    "Height",
    "Density",
    "Fuzz"
    ]

widget_class_labels = [
    "Simple mirrors",
    "Flipping mirrors",
    "Box and sink",
    "Axial mirrors",
    "Rotators",
    "One-way mirrors",
    "PURE EVIL"
    ]

pic_list = [
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

# this indexes the above picture list so we know which ones are
# used for labels on the configure screen
config_percent_list = [1,2,3,5,9,10,11,14,15,18,19,22,23,31]

# need to keep track of the current square

square = None


def LoadConfig (self):

    print ("LoadConfig...")


def SaveConfig (self):

    print ("SaveConfig...")


def RestoreDefaults (self):

    print ("RestoreDefaults...")
    game_cols = default_game_cols
    game_rows = default_game_rows
    density = default_density
    density_fuzz = default_density_fuzz
    class_weights = default_class_weights


