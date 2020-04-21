import math

angles = []
for y in range(0, 8):
    for x in range(1, 8):
        if math.gcd(x, y) > 1:
            continue
        angles.append((x, y))

angles.sort(key = lambda k: k[1]/k[0])

print(angles)
