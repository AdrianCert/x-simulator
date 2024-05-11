from xsim.core import processor

from .base import BaseInstruction


class JumpInstruction(BaseInstruction):
    @classmethod
    def check_condition(cls, context: processor.ProcessorBase):
        ...

    @classmethod
    def execute(cls, context: processor.ProcessorBase, address):
        if cls.check_condition(context):
            address_value = cls.resolve_operand(context, *address)
            context.registers["PC"] = address_value


class Jmp(JumpInstruction):
    instruction_name = "JMP"

    @classmethod
    def check_condition(cls, context: processor.ProcessorBase):
        return True


class Jz(JumpInstruction):
    instruction_name = "JZ"

    @classmethod
    def check_condition(cls, context: processor.ProcessorBase):
        return context.registers["SREG"] & context.flags_mask["Z"]


class Jeq(Jz):
    instruction_name = "JEQ"


class Jne(JumpInstruction):
    instruction_name = "JNE"

    @classmethod
    def check_condition(cls, context: processor.ProcessorBase):
        return not context.registers["SREG"] & context.flags_mask["Z"]


class Jnz(Jne):
    instruction_name = "JNZ"


class Jl(JumpInstruction):
    instruction_name = "JL"

    @classmethod
    def check_condition(cls, context: processor.ProcessorBase):
        return context.registers["SREG"] & context.flags_mask["S"]


class Jg(JumpInstruction):
    instruction_name = "JG"

    @classmethod
    def check_condition(cls, context: processor.ProcessorBase):
        return (
            not context.registers["SREG"] & context.flags_mask["Z"]
            and not context.registers["SREG"] & context.flags_mask["S"]
        )


class Jge(JumpInstruction):
    instruction_name = "JGE"

    @classmethod
    def check_condition(cls, context: processor.ProcessorBase):
        return not context.registers["SREG"] & context.flags_mask["S"]


class Jle(JumpInstruction):
    instruction_name = "JLE"

    @classmethod
    def check_condition(cls, context: processor.ProcessorBase):
        return (
            context.registers["SREG"] & context.flags_mask["Z"]
            or context.registers["SREG"] & context.flags_mask["S"]
        )
