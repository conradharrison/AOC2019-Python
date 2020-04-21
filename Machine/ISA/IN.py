from .Unit import Unit

class IN(Unit):

    def __init__(self, machine):
        super().__init__(machine, "IN")

    def fetch_operands_and_compute(self):

        o = self.fetch_operand(is_dest=True) 

        # Execute
        result = self.machine.inputs.pop(0)
        self.machine.write_mem(o, result)
