import abc


class InstructionSetMeta(abc.ABCMeta):
    """Metaclass for registering classes in a registry."""

    def __new__(
        cls,
        name,
        bases,
        namespace,
    ):
        new_cls = super().__new__(cls, name, bases, namespace)
        cluster = new_cls.__mro__[-2].__name__
        if name == cluster:
            # If the class is the abstract class then add factory to it
            setattr(new_cls, "instruction_set", {})
            return new_cls
        else:
            # If the class is the concrete class then add it to the instruction set
            instruction_set = getattr(new_cls, "instruction_set")
            instruction_name = namespace.get("instruction_name")
            if instruction_name is not None:
                instruction_set[instruction_name] = new_cls

        return new_cls


class InstructionSet:
    """Base class for instruction sets."""
    instruction_set = {}

    def __init__(self, context=None):
        pass
        self.context = context

    def get_instruction(self, instruction_name):
        return self.instruction_set.get(instruction_name)

    def get_instruction_names(self):
        return list(self.instruction_set.keys())

    def execute(self, instruction_name, **kwargs):
        instruction = self.get_instruction(instruction_name)
        if instruction is None:
            raise ValueError(f"Unknown instruction: {instruction_name}")
        return instruction.execute(self.context, kwargs)

