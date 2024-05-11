from xsim.core import processor

from .base import BaseInstruction


class Call(BaseInstruction):
    instruction_name = "CALL"

    @classmethod
    def execute(cls, context: processor.ProcessorBase, destination):
        address_value = cls.resolve_operand(context, *destination)
        context.registers["SP"] -= 2
        context.memory.write(context.registers["SP"], context.registers["PC"], 2)
        context.registers["PC"] = address_value


class Ret(BaseInstruction):
    instruction_name = "RET"

    @classmethod
    def execute(cls, context: processor.ProcessorBase):
        context.registers["PC"] = context.memory.read(context.registers["SP"], 2)
        context.registers["SP"] += 2
