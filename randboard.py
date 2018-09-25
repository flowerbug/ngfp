import pyglet
from pyglet.window import mouse
import random
from random import randrange, getrandbits, seed
from time import sleep
import copy

def InitRandomBoardItems (self):

    # use "./gfpoken" configuration file if it exists
    #   1st line:
    #     1 integer:
    #       version # 1
    #   2nd line:
    #     11 integers:
    #       width
    #       height
    #       density
    #       densityfuzz
    #       classweight 0 - 6
    #
    #  currently i'm using:
    #    1
    #    12 12 59 15 100 25 11 5 5 5 5
    #
    # and random seed 8 for testing
    random.seed(a=8)

    # these will come from configuration file eventually...
    gridx = self.game_rows
    gridy = self.game_cols
    self.density = 59
    self.densityfuzz = 15
    self.classweight = [100, 75, 20, 20, 20, 20, 20]
    self.class_sum = sum(self.classweight)

    print ('classweight, class_sum', self.classweight, self.class_sum)

    self.class_list = [
                  ['ClSimple', []],
                  ['ClFlipper', []],
                  ['ClBoxSink', []],
                  ['ClAxis', []],
                  ['ClRotator', []],
                  ['ClOneWay', []],
                  ['ClEvil', []]
                 ]

    self.test_class_list = [['ClSimple', [[0, 1], [1, 2]]], ['ClFlipper', [[2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8]]], ['ClBoxSink', [[8, 9], [9, 10]]], ['ClAxis', [[10, 11], [11, 12], [12, 13], [13, 14]]], ['ClRotator', [[14, 15], [15, 16], [16, 17], [17, 18]]], ['ClOneWay', [[18, 19], [19, 20], [20, 21], [21, 22]]], ['ClEvil', [[22, 23], [23, 24], [24, 25], [25, 26], [26, 27], [27, 28], [28, 29], [29, 30], [30, 31], [31, 32]]]]


    if (self.use_test_board):
        self.class_list = list(self.test_class_list)
        self.widget_pile_list_counts = list(self.test_widget_pile_list_counts)
        self.board = copy.deepcopy(self.test_board)
    else:
        randpop = ((self.density * self.board_squares / 100) + 1) // 1
        randpop += ((random.getrandbits(32) % (randpop*self.densityfuzz*2/100 + 1)) - (randpop*self.densityfuzz/100)) // 1

        if (randpop > self.board_squares):
            randpop = self.board_squares

        if randpop < 0:
            randpop = 0

        while (randpop > 0):
            position = random.getrandbits(32) % self.board_squares
            print ('randpop, position', randpop, position)

            if (self.board[position][0] == 0):
                randchance = random.getrandbits(32) % self.class_sum

                print ('  randchance', randchance)
                upperbound = 0
                tempobj = 0

                for counter in range(len(self.classweight)):
                    upperbound += self.classweight[counter]
                    print ('    upperbound', upperbound)
                    if (upperbound == 0):
                        continue                                         #  Base case

                    if (randchance < upperbound):
                        if (self.class_list[counter][0] == 'ClSimple'):
                            tempobj = (random.getrandbits(32) % 2) + 1     # 1-2
                            if (self.board[position][0] == 0):
                                self.widget_pile_list_counts[tempobj-1] += 1
                        elif (self.class_list[counter][0] == 'ClFlipper'):
                            tempobj = (random.getrandbits(32) % 6) + 3     # 3-8
                            if (self.board[position][0] == 0):
                                if ((tempobj == 3) or (tempobj == 4)):
                                    self.widget_pile_list_counts[2] += 1
                                else:
                                    self.widget_pile_list_counts[3] += 1
                        elif (self.class_list[counter][0] == 'ClBoxSink'):
                            tempobj = (random.getrandbits(32) % 2) + 9     # 9-10
                            if (self.board[position][0] == 0):
                                self.widget_pile_list_counts[tempobj-5] += 1
                        elif (self.class_list[counter][0] == 'ClAxis'):
                            tempobj = (random.getrandbits(32) % 4) + 11    # 11-14
                            if (self.board[position][0] == 0):
                                if (tempobj == 11):
                                    self.widget_pile_list_counts[6] += 1
                                elif (tempobj == 12):
                                    self.widget_pile_list_counts[7] += 1
                                else:
                                    self.widget_pile_list_counts[8] += 1
                        elif (self.class_list[counter][0] == 'ClRotator'):
                            tempobj = (random.getrandbits(32) % 4) + 15    # 15-18
                            if (self.board[position][0] == 0):
                                if (tempobj == 15):
                                    self.widget_pile_list_counts[9] += 1
                                elif (tempobj == 16):
                                    self.widget_pile_list_counts[10] += 1
                                else:
                                    self.widget_pile_list_counts[11] += 1
                        elif (self.class_list[counter][0] == 'ClOneWay'):
                            tempobj = (random.getrandbits(32) % 4) + 19    # 19-22
                            if (self.board[position][0] == 0):
                                self.widget_pile_list_counts[tempobj-7] += 1
                        elif (self.class_list[counter][0] == 'ClEvil'):
                            tempobj = (random.getrandbits(32) % 10) + 23   # 23-32
                            if (self.board[position][0] == 0):
                                if ((tempobj >= 23) and (tempobj <= 26)):
                                    self.widget_pile_list_counts[16] += 1
                                elif ((tempobj >= 27) and (tempobj <= 30)):
                                    self.widget_pile_list_counts[17] += 1
                                elif (tempobj == 31):
                                    self.widget_pile_list_counts[18] += 1
                                else:
                                    self.widget_pile_list_counts[19] += 1
                        else:
                            pass

                        if (self.board[position][0] == 0):
                            self.board[position][0] = tempobj
                            print ('    position, tempobj', position, tempobj)
                            self.class_list[counter][1].append([position, tempobj])
                        else:
                            continue

            randpop -= 1

    print (self.class_list)
    print (self.widget_pile_list_counts)
    print (self.board)

