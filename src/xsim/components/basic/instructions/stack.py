from xsim.core import processor

from .base import BaseInstruction


class Push(BaseInstruction):
    instruction_name = "PUSH"

    @classmethod
    def execute(cls, context: processor.ProcessorBase, source):
        source_size = cls.compute_require_size(context, *source)
        value = cls.resolve_operand(context, *source, size=source_size)

        context.registers["SP"] -= 2
        context.memory.write(context.registers["SP"], value, 2)


class Pop(BaseInstruction):
    instruction_name = "POP"

    @classmethod
    def execute(cls, context: processor.ProcessorBase, destination):
        destination_type, destination_value = destination
        if destination_type == "REG":
            context.registers[destination_value] = context.memory.read(
                context.registers["SP"], 2
            )
            context.registers["SP"] += 2
            return

        raise ValueError(f"Unknown destination type: {destination_type}")
