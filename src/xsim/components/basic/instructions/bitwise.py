from xsim.core import processor

from .base import BaseInstruction


class BitwiseInstructionSet(BaseInstruction):
    @classmethod
    def compute_result(cls, context, source, destination): ...

    @classmethod
    def execute(cls, context: processor.ProcessorBase, source, destination):
        source_op_value = cls.resolve_operand(context, *source, size=2)
        destination_op_value = cls.resolve_operand(context, *destination, size=2)
        result = cls.compute_result(context, source_op_value, destination_op_value)

        if destination[0] == "REG":
            context.registers[destination[1]] = result
        elif destination[0] == "ADDR":
            address = cls.resolve_operand(context, *destination[1])
            context.memory.write(address, result, 2)


class And(BitwiseInstructionSet):
    instruction_name = "AND"

    @classmethod
    def compute_result(cls, context, source, destination):
        return source & destination


class Or(BitwiseInstructionSet):
    instruction_name = "OR"

    @classmethod
    def compute_result(cls, context, source, destination):
        return source | destination


class Xor(BitwiseInstructionSet):
    instruction_name = "XOR"

    @classmethod
    def compute_result(cls, context, source, destination):
        return source ^ destination


class Not(BitwiseInstructionSet):
    instruction_name = "NOT"

    @classmethod
    def compute_result(cls, context, source, destination):
        return ~source


class Shl(BitwiseInstructionSet):
    instruction_name = "SHL"

    @classmethod
    def compute_result(cls, context, source, destination):
        return source << destination


class Shr(BitwiseInstructionSet):
    instruction_name = "SHR"

    @classmethod
    def compute_result(cls, context, source, destination):
        return source >> destination
