import itertools
import typing

import intervaltree


class Memory:
    def __init__(
        self,
        size: int,
        endianess: str = "big",
        memory: typing.Optional[typing.Union[memoryview, bytearray]] = None,
        origin=None,
    ):
        self.size = size
        self.endianess = endianess
        self.callbacks = []
        self.data = memory or bytearray(size)
        self.mv = memoryview(self.data)
        self.sub_views = intervaltree.IntervalTree()
        self.parent: typing.Optional[typing.Tuple[Memory, int]] = None
        self.origin = origin
        self.restricts = {
            "access_at_time": intervaltree.IntervalTree(),
        }

    def validate_address(self, address: int, size: int = 1):
        if address < 0 or address >= self.size:
            raise ValueError(f"Invalid address: {address}")
        if address + size > self.size:
            raise ValueError(f"Invalid address range: {address} - {address + size}")
        return True

    def get_limit_access_at_time(self, address, size: int = 1) -> int:
        bound = self.restricts["access_at_time"].overlap(address, address + size)
        if not bound:
            return size
        interval = bound.pop()
        limit = interval.data
        if limit < size:
            return limit
        return size

    def limit_access_at_time(self, address: int = 0, size: int = None, limit: int = 1):
        size = size or self.size
        if self.parent:
            return self.parent.limit_access_at_time(address + self.offset, size)

        self.restricts["access_at_time"][address : address + size] = limit

    def view(
        self, address: int, size: int = 1, restrict_access_at_time=None
    ) -> "Memory":
        assert self.validate_address(address, size)
        memory_view = MemoryView(self, address, size, origin=self.origin)
        if restrict_access_at_time:
            memory_view.limit_access_at_time(
                address=0, size=size, limit=restrict_access_at_time
            )
        self.sub_views[address : address + size] = memory_view
        return memory_view

    def read(self, address: int, size: int = 1) -> int:
        assert self.validate_address(address, size)
        self.on_read_hook(address, size)
        size = self.get_limit_access_at_time(address, size)
        if size == 1:
            return self.data[address]
        else:
            return int.from_bytes(self.data[address : address + size], self.endianess)

    def dump(self, size: int = 0, address: int = 0, bytes_per_row=16) -> str:
        assert self.validate_address(address, size)
        slice = self.mv
        if address > 0:
            slice = self.mv[address:]
        if size > 0:
            slice = slice[:size]

        bytes = slice.hex(" ").split(" ")
        rows = [
            " ".join(bytes[i : i + bytes_per_row])
            for i in range(0, len(bytes), bytes_per_row)
        ]
        return "\n".join(rows)

    def on_write_hook(self, address: int, values: list[int]):
        self.on_hook(address, values, trace=[id(self)], kind="write")

    def on_read_hook(self, address: int, size: int):
        self.on_hook(address, size, trace=[id(self)], kind="read")

    def on_hook(
        self, address, *args, trace: typing.Optional[list] = None, kind: str = "write"
    ):
        for c_kind, callback in self.callbacks:
            if c_kind == kind:
                callback(address, *args)
        if trace is None:
            trace = [id(self)]

        for item in itertools.chain(
            zip(itertools.repeat("subset"), self.sub_views[address]),
            [("parent", (self.parent, self.offset) if self.parent else None)],
        ):
            i_kind, _value = item
            if i_kind == "subset":
                memory = _value.data
                new_addr = address - _value.begin
            elif _value is not None:
                memory = _value[0]
                new_addr = address + _value[1]
            else:
                continue
            if id(memory) in trace:
                continue

            trace.append(id(memory))
            memory.on_hook(new_addr, *args, trace=trace, kind=kind)

    def on_write(self, callback):
        self.callbacks.append(("write", callback))
        return callback

    def on_read(self, callback):
        self.callbacks.append(("read", callback))
        return callback

    def __iter__(self):
        return iter(self.mv)

    def write(self, address: int, value: int, size: int = 1):
        size = self.get_limit_access_at_time(address, size)

        assert self.validate_address(address, size)
        bytes = value.to_bytes(size, self.endianess)
        bytes_len = len(bytes)
        if bytes_len == 1:
            self.data[address] = value
        else:
            self.data[address : address + bytes_len] = bytes
        self.on_write_hook(address, bytes)


class MemoryView(Memory):
    def __init__(self, memory: Memory, address: int, size: int, origin):
        super().__init__(
            size,
            memory.endianess,
            memory=memory.mv[address : address + size],
            origin=origin,
        )
        self.parent = memory
        self.offset = address


if __name__ == "__main__":
    ram = Memory(256)
    memory = ram.view(0x10, 0x10)

    def on_write(address, values):
        print(f"Write at {address}: {values}")

    memory.on_write(on_write)

    def on_read(address, size):
        print(f"Read at {address}: {size}")

    memory.on_read(on_read)
    ram.on_read(on_read)
    print(ram.dump())
    memory.write(0, 0x41)
    memory.write(1, 0x42)
    memory.write(2, 0x43)
    memory.write(3, 0x44)
    print(ram.dump())
    print(memory.read(0))
    print(memory.read(1))
    print(memory.read(2))
    print(memory.read(3))
