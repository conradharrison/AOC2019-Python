import math

f = open("10.txt", "r")
field = []
for line in f:
    l = (list(map(lambda x:(0 if x=='.' else 1), line.strip())))
    print(l)
    field.append(l)
fieldW = len(field[0])
fieldH = len(field)

def get_points_in_dir(x0, y0, dirx, diry):
    global field, fieldW, fieldH
    points = []
    k = 1
    while True:
        x, y = x0 + dirx*k, y0 + diry*k
        if x >= fieldW or y >= fieldH or x < 0 or y < 0:
            break
        else:
            if field[y][x] == 1:
                points.append((x, y))
            else:
                pass
            k = k + 1
    return points

def add_points_in_dirs(x0, y0, dirs, valid_dirs, points_in_dir):
    for ax, ay in dirs:
        points = get_points_in_dir(x0, y0, ax, ay)
        if len(points) > 0:
            points_in_dir[(ax, ay)] = points
            valid_dirs.append((ax, ay))

def get_all_dirs(x0, y0):
    global field

    # quadrants:
    # -------------
    #|      |      |
    #|  2   |   3  |
    #|      |      |
    # ---(x0,y0)----
    #|      |      |
    #|  1   |   0  |
    #|      |      |
    # -------------

    points_in_dir = {}
    valid_dirs = []

    # Shooting startes at quadrant 3, and goes clockwise

    # Quadrant 3
    dirs = []
    for ty in range(x0, fieldW):
        for tx in range(y0-1, 0-1, -1):
            dx, dy = ty-x0, tx-y0
            if math.gcd(dx, dy) > 1:
                continue
            dirs.append((dx, dy))
    dirs.sort(key = lambda k: -k[0]/k[1])
    add_points_in_dirs(x0, y0, dirs, valid_dirs, points_in_dir)

    # Quadrant 0
    dirs = []
    for ty in range(y0, fieldH):
        for tx in range(x0+1, fieldW):
            dx, dy = tx-x0, ty-y0
            if math.gcd(dx, dy) > 1:
                continue
            dirs.append((dx, dy))
    dirs.sort(key = lambda k: k[1]/k[0])
    add_points_in_dirs(x0, y0, dirs, valid_dirs, points_in_dir)

    # Quadrant 1
    dirs = []
    for ty in range(x0, 0-1, -1):
        for tx in range(y0+1, fieldH):
            dx, dy = ty-x0, tx-y0
            if math.gcd(dx, dy) > 1:
                continue
            dirs.append((dx, dy))
    dirs.sort(key = lambda k: -k[0]/k[1])
    add_points_in_dirs(x0, y0, dirs, valid_dirs, points_in_dir)

    # Quadrant 2
    dirs = []
    for ty in range(y0, 0-1, -1):
        for tx in range(x0-1, 0-1, -1):
            dx, dy = tx-x0, ty-y0
            if math.gcd(dx, dy) > 1:
                continue
            dirs.append((dx, dy))
    dirs.sort(key = lambda k: k[1]/k[0])
    add_points_in_dirs(x0, y0, dirs, valid_dirs, points_in_dir)

    return(valid_dirs, points_in_dir)

def walk(x0, y0):

    valid_dirs, points_in_dir = get_all_dirs(x0, y0)
    yield (valid_dirs, points_in_dir)

    # yeild from points in each valid_dirs
    for (dirx, diry) in valid_dirs:
        if points_in_dir[(dirx, diry)]:
            p = points_in_dir[(dirx, diry)].pop(0)
            yield p

largest = -1
largest_x = -1
largest_y = -1

y = 0
for line in field:
    x = 0
    for point in line:
        if point == 0:
            x = x + 1
            continue

        asteroid_count = 0

        walker = walk(x, y)
        valid_dirs, points_in_dir = next(walker)
        asteroid_count = len(valid_dirs)

        if asteroid_count > largest:
            largest = asteroid_count
            largest_x = x
            largest_y = y
            largest_valid_dirs = valid_dirs
            largest_points_in_dir = points_in_dir

        x = x + 1
    y = y + 1

print("most asterods sighted from", largest_x, largest_y, "=", largest)

# Keep rotating till all asteroids are shot
t = 1
done = False
while not done:
    done = True
    for d in largest_valid_dirs:
        if largest_points_in_dir[d]:
            (px, py) = largest_points_in_dir[d].pop(0)
            if t == 200:
                print(px*100 + py)
            t = t + 1
            done = False
