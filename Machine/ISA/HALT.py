from .Unit import Unit

class HALT(Unit):

    def __init__(self, machine):
        super().__init__(machine, "HALT")

    def fetch_operands_and_compute(self):

        # Execute
        self.machine.halted = True
