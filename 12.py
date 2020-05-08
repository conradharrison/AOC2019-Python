import re
import itertools
import operator
import cProfile

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
    moons.append({'name': "M"+str(i), 'pos0':(int(x), int(y), int(z)), 'pos':(int(x), int(y), int(z)), 'vel':(0, 0, 0)})
    i = i + 1
moons_start = moons[:]
moon_pairs = pairs(len(moons))

def show():
    global moons
    for m in moons:
        print(m)

def step():
    global moons, moon_pairs

    #update velocity
    for (p1,p2) in moon_pairs:
        m1 = moons[p1]
        m2 = moons[p2]

        (dx, dy, dz) = (cmp(m1['pos'][0], m2['pos'][0]), cmp(m1['pos'][1], m2['pos'][1]), cmp(m1['pos'][2], m2['pos'][2]))
        m1['vel'] = (m1['vel'][0] + dx, m1['vel'][1] + dy, m1['vel'][2] + dz)
        m2['vel'] = (m2['vel'][0] - dx, m2['vel'][1] - dy, m2['vel'][2] - dz)

    #use updated velocity to update position
    cycle = True
    for m in moons:
        m['pos'] = (m['pos'][0]+m['vel'][0], m['pos'][1]+m['vel'][1], m['pos'][2]+m['vel'][2])

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
while((not done) and i<10000000):
    i = i + 1
    if i%(1000000)==0: print(int(i/1000000), "M+")
    done = step()

print(i)
#pr.print_stats()
