import math

f = open("5.txt", "r")
line = f.readline()
intcodes = list(map(lambda x:int(x), line.split(',')))
length = len(intcodes)

def run(inputs):

    global length
    global intcodes

    intcodes_local = intcodes[:]

    done = False
    index = 0

    while (not done):
        opcode_full = intcodes_local[index]
        opcode = opcode_full % 100
        index = index + 1

        if opcode == 99:
            done = True
            continue

        if opcode == 1:
            if (index >= length-1):
                raise ValueError("Run out of operands for opcode " + str(opcode))
            parameter_mode_s1 = int(opcode_full/100) % 10
            parameter_mode_s2 = int(opcode_full/1000) % 10
            s1 = intcodes_local[index] 
            s2 = intcodes_local[index+1] 
            d =  intcodes_local[index+2] 
            intcodes_local[d] = (intcodes_local[s1] if parameter_mode_s1==0 else s1) + \
                                (intcodes_local[s2] if parameter_mode_s2==0 else s2)
            #print("ADD", opcode_full, opcode, s1, "(", parameter_mode_s1, ")", s2, "(", parameter_mode_s2, ")", d)                     
            index = index + 3
        elif opcode == 2:
            if (index >= length-1):
                raise ValueError("Run out of operands for opcode " + str(opcode))
            parameter_mode_s1 = int(opcode_full/100) % 10
            parameter_mode_s2 = int(opcode_full/1000) % 10
            s1 = intcodes_local[index] 
            s2 = intcodes_local[index+1] 
            d =  intcodes_local[index+2] 
            intcodes_local[d] = (intcodes_local[s1] if parameter_mode_s1==0 else s1) * \
                                (intcodes_local[s2] if parameter_mode_s2==0 else s2)
            #print("MUL", opcode_full, opcode, s1, "(", parameter_mode_s1, ")", s2, "(", parameter_mode_s2, ")", d)                     
            index = index + 3
        elif opcode == 3:
            d =  intcodes_local[index] 
            intcodes_local[d] = inputs.pop(0)
            #print("IN", opcode_full, opcode, d)                     
            index = index + 1
        elif opcode == 4:
            parameter_mode_s = int(opcode_full/100) % 10
            s =  intcodes_local[index] 
            output = intcodes_local[s] if parameter_mode_s==0 else s
            print(output)
            #print("OUT", opcode_full, opcode, s)                     
            index = index + 1
        elif opcode == 5:
            if (index >= length-1):
                raise ValueError("Run out of operands for opcode " + str(opcode))
            parameter_mode_cond = int(opcode_full/100) % 10
            parameter_mode_addr = int(opcode_full/1000) % 10
            cond = intcodes_local[index] 
            addr = intcodes_local[index+1] 
            #print("JUMPT", opcode_full, opcode, cond, "(", parameter_mode_cond, ")", addr, "(", parameter_mode_addr, ")")                     
            if (intcodes_local[cond] if parameter_mode_cond==0 else cond):
                index = (intcodes_local[addr] if parameter_mode_addr==0 else addr) 
            else:
                index = index + 2
        elif opcode == 6:
            if (index >= length-1):
                raise ValueError("Run out of operands for opcode " + str(opcode))
            parameter_mode_cond = int(opcode_full/100) % 10
            parameter_mode_addr = int(opcode_full/1000) % 10
            cond = intcodes_local[index] 
            addr = intcodes_local[index+1] 
            #print("JUMPF", opcode_full, opcode, cond, "(", parameter_mode_cond, ")", addr, "(", parameter_mode_addr, ")")                     
            if not (intcodes_local[cond] if parameter_mode_cond==0 else cond):
                index = (intcodes_local[addr] if parameter_mode_addr==0 else addr) 
            else:
                index = index + 2
        elif opcode == 7:
            if (index >= length-1):
                raise ValueError("Run out of operands for opcode " + str(opcode))
            parameter_mode_s1 = int(opcode_full/100) % 10
            parameter_mode_s2 = int(opcode_full/1000) % 10
            s1 = intcodes_local[index] 
            s2 = intcodes_local[index+1] 
            d =  intcodes_local[index+2] 
            if (intcodes_local[s1] if parameter_mode_s1==0 else s1) < (intcodes_local[s2] if parameter_mode_s2==0 else s2):
                intcodes_local[d] = 1
            else:
                intcodes_local[d] = 0
            #print("SLT", opcode_full, opcode, s1, "(", parameter_mode_s1, ")", s2, "(", parameter_mode_s2, ")", d)                     
            index = index + 3
        elif opcode == 8:
            if (index >= length-1):
                raise ValueError("Run out of operands for opcode " + str(opcode))
            parameter_mode_s1 = int(opcode_full/100) % 10
            parameter_mode_s2 = int(opcode_full/1000) % 10
            s1 = intcodes_local[index] 
            s2 = intcodes_local[index+1] 
            d =  intcodes_local[index+2] 
            if (intcodes_local[s1] if parameter_mode_s1==0 else s1) == (intcodes_local[s2] if parameter_mode_s2==0 else s2):
                intcodes_local[d] = 1
            else:
                intcodes_local[d] = 0
            #print("SEQ", opcode_full, opcode, s1, "(", parameter_mode_s1, ")", s2, "(", parameter_mode_s2, ")", d)                     
            index = index + 3
        else:
            raise ValueError("Invalid opcode: " + str(opcode))

    return

run([5])
