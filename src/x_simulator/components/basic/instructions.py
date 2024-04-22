from x_simulator.core import instruction


class InstructionSet(
    instruction.InstructionSet, metaclass=instruction.InstructionSetMeta
):
    """Simple instruction set."""
