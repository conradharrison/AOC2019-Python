from Machine.Machine import Machine

f = open("9.txt", "r")
line = f.readline()
intcodes = list(map(lambda x:int(x), line.split(',')))

m = Machine("m0", intcodes)
m.inputs = [2]
m.run()
print(m.outputs)
