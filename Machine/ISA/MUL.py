from .Unit import Unit

class MUL(Unit):

    def __init__(self, machine):
        super().__init__(machine, "MUL")

    def fetch_operands_and_compute(self):

        i1 = self.fetch_operand()
        i2 = self.fetch_operand()

        o = self.fetch_operand(is_dest=True)

        # Execute
        result = i1 * i2
        self.machine.write_mem(o, result)
