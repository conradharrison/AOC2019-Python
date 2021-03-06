from .Unit import Unit

class JMPT(Unit):

    def __init__(self, machine):
        super().__init__(machine, "JMPT")

    def fetch_operands_and_compute(self):

        cond = self.fetch_operand()
        addr = self.fetch_operand()

        # Execute
        if cond != 0:
            self.machine.ipointer = addr
