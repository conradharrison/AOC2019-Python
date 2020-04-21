f = open("12.txt", "r")

for moon in f:
    line = moon.split("<>:)
intcodes = list(map(lambda x:int(x), line.split(',')))
