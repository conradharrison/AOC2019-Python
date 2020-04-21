from .Unit import Unit

class OUT(Unit):

    def __init__(self, machine):
        super().__init__(machine, "OUT")

    def fetch_operands_and_compute(self):

        result = self.fetch_operand()

        # Execute
        self.machine.outputs.append(result)
        self.machine.output_ready = True
