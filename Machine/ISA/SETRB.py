from .Unit import Unit

class SETRB(Unit):

    def __init__(self, machine):
        super().__init__(machine, "SETRB")

    def fetch_operands_and_compute(self):

        i1 = self.fetch_operand()

        # Execute
        self.machine.relative_base = self.machine.relative_base + i1
