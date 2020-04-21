import math

f = open("7.txt", "r")
line = f.readline()
intcodes = list(map(lambda x:int(x), line.split(',')))
length = len(intcodes)

# Total of 5 machines can be supported
state = []
state.append((intcodes[:], 0)) # instruction pointer, program state
state.append((intcodes[:], 0)) 
state.append((intcodes[:], 0))
state.append((intcodes[:], 0))
state.append((intcodes[:], 0))

def reset(machine):
    global state
    global intcodes
    state[machine] = (intcodes[:], 0)
    return

def run(machine, inputs):

    global length
    global intcodes

    global state

    intcodes_local = state[machine][0]
    index = state[machine][1]

    #print("Starting machine", machine, "from", index, "with inputs=", inputs)

    done = False
    outputs = []

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
            #print("IN", opcode_full, opcode, d, intcodes_local[d])                     
            index = index + 1
        elif opcode == 4:
            parameter_mode_s = int(opcode_full/100) % 10
            s =  intcodes_local[index] 
            outputs.append(intcodes_local[s] if parameter_mode_s==0 else s)
            #print("OUT", opcode_full, opcode, s)                     
            index = index + 1
            # Save state and return
            state[machine] = (intcodes_local[:], index)
            #print("Stopping machine", machine, "at", index, "with outputs=", outputs, state[machine])
            return outputs
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

    return outputs

def run_phase(p0, p1, p2, p3, p4):

    maxthrust = -1

    first = True
    halt = False
    while (not halt):
        if first:
            out0 = run(0, [p0, 0]) 
            out1 = run(1, [p1, *out0]) 
            out2 = run(2, [p2, *out1]) 
            out3 = run(3, [p3, *out2]) 
            out4 = run(4, [p4, *out3]) 
            first = False
        else:
            out0 = run(0, [*out4])
            out1 = run(1, [*out0]) 
            out2 = run(2, [*out1]) 
            out3 = run(3, [*out2]) 
            out4 = run(4, [*out3]) 

        if out0==[] and out1==[] and out2==[] and out3==[] and out4==[]:
            halt = True
        else:
            #print("   Thrust =", out4[0])
            if out4[0] > maxthrust:
                maxthrust = out4[0]

    return maxthrust

supermaxthrust = -1

l = [5,6,7,8,9]
l0 = l[:]
for p0 in l0:
    l1 = l[:]
    l1.remove(p0)
    for p1 in l1:
        l2 = l[:]
        l2.remove(p0)
        l2.remove(p1)
        for p2 in l2:
            l3 = l[:]
            l3.remove(p0)
            l3.remove(p1)
            l3.remove(p2)
            for p3 in l3:
                l4 = l[:]
                l4.remove(p0)
                l4.remove(p1)
                l4.remove(p2)
                l4.remove(p3)
                for p4 in l4:
                    print("Running phase setting", (p0, p1, p2, p3, p4))
                    thrust = run_phase(p0, p1, p2, p3, p4)
                    if thrust > supermaxthrust:
                        supermaxthrust = thrust
                    print(thrust)
                    reset(0)
                    reset(1)
                    reset(2)
                    reset(3)
                    reset(4)
print(supermaxthrust)
