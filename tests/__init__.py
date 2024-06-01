class HookedByteArray(bytearray):
    def __init__(self, *args, **kwargs):
        self.write_callback = kwargs.pop("write_callback", None)
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        # Call the write callback before writing the data
        if self.write_callback:
            self.write_callback(key, value)
        super().__setitem__(key, value)


# Define a callback function
def on_write(key, value):
    print(f"Writing {value} to index {key}")


data = HookedByteArray(20, write_callback=on_write)
view = memoryview(data)[5:15]

data[0] = 0xFF
data[0] = 0xE
view[0] = 0x10
view[3] = 0x20
view[-1] = 0x30
print(memoryview(data).hex(" "))
print(memoryview(view).hex(" "))
