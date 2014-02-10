from libs.launchpad import *


class Games():

    def __init__(self):
        launchpads = find_launchpads()
        self.launchpad = Launchpad(*launchpads[0])

    def tictactoe(self):
        grid = [
            [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1)],
            [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1)],
            [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1)],
            [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1)],
            [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1)],
            [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (0, 0), (0, 0), (0, 0), (2, 1)],
            [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (0, 0), (0, 0), (0, 0), (2, 1)],
            [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (0, 0), (0, 0), (0, 0), (2, 1)],
            [(2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1), (2, 1)]]

        self.launchpad.set_all(grid)

        game_playing = True
        green_turn = True

        while game_playing:
            move = self.launchpad.poll()
            if move is not None:
                print "DATA:", move[0], move[1]
                if move[0] == 0 and move[1] == 8:
                    self.launchpad.set_all(grid)

                if green_turn and move[2]:
                    self.launchpad.set_light(move[0], move[1], 0, 3)
                    self.launchpad.poll()
                    green_turn = False

                elif not green_turn and move[2]:
                    self.launchpad.set_light(move[0], move[1], 3, 0)
                    self.launchpad.poll()
                    green_turn = True