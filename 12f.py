import re
import itertools
import operator
#import cProfile

# generic utilities
def pairs(n):
    p = []
    for i in range(0, n):
        for j in range(i+1, n):
            p.append((i, j))
    return p

def cmp(a, b):
    if a < b:
        return 1
    if a > b:
        return -1
    else:
        return 0

#
# main solution
#

re_parse = re.compile(r"\<x=(-?\d+), y=(-?\d+), z=(-?\d+)\>")
moons = []

f = open("12.txt", "r")
i = 0 # For moon-id
for moon in f:
    (x, y, z) = re_parse.match(moon).group(1,2,3)
    moons.append({'name': "M"+str(i), 'pos0':(int(x), int(y), int(z)), 'pos':[int(x), int(y), int(z)], 'vel':(0, 0, 0)})
    i = i + 1

def show():
    global moons
    for m in moons:
        print(m)

def step():
    global moons

    #update velocity, for all pairs
    # 0, 1
    m1, m2 = moons[0], moons[1]
    (dx01, dy01, dz01) = (cmp(m1['pos'][0], m2['pos'][0]), cmp(m1['pos'][1], m2['pos'][1]), cmp(m1['pos'][2], m2['pos'][2]))

    # 0, 2
    m1, m2 = moons[0], moons[2]
    (dx02, dy02, dz02) = (cmp(m1['pos'][0], m2['pos'][0]), cmp(m1['pos'][1], m2['pos'][1]), cmp(m1['pos'][2], m2['pos'][2]))

    # 0, 3
    m1, m2 = moons[0], moons[3]
    (dx03, dy03, dz03) = (cmp(m1['pos'][0], m2['pos'][0]), cmp(m1['pos'][1], m2['pos'][1]), cmp(m1['pos'][2], m2['pos'][2]))

    # 1, 2
    m1, m2 = moons[1], moons[2]
    (dx12, dy12, dz12) = (cmp(m1['pos'][0], m2['pos'][0]), cmp(m1['pos'][1], m2['pos'][1]), cmp(m1['pos'][2], m2['pos'][2]))

    # 1, 3
    m1, m2 = moons[1], moons[3]
    (dx13, dy13, dz13) = (cmp(m1['pos'][0], m2['pos'][0]), cmp(m1['pos'][1], m2['pos'][1]), cmp(m1['pos'][2], m2['pos'][2]))

    # 2, 3
    m1, m2 = moons[2], moons[3]
    (dx23, dy23, dz23) = (cmp(m1['pos'][0], m2['pos'][0]), cmp(m1['pos'][1], m2['pos'][1]), cmp(m1['pos'][2], m2['pos'][2]))

    moons[0]['pos'][0] = dx01 + dx02 + dx03
    moons[0]['pos'][1] = dy01 + dy02 + dy03
    moons[0]['pos'][2] = dz01 + dz02 + dz03

    moons[1]['pos'][0] = -dx01 + dx12 + dx13
    moons[1]['pos'][1] = -dy01 + dy12 + dy13
    moons[1]['pos'][2] = -dz01 + dz12 + dz13

    moons[2]['pos'][0] = -dx02 - dx12 + dx23
    moons[2]['pos'][1] = -dy02 - dy12 + dy23
    moons[2]['pos'][2] = -dz02 - dz12 + dz23

    moons[3]['pos'][0] = -dx03 - dx13 - dx23
    moons[3]['pos'][1] = -dy03 - dy13 - dy23
    moons[3]['pos'][2] = -dz03 - dz13 - dz23

    cycle = True
    for m in moons:
        if cycle==True:
            if m['vel']==(0,0,0):
                if m['pos']==m['pos0']:
                    continue
                else:
                    cycle = False
            else:
                cycle = False

    return cycle

def energy():
    global moons
    sum = 0
    for m in moons:
        pe = abs(m['pos'][0]) + abs(m['pos'][1]) + abs(m['pos'][2])
        ke = abs(m['vel'][0]) + abs(m['vel'][1]) + abs(m['vel'][2])
        sum = sum + (pe * ke)
    return sum

#pr = cProfile.Profile()
#pr.enable()

i = 0
done = False
while (not done):
    i = i + 1
    if i%(1000000)==0: print(int(i/1000000), "M+")
    done = step()

print(i)
#pr.print_stats()
