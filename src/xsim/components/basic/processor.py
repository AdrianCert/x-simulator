from xsim.components.basic.instructions import BaseInstruction
from xsim.core import asm_parser, processor


class BasicProcessor(processor.ProcessorBase):
    def __init__(self, rom_size: int, registers_spec: dict, flags_names):
        super().__init__(rom_size, registers_spec, flags_names=flags_names)
        self.program_data = []
        self.instruction_set = BaseInstruction()

    def update_program(self, program_data):
        self.program_data = program_data

    def execute_instruction(self, instruction_data):
        instruction: BaseInstruction = self.instruction_set.get_instruction(
            instruction_data["name"]
        )
        instruction.execute(self, **instruction_data["params"])

    def execute(self):
        self.pc = self.registers.take("pc")
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
            ("r0", 2),
            ("r1", 2),
            ("r2", 2),
            ("r3", 2),
            ("r4", 2),
            ("r5", 2),
            ("r6", 2),
            ("r7", 2),
            ("pc", 2),
            ("ir", 2),
            ("mar", 2),
            ("mdr", 2),
            ("sp", 2),
            ("sr", 2),
            ("lr", 2),
            ("sreg", 1),
        ],
    }

    proc = BasicProcessor(
        2048 * 2,
        registers_spec,
        flags_names=["I", "T", "H", "S", "V", "P", "Z", "C"],
    )

    print(sorted(proc.instruction_set.get_instruction_names()))

    program = asm_parser.AssemblyParser.load(
        # "program.s",
        "tests/source.asm",
        register_names=list(zip(*registers_spec["registers"]))[0],
    )
    proc.update_program(program)

    def debugger(processor: BasicProcessor, extra=None):
        # if processor.registers['PC'] not in [2]:
        #     return
        print(f"PC: {processor.registers['pc']}")
        print(f"R0: {processor.registers['R0']}")
        print(f"R1: {processor.registers['R1']}")
        print(f"R2: {processor.registers['R2']}")
        print(f"R3: {processor.registers['R3']}")
        print(f"R4: {processor.registers['R4']}")
        print(f"R5: {processor.registers['R5']}")
        print(f"R6: {processor.registers['R6']}")
        print(f"R7: {processor.registers['R7']}")
        print(f"IR: {processor.registers['IR']}")
        print(f"MAR: {processor.registers['MAR']}")
        print(f"MDR: {processor.registers['MDR']}")
        print(f"SP: {processor.registers['SP']}")
        print(f"SR: {processor.registers['SR']}")
        print(f"LR: {processor.registers['LR']}")
        print(f"SREG: {processor.registers['SREG']}")
        # print(processor.memory.dump())
        print()

    proc.attach_debugger(debugger)

    proc.run()
