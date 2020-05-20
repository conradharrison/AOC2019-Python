from .ISA.ADD import ADD
from .ISA.MUL import MUL
from .ISA.IN import IN
from .ISA.OUT import OUT
from .ISA.JMPT import JMPT
from .ISA.JMPF import JMPF
from .ISA.SETLT import SETLT
from .ISA.SETEQ import SETEQ
from .ISA.SETRB import SETRB
from .ISA.HALT import HALT

class Machine():
    def __init__(self, name, program):
        self.name = name
        self.program = program[:] # Save away
        self.program_size = len(program)

        # Machine state
        self.imem = program[:]
        self.ipointer = 0
        self.relative_base = 0
        self.inputs = []
        self.input_needed = False
        self.outputs = []
        self.output_ready = False
        self.halted = False
        self.heap = [0] * (1024*1024) # Allocate 1M heap locations
        
        # list of execution units
        self.units = {}

        # Machine has the following execution units, with the following opcodes:
        self.units[1] = ADD(self)
        self.units[2] = MUL(self)
        self.units[3] = IN(self)
        self.units[4] = OUT(self)
        self.units[5] = JMPT(self)
        self.units[6] = JMPF(self)
        self.units[7] = SETLT(self)
        self.units[8] = SETEQ(self)
        self.units[9] = SETRB(self)
        self.units[99] = HALT(self)

    def reset(self):
        self.imem = self.program[:]
        self.ipointer = 0
        self.relative_base = 0
        self.inputs = []
        self.input_needed = False
        self.outputs = []
        self.output_ready = False
        self.halted = False
        # Leave self.heap[:] as is

    def run(self, stop_on_output=False, wait_for_input=False):

        if stop_on_output:
            self.outputs = [] # TODO: should this be the responsibility of the caller?

        while (True):
            op = self.step(wait_for_input)
            
            if self.halted == True:
                break

            if self.input_needed and wait_for_input:
                self.input_needed = False
                break
            
            if self.output_ready and stop_on_output:
                self.output_ready = False
                break
        #print(self.get_state())

    def step(self, wait_for_input):
        # Peek for instruction opcode
        opcode_full = self.imem[self.ipointer] % 100
        opcode = opcode_full % 100

        if wait_for_input and opcode == 3 and self.inputs == []:
            self.input_needed = True
        else:
            # Call the corresponding execution unit
            self.units[opcode].execute()

    def read_mem(self, addr):
        # |<---program--->|<---heap--->|<---ERROR--->|
        if addr >= self.program_size:
            if addr - self.program_size >= len(self.heap):
                raise ValueError("Exceeded heap size " + str(addr))
            d = self.heap[addr % self.program_size]
        else:
            d = self.imem[addr]
        return d

    def write_mem(self, addr, data):
        # |<---program--->|<---heap--->|<---ERROR--->|
        if addr >= self.program_size:
            if addr - self.program_size >= len(self.heap):
                raise ValueError("Exceeded heap size " + str(addr))
            self.heap[addr % self.program_size] = data
        else:
            self.imem[addr] = data

    # Debug
    def get_state(self):
        s = self.name + ":\n" 
        s = s + ">>> " + "IP=" + str(self.ipointer) + ", " + "RB=" + str(self.relative_base) + "\n"
        s = s + ">>> " + "inputs=" + str(self.inputs) + ", " + "outputs=" + str(self.outputs) + "\n"
        s = s + ">>> " + "halted=" + str(self.halted) + ", " + "output_ready=" + str(self.output_ready) + "\n"
        s = s + ">>> " + "mem=" + str(self.imem) + "\n"
        s = s + ">>> " + "heap=" + str(self.heap[:64])
        return s
