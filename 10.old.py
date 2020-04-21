import math

f = open("10.txt", "r")
field = []
for line in f:
    l = (list(map(lambda x:(0 if x=='.' else 1), line.strip())))
    print(l)
    field.append(l)

def walk(x0, y0):
    global field

    y = 0
    for line in field:
        x = 0
        for point in line:
            if x == x0 and y == y0:
                x = x + 1
                continue
            else:
                yield (x, y)
            x = x + 1
        y = y + 1

global angles_blocked

def ab_in_angles_blocked(da, db):
    global angles_blocked

    sign = lambda x: (1, -1)[x < 0]

    for (dx, dy) in angles_blocked:
        if (sign(dx) != sign(da)) or (sign(dy) != sign(db)):
            continue
        if dx == 0:
            if da == 0:
                return True
        elif da == 0:
            if dx == 0:
                return True
        elif dy/dx == db/da:
            return True
        else:
            continue
    return False

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
        angles_blocked = []
        walker = walk(x, y)
        for (a, b) in walker:
            if field[b][a] == 1:
                if ab_in_angles_blocked((a-x), (b-y)):
                    continue
                asteroid_count = asteroid_count + 1
                angles_blocked.append(((a-x), (b-y)))

        print(x, y, ": ", asteroid_count)

        if asteroid_count > largest:
            largest = asteroid_count
            largest_x = x
            largest_y = y

        x = x + 1
    y = y + 1

print(largest_x, largest_y, "=", largest)
