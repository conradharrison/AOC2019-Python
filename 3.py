import math
import re

def step(direction, start_position):
    (x, y) = start_position
    if direction == 'R':
            return (x + 1, y)
    elif direction == 'L':
            return (x - 1, y)
    elif direction == 'U':
            return (x, y + 1)
    elif direction == 'D':
            return (x, y - 1)
    else:
        raise ValueError("Invalid driection")

def intersects(position, path):

    for (ref_pos, ref_steps) in path:
        if ref_pos == position:
            return (True, ref_steps)

    return (False, -1)

def walk(move, start_path_item, my_path, ref_path):
    global closest_distance
    global lowest_steps

    if move == "NULL":
        return

    direction = move[0]
    steps = int(re.split(r'[LRUD]', move)[1])

    (current_position, my_total_steps) = start_path_item
    for i in range(1, steps+1):
        next_position = step(direction, current_position)
        my_total_steps = my_total_steps + 1
        (intersection, ref_total_steps) = intersects(next_position, ref_path)
        (self_intersection, my_first_steps) = intersects(next_position, my_path)

        if self_intersection:
            my_steps = my_first_steps
        else:
            my_steps = my_total_steps
        
        if intersection:
        
            # record lowest total_steps
            total_steps = my_steps + ref_total_steps
            if total_steps < lowest_steps or lowest_steps == -1:
                lowest_steps = total_steps
            
            # record closet distance
            (x, y) = next_position
            distance = abs(x)+abs(y)
            if distance < closest_distance or closest_distance == -1:
                closest_distance = distance

            print("Intersection at", next_position, "Distance =", distance, "Closest =", closest_distance, "Steps =", total_steps, "Lowest steps =", lowest_steps)

        my_path.append((next_position, my_steps))
        current_position = next_position

    return (current_position, my_steps)

## Main

f = open("3.txt", "r")
red_move_list = f.readline().split(',')
blue_move_list = f.readline().split(',')

red_path= []
blue_path= []
red_path_item = ((0,0), 0)
blue_path_item = ((0,0), 0)
closest_distance = -1
lowest_steps = -1

while(True):
    # Read one move from each list, NULL move if empty
    if len(red_move_list) != 0:
        red_move = red_move_list.pop(0)
        red_path_item = walk(red_move, red_path_item, red_path, blue_path)
    else:
        red_move = "NULL"

    if len(blue_move_list) != 0:
        blue_move = blue_move_list.pop(0)
        blue_path_item = walk(blue_move, blue_path_item, blue_path, red_path)
    else:
        blue_move = "NULL"

    if red_move == "NULL" and blue_move == "NULL":
        break

print(closest_distance)
