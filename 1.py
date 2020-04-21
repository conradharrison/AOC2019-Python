import math

def fuel(m):
    f = max(math.floor(m/3) - 2, 0)
    if f == 0:
        return f
    else:
        return f + fuel(f)

f = open("1.txt", "r")

s = 0
for x in f:
    s = s + fuel(int(x)) 
print(s)

