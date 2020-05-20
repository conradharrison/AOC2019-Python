from Machine.Machine import Machine
from PaddleGame.PaddleGame import PaddleGame, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_WIDTH, CELL_HEIGHT
import arcade

f = open("13.txt", "r")
line = f.readline()
intcodes = list(map(lambda x:int(x), line.split(',')))

tile_name = {0: "BLANK", 1: "WALL", 2: "BLOCK", 3: "HPADDLE", 4: "BALL"}

# Setup machine and get tiles for screen size
m = Machine("m0", intcodes)
m.inputs = []
m.run()

max_x = -1
max_y = -1
while m.outputs:
    x = m.outputs.pop(0)
    y = m.outputs.pop(0)
    t = m.outputs.pop(0)
    #print(tile_name[t], "@", x, y)
    if x > max_x: max_x = x
    if y > max_y: max_y = y

board_width = (max_x+1)*CELL_WIDTH
board_height = (max_y+2)*CELL_HEIGHT # Extra for score line

game = PaddleGame(board_width, board_height, m)
game.set_minimum_size(board_width, board_height)
game.set_unit_scale(board_width, board_height)
game.reset_game()
arcade.run()
