from x_simulator.components.basic import instructions
from x_simulator.core import processor


class BasicProcessor(processor.ProcessorBase):
    def __init__(self, rom_size: int, registers_spec: dict, program_data, flags_names):
        super().__init__(rom_size, registers_spec, flags_names=flags_names)
        self.program_data = program_data
        self.instruction_set = instructions.InstructionSet()

    def execute_instruction(self, instruction_data):
        instruction: instructions.InstructionSet = self.instruction_set.get_instruction(
            instruction_data["name"]
        )
        instruction.execute(self, **instruction_data["params"])

    def execute(self):
        self.pc = self.registers.take("PC")
        while True:
            current_address = self.pc.get()
            if self.pc.get() >= len(self.program_data):
                break
            instruction_data = self.program_data[self.pc.get()]
            self.pc.set(current_address + 1)
            self.execute_instruction(instruction_data)
            yield self


if __name__ == "__main__":

    registers_spec = {
        "memory_mapped": [0, 16],
        "registers": [
            ("R1", 2),
            ("R2", 2),
            ("R3", 2),
            ("R4", 2),
            ("R5", 2),
            ("R6", 2),
            ("R7", 2),
            ("R8", 2),
            ("PC", 2),
            ("IR", 2),
            ("MAR", 2),
            ("MDR", 2),
            ("SP", 2),
            ("SR", 2),
            ("LR", 2),
            ("SREG", 1),
        ],
    }

    proc = BasicProcessor(
        20,
        registers_spec,
        program_data=[
            {
                "name": "MOV",
                "params": {
                    "source": ["CONST", 0x10],
                    "destination": ["REG", "R1"],
                },
            },
            {
                "name": "MOV",
                "params": {
                    "source": ["CONST", 0x20],
                    "destination": ["REG", "R2"],
                },
            },
            {
                "name": "ADD",
                "params": {
                    "source": ["REG", "R1"],
                    "destination": ["REG", "R2"],
                },
            },
        ],
        flags_names=['I', 'T', 'H', 'S', 'V', 'P', 'Z', 'C'],
    )

    def debugger(processor: BasicProcessor):
        print(f"PC: {processor.registers['PC']}")
        print(f"R1: {processor.registers['R1']}")
        print(f"R2: {processor.registers['R2']}")
        print(f"R3: {processor.registers['R3']}")
        print(f"R4: {processor.registers['R4']}")
        print(f"R5: {processor.registers['R5']}")
        print(f"R6: {processor.registers['R6']}")
        print(f"R7: {processor.registers['R7']}")
        print(f"R8: {processor.registers['R8']}")
        print(f"IR: {processor.registers['IR']}")
        print(f"MAR: {processor.registers['MAR']}")
        print(f"MDR: {processor.registers['MDR']}")
        print(f"SP: {processor.registers['SP']}")
        print(f"SR: {processor.registers['SR']}")
        print(f"LR: {processor.registers['LR']}")
        print(f"SREG: {processor.registers['SREG']}")
        print(processor.memory.dump())
        print("")

    proc.attach_debugger(debugger)

    proc.run()
