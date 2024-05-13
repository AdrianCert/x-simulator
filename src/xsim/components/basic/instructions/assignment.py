from xsim.core import processor

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


class Db(BaseInstruction):
    instruction_name = "DB"

    @classmethod
    def execute(cls, context: processor.ProcessorBase, destination, source):
        address = cls.resolve_operand(context, *destination, size=1)

        source_type, source = source

        if source_type == "CONST":
            context.memory.write(address, source, size=1)
            return

        if source_type == "STRING" and isinstance(source, str):
            source = source.encode("utf-8")
            for offset, byte in enumerate(source):
                context.memory.write(address + offset, byte)
            return

        raise ValueError(f"Incorrect source type: {source} ({type(source)})")
