from xsim.core import const, processor

from .base import BaseInstruction


class ArithmeticInstructionSet(BaseInstruction):
    @classmethod
    def arithmetic_compute(cls, context, source, destination):
        ...

    @classmethod
    def flags_compute(cls, result):
        yield "S", result & const.SIGN_U16 != 0
        yield "Z", result & const.MAX_U16 == 0
        yield "P", const.parity(result & const.MAX_U16)
        yield "C", result > const.MAX_U16

    @classmethod
    def execute(
        cls, context: processor.ProcessorBase, destination, source=None, **kwargs
    ):
        source_op_value = cls.resolve_operand(context, *source, size=2) if source else 0
        destination_op_value = cls.resolve_operand(context, *destination, size=2)
        result, *flags = cls.arithmetic_compute(
            context, source_op_value, destination_op_value
        )

        seated_flags = dict(flags)

        mask_set, mask_cls = zip(
            *[
                (flag_mask, 0) if flag_name in seated_flags else (0, flag_mask)
                for flag_name, flag_mask in context.flags_mask.items()
            ]
        )

        flag_reg = context.registers.take("SREG")
        flag_reg.set(
            const.set_bits(
                const.mask(
                    flag_reg.get(),
                    sum(mask_cls),
                ),
                sum(mask_set),
            )
        )

        if "read_only" in kwargs and kwargs["read_only"]:
            return

        if destination[0] == "REG":
            context.registers[destination[1]] = result
        elif destination[0] == "ADDR":
            address = cls.resolve_operand(context, *destination[1])
            context.memory.write(address, result, 2)
        else:
            context.memory.write(destination_op_value, result)


class Cmp(ArithmeticInstructionSet):
    instruction_name = "CMP"

    @classmethod
    def arithmetic_compute(cls, context, source, destination):
        result = destination - source
        yield result & const.MAX_U16
        yield from cls.flags_compute(result)

    @classmethod
    def execute(cls, context: processor.ProcessorBase, source, destination):
        super().execute(context, source, destination, read_only=True)


class Add(ArithmeticInstructionSet):
    instruction_name = "ADD"

    @classmethod
    def arithmetic_compute(cls, context, source, destination, carry=False):
        result = source + destination + int(carry)
        yield result & const.MAX_U16
        yield from cls.flags_compute(result)


class Sub(ArithmeticInstructionSet):
    instruction_name = "SUB"

    @classmethod
    def arithmetic_compute(cls, context, source, destination, carry=False):
        result = destination - source - int(carry)
        yield result & const.MAX_U16
        yield from cls.flags_compute(result)


class Mul(ArithmeticInstructionSet):
    instruction_name = "MUL"

    @classmethod
    def arithmetic_compute(cls, context, source, destination):
        result = source * destination
        yield result & const.MAX_U16
        yield from cls.flags_compute(result)


class Div(ArithmeticInstructionSet):
    instruction_name = "DIV"

    @classmethod
    def arithmetic_compute(cls, context, source, destination):
        result = destination // source
        yield result & const.MAX_U16
        yield from cls.flags_compute(result)


class Inc(ArithmeticInstructionSet):
    instruction_name = "INC"

    @classmethod
    def arithmetic_compute(cls, context, source, destination):
        result = destination + 1
        yield result & const.MAX_U16
        yield from cls.flags_compute(result)


class Dec(ArithmeticInstructionSet):
    instruction_name = "DEC"

    @classmethod
    def arithmetic_compute(cls, context, source, destination):
        result = destination - 1
        yield result & const.MAX_U16
        yield from cls.flags_compute(result)
