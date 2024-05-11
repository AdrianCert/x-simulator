import typing

from x_simulator.core import const, instruction, processor


class InstructionSet(
    instruction.InstructionSet, metaclass=instruction.InstructionSetMeta
):
    """Simple instruction set."""

    @staticmethod
    def resolve_operand(
        context: processor.ProcessorBase, operand_type: str, operand_value: str
    ) -> typing.Optional[int]:
        if operand_type == "CONST":
            return operand_value
        elif operand_type == "REG":
            return context.registers[operand_value]
        else:
            raise ValueError(f"Unknown operand type: {operand_type}")


class ArithmeticInstructionSet(InstructionSet):
    @classmethod
    def arithmetic_compute(cls, context, source, destination): ...

    @classmethod
    def flags_compute(cls, result):
        yield "S", result & 0x80 != 0
        yield "Z", result & const.MAX_U16 == 0
        yield "P", const.parity(result & const.MAX_U16)
        yield "C", result > const.MAX_U16

    @classmethod
    def execute(cls, context: processor.ProcessorBase, source, destination):
        source_op_value = cls.resolve_operand(context, *source)
        destination_op_value = cls.resolve_operand(context, *destination)
        result, *flags = cls.arithmetic_compute(
            context, source_op_value, destination_op_value
        )

        context.registers[destination[1]] = result
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


class Mov(InstructionSet):
    instruction_name = "MOV"

    @staticmethod
    def execute(context, source, destination):
        source_type, source_value = source
        if source_type == "CONST":
            value = source_value
        elif source_type == "REG":
            value = context.registers[source_value]
        else:
            raise ValueError(f"Unknown source type: {source_type}")

        destination_type, destination_value = destination
        if destination_type == "REG":
            context.registers[destination_value] = value
        else:
            raise ValueError(f"Unknown destination type: {destination_type}")
