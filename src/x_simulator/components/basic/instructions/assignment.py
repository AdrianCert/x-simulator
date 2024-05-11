from x_simulator.core import processor

from .base import BaseInstruction


class Mov(BaseInstruction):
    instruction_name = "MOV"

    @classmethod
    def execute(cls, context: processor.ProcessorBase, source, destination):
        source_size = cls.compute_require_size(context, *destination)
        value = cls.resolve_operand(context, *source, size=source_size)

        destination_type, destination_value = destination
        if destination_type == "ADDR":
            address = cls.resolve_operand(context, *destination_value)
            context.memory.write(address, value, size=source_size)
            return

        if destination_type == "REG":
            context.registers[destination_value] = value
            return

        raise ValueError(f"Unknown destination type: {destination_type}")
