import math
from Machine.Machine import Machine

f = open("7.txt", "r")
line = f.readline()
intcodes = list(map(lambda x:int(x), line.split(',')))
length = len(intcodes)

m0 = Machine("m0", intcodes)
m1 = Machine("m1", intcodes)
m2 = Machine("m2", intcodes)
m3 = Machine("m3", intcodes)
m4 = Machine("m4", intcodes)

def run_phase(p0, p1, p2, p3, p4):

    maxthrust = -1

    first = True
    halt = False
    while (not halt):
        if first:
            m0.inputs = [p0, 0]
            m0.run(stop_on_output=True)
            m1.inputs = [p1, *(m0.outputs)]
            m1.run(stop_on_output=True)
            m2.inputs = [p2, *(m1.outputs)]
            m2.run(stop_on_output=True)
            m3.inputs = [p3, *(m2.outputs)]
            m3.run(stop_on_output=True)
            m4.inputs = [p4, *(m3.outputs)]
            m4.run(stop_on_output=True)
            first = False
        else:
            m0.inputs = [*(m4.outputs)]
            m0.run(stop_on_output=True)
            m1.inputs = [*(m0.outputs)]
            m1.run(stop_on_output=True)
            m2.inputs = [*(m1.outputs)]
            m2.run(stop_on_output=True)
            m3.inputs = [*(m2.outputs)]
            m3.run(stop_on_output=True)
            m4.inputs = [*(m3.outputs)]
            m4.run(stop_on_output=True)


        if m0.halted and m1.halted and m2.halted and m3.halted and m4.halted:
            halt = True
        else:
            output = m4.outputs[0]
            #print("   Thrust =", output)
            if output > maxthrust:
                maxthrust = output

    return maxthrust

supermaxthrust = -1

l = [5,6,7,8,9]
l = [9,8,7,6,5]
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
                    #print("Running phase setting", (p0, p1, p2, p3, p4))
                    thrust = run_phase(p0, p1, p2, p3, p4)
                    #input("")
                    if thrust > supermaxthrust:
                        supermaxthrust = thrust
                    #print(thrust)
                    m0.reset()
                    m1.reset()
                    m2.reset()
                    m3.reset()
                    m4.reset()
print(supermaxthrust)
