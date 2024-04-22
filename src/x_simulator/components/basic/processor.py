from x_simulator.components.basic import instructions
from x_simulator.core import memory


class Processor:
    def __init__(self, rom_size, program_data):
        self.memory = memory.Memory(rom_size)
        self.program_data = program_data
        self.instruction_set = instructions.InstructionSet()
        self.sreg = 0
        self.pc = 0
        self.accumulator = 0

    def run(self):
        while True:
            self.execute_next()

    def execute_next(self):
        instruction_data = self.program_data[self.pc]
        self.pc += 1
        instruction: instructions.InstructionSet = self.instruction_set.get_instruction(instruction_data["name"])
        instruction.execute(self, **instruction_data["params"])