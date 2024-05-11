import typing

from x_simulator.core import instruction, processor


class BaseInstruction(
    instruction.InstructionSet, metaclass=instruction.InstructionSetMeta
):
    """Simple instruction set."""

    @classmethod
    def compute_require_size(
        cls, context: processor.ProcessorBase, operand_type, operand_value
    ):
        if operand_type == "ADDR":
            return 2
        if operand_type == "REG":
            return context.registers[operand_value]
        return 1

    @classmethod
    def resolve_operand(
        cls,
        context: processor.ProcessorBase,
        operand_type: str,
        operand_value: typing.Union[str, int],
        size: int = 1,
    ) -> typing.Optional[int]:
        if operand_type == "ADDR":
            require_size = cls.compute_require_size(context, *operand_value)
            return context.memory.read(
                cls.resolve_operand(context, *operand_value),
                require_size,
            )

        if operand_type == "CONST":
            return operand_value

        if operand_type == "REG":
            return context.registers[operand_value]

        raise ValueError(f"Unknown operand type: {operand_type}")


class Nop(BaseInstruction):
    instruction_name = "NOP"

    @staticmethod
    def execute(context: processor.ProcessorBase, **kwargs):
        pass


class Halt(BaseInstruction):
    instruction_name = "HALT"

    @staticmethod
    def execute(context: processor.ProcessorBase, **kwargs):
        context.halt = True
