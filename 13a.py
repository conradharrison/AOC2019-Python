from Machine.Machine import Machine
from PaddleGame.PaddleGame import PaddleGame, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_WIDTH, CELL_HEIGHT
import arcade
import time

f = open("13.txt", "r")
line = f.readline()
intcodes = list(map(lambda x:int(x), line.split(',')))

tile_name = {0: "BLANK", 1: "WALL", 2: "BLOCK", 3: "HPADDLE", 4: "BALL"}

# Setup machine and get tiles for screen size
m = Machine("m0", intcodes)
m.inputs = []
m.run()

game = PaddleGame(SCREEN_WIDTH, SCREEN_HEIGHT, m)

block_count = 0
max_x = -1
max_y = -1
while m.outputs:
    x = m.outputs.pop(0)
    y = m.outputs.pop(0)
    t = m.outputs.pop(0)
    #print(tile_name[t], "@", x, y)
    if x > max_x: max_x = x
    if y > max_y: max_y = y

    if t==2:
        game.add_block(x, y)
        block_count = block_count + 1
    
print(block_count)
game.set_minimum_size((max_x+1)*CELL_WIDTH, (max_y+1)*CELL_HEIGHT)
game.set_unit_scale((max_x+1)*CELL_WIDTH, (max_y+1)*CELL_HEIGHT)
game.set_size(max_x*CELL_WIDTH, max_y*CELL_HEIGHT)

m.reset()
m.imem[0] = 2
m.wait_for_input = True

arcade.run()
