class Unit:
    def __init__(self, machine, opname):
        self.opname = opname
        self.machine = machine
        self.operands = []

        self.opcode_full = None
        self.parameter_modes = None

        self.logstr = ""

    def check(self):
        if (self.machine.ipointer >= self.machine.program_size):
            raise ValueError("Run out of program for " + self.opname + "\n" + self.machine.get_state())

    def fetch_opcode(self):
        self.opcode_full = self.machine.read_mem(self.machine.ipointer)
        self.machine.ipointer = self.machine.ipointer + 1

        self.parameter_modes = int(self.opcode_full / 100)
        self.logstr = self.logstr + self.opname + " "

    def fetch_operand(self, is_dest=False):

        operand = self.machine.read_mem(self.machine.ipointer)
        self.machine.ipointer = self.machine.ipointer + 1

        # resolve based on parameter_mode
        parameter_mode = self.parameter_modes % 10
        self.parameter_modes = int(self.parameter_modes / 10)

        if parameter_mode == 0: # postion mode
            self.logstr = self.logstr + "["+str(operand)+"]="
            if is_dest == False:
                operand = self.machine.read_mem(operand)
            else:
                operand = operand
            self.logstr = self.logstr + str(operand) + " "
        elif parameter_mode == 1: # immediate mode
            self.logstr = self.logstr + str(operand) + " "
            if is_dest == False:
                operand = operand
            else:
                raise ValueError("Invalid mode 1 for dest parameter\n" + machine.get_state())
        elif parameter_mode == 2: # relative mode
            self.logstr = self.logstr + "{"+str(operand)+"}="
            if is_dest == False:
                operand = self.machine.read_mem(operand + self.machine.relative_base)
            else:
                operand = operand + self.machine.relative_base
            self.logstr = self.logstr + str(operand) + " "
        else:
            raise ValueError("Invalid parameter mode=" + str(parameter_mode) + "\n" + machine.get_state())

        return operand

    # Override
    def fetch_operands_and_compute(self):
        return

    def reset(self):
        self.operands = []
        self.parameter_modes = None
        self.logstr = ""

    def execute(self):
        
        self.reset()

        self.check()
        
        self.fetch_opcode()

        self.fetch_operands_and_compute()

        #print(self.machine.name, ":", self.logstr)
