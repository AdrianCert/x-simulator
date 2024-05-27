import abc
import typing

from xsim.core import memory


class ProcessorRegister:
    def __init__(self, name, size, memory_view=None):
        self.name = name
        self.size = size
        self.value = memory_view or memory.Memory(size)

    def bind(self, memory: memory.MemoryView):
        self.value = memory

    def get(self):
        return self.value.read(0, self.size)

    def set(self, value):
        self.value.write(0, value, self.size)


class ProcessorRegisters:
    def __init__(self, memory_view: memory.MemoryView, registers=None):
        self.memory = memory_view or memory.Memory(32)
        self.resisters = {}
        self.registers_addr = {}
        current_address = 0
        left_space = self.memory.size
        left_mapped = -1
        for seq, register in enumerate(registers or []):
            label = register["name"]
            size = register["size"]
            if size > left_space:
                left_mapped = seq
                break
            self.resisters[label] = ProcessorRegister(
                label, size, self.memory.view(current_address, size)
            )
            if "default" in register:
                self.resisters[label].set(register["default"])
            self.registers_addr[current_address] = label
            current_address += size
            left_space -= size

        if left_mapped != -1:
            unmapped_registers = registers[left_mapped:]
            self.unmapped_memory = memory.Memory(
                sum(reg["size"] for reg in unmapped_registers)
            )
            current_address = 0
            for register in unmapped_registers:
                label = register["name"]
                size = register["size"]
                self.resisters[label] = ProcessorRegister(
                    label, size, self.unmapped_memory.view(current_address, size)
                )
                if "default" in register:
                    self.resisters[label].set(register["default"])
                current_address += size

    def take(
        self, register: typing.Union[int, str]
    ) -> typing.Optional[ProcessorRegister]:
        if isinstance(register, int):
            if register not in self.registers_addr:
                return None
            register = self.registers_addr[register]
        return self.resisters[register.lower()]

    def __getitem__(self, item: typing.Union[int, str]):
        return self.take(item).get()

    def __setitem__(self, key: typing.Union[int, str], value):
        self.take(key).set(value)


class ProcessorBase:
    dbc: typing.Optional[typing.Callable[["ProcessorBase"], None]] = None

    def __init__(self, rom_size: int, registers_spec: dict, flags_names=None):
        self.memory = memory.Memory(rom_size)
        self.registers_sizes = {
            item["name"]: item["size"] for item in registers_spec["registers"]
        }
        self.registers = self.make_registers_space(registers_spec)
        self.flags_mask = {
            flag: 2**i for i, flag in enumerate(reversed(flags_names) or [])
        }
        self.halt = False

    def make_registers_space(self, registers_spec: dict):
        memory_mapped_start, memory_mapped_stop = registers_spec.get(
            "memory_mapped", (0, 0)
        )
        memory_mapped_size = memory_mapped_stop - memory_mapped_start
        if memory_mapped_size:
            memory_mapped = self.memory.view(memory_mapped_start, memory_mapped_size)
        else:
            memory_mapped = memory.Memory(0)
        return ProcessorRegisters(memory_mapped, registers=registers_spec["registers"])

    def attach_debugger(self, dbc):
        self.dbc = dbc

    def detach_debugger(self):
        """
        Detaches the debugger from the processor.
        """
        self.dbc = None

    @abc.abstractmethod
    def execute(self): ...

    def run(self):
        self.executors = self.execute()
        while True:
            try:
                nfo = next(self.executors)
            except StopIteration:
                break
            if self.dbc:
                self.dbc(self, nfo)
            if self.halt:
                break
