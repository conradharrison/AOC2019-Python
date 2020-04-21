import math

f = open("2.txt", "r")
line = f.readline()
intcodes = list(map(lambda x:int(x), line.split(',')))
length = len(intcodes)

def run(a, b):

    global length
    global intcodes

    intcodes_local = intcodes[:]
    intcodes_local[1] = a
    intcodes_local[2] = b

    done = False
    index = 0

    while (not done):
        opcode = intcodes_local[index]
        index = index + 1

        if opcode == 99:
            done = True
            continue

        if opcode == 1:
            if (index >= length-1):
                raise ValueError("Run out of operands for opcode " + str(opcode))
            s1 = intcodes_local[index] 
            s2 = intcodes_local[index+1] 
            d =  intcodes_local[index+2] 
            intcodes_local[d] = intcodes_local[s1] + intcodes_local[s2]
            index = index + 3
        elif opcode == 2:
            if (index >= length-1):
                raise ValueError("Run out of operands for opcode " + str(opcode))
            s1 = intcodes_local[index] 
            s2 = intcodes_local[index+1] 
            d =  intcodes_local[index+2] 
            intcodes_local[d] = intcodes_local[s1] * intcodes_local[s2]
            index = index + 3
        else:
            raise ValueError("Invalid opcode: " + str(opcode))

    return(intcodes_local[0])

def search():
    for a in range(0, 100):
        for b in range(0, 100):
            result = run(a, b)
            if result == 19690720:
                return(a, b)

(x, y) = search()
print(100 * x + y)
