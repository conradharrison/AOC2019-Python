from Machine.Machine import Machine

f = open("11.txt", "r")
line = f.readline()
intcodes = list(map(lambda x:int(x), line.split(',')))

m = Machine("m0", intcodes)

turn_table = {
        (( 0,  1), 0): ((-1,  0), (-1,  0)),
        ((-1,  0), 0): (( 0, -1), ( 0, -1)),
        (( 0, -1), 0): (( 1,  0), ( 1,  0)),
        (( 1,  0), 0): (( 0,  1), ( 0,  1)),
        (( 0,  1), 1): (( 1,  0), ( 1,  0)),
        ((-1,  0), 1): (( 0,  1), ( 0,  1)),
        (( 0, -1), 1): ((-1,  0), (-1,  0)),
        (( 1,  0), 1): (( 0, -1), ( 0, -1)),
        }

painted_pixels = {}

largest_x, largest_y = -1, -1
smallest_x, smallest_y = 999999, 999999
x, y = 0, 0
dir = (0, 1)
halted = False
while True:
    if (x,y) in painted_pixels:
        m.inputs = [painted_pixels[(x,y)]]
    else:
        m.inputs = [1]

    m.run(stop_on_output=True)
    if m.halted:
        break
    color = m.outputs.pop(0)
    m.run(stop_on_output=True)
    turn = m.outputs.pop(0)

    painted_pixels[(x,y)] = color # if already exists overwrites
    (dx, dy), dir = turn_table[(dir, turn)] 
    x, y = x + dx, y + dy

    if x > largest_x:
        largest_x = x
    if x < smallest_x:
        smallest_x = x
    if y > largest_y:
        largest_y = y
    if y < smallest_y:
        smallest_y = y

print(len(painted_pixels))
for y in range(largest_y, smallest_y-1, -1):
    for x in range(smallest_x, largest_x+1):
        if (x,y) in painted_pixels:
            print(" " if painted_pixels[(x,y)]==0 else "1", end="")
        else:
            print(" ", end="")
    print()
