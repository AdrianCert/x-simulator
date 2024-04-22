import msvcrt
import os
import time

from x_simulator.core import memory

TOTAL_MEMORY = 1024
VIDEO_H_SIZE = 0x30
VIDEO_V_SIZE = 0x10
VIDEO_MEMORY_SIZE = VIDEO_H_SIZE * VIDEO_V_SIZE
VIDEO_MEMORY_LOCATION = TOTAL_MEMORY - VIDEO_MEMORY_SIZE


def clear_screen():
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Unix-based systems
        print("\033c", end="")


def write_to_video_memory(memory_dev: memory.Memory, address: int, value: str):
    for offset, byte in enumerate(value.encode("utf-8")):
        memory_dev.write(address + offset, byte)


class Blinker:
    def __init__(self, memory, cursor, char_placeholder="_", blink_interval=0.5):
        self.memory = memory
        self.prev_key = self.memory.read(cursor)
        self.blink_interval = blink_interval
        self.last_time = time.time()
        self.chr_placeholder = char_placeholder.encode("utf-8")[0]
        self.cursor = cursor
        self.show_placeholder = True
        self.memory.on_write(self.update_last_key)

    def update_last_key(self, address, value):
        if address != self.cursor:
            return
        if value[0] not in [self.prev_key, self.chr_placeholder]:
            self.prev_key = value[0]

    def blink(self, cursor):
        force = False
        if cursor != self.cursor:
            self.memory.write(self.cursor, self.prev_key)
            self.prev_key = self.memory.read(cursor)
            self.show_placeholder = True
            self.last_time = time.time()
            force = True
        self.cursor = cursor
        if not force and time.time() - self.last_time < self.blink_interval:
            return

        write_char = self.chr_placeholder if self.show_placeholder else self.prev_key
        self.show_placeholder = not self.show_placeholder
        self.last_time = time.time()
        self.memory.write(cursor, write_char)


class EditorApp:
    def __init__(self, memory):
        self.memory = memory
        self.cursor = 0
        self.blinker = Blinker(memory, self.cursor)
        self.fill(" ")
        self.render()
        self.memory.on_write(self.render)

    def fill(self, value: str):
        for i in range(VIDEO_MEMORY_SIZE):
            video_memory.write(i, value.encode("utf-8")[0])

    def render(self, address=0, values=0):
        clear_screen()
        print("/", "-" * VIDEO_H_SIZE, "\\", sep="")
        stream = video_memory.mv.tobytes().decode("utf-8")
        s_rows = [
            stream[i : i + VIDEO_H_SIZE] for i in range(0, len(stream), VIDEO_H_SIZE)
        ]
        print("|", end="")
        print(*s_rows, sep="|\n|", end="|\n")
        print("\\", "-" * VIDEO_H_SIZE, "/", sep="")
        print("Cursor at", address)

    def loop(self):
        if not msvcrt.kbhit():
            return
        key = msvcrt.getch()
        if key == b"\x1b":  # ESC key
            return True
        elif key == b"\xe0":  # Arrow key
            key = msvcrt.getch()  # Get the second character
            step = {b"H": -VIDEO_H_SIZE, b"P": VIDEO_H_SIZE, b"K": -1, b"M": 1}.get(key)
            if step is not None:
                self.cursor += step
                if 0 <= self.cursor < VIDEO_MEMORY_SIZE:
                    self.blinker.blink(self.cursor)
                    return
                self.cursor -= step
            return
        else:
            try:
                self.memory.write(self.cursor, key[0])
                self.cursor += 1
                if self.cursor >= VIDEO_MEMORY_SIZE:
                    self.cursor = 0
            except Exception as e:
                print(e)
                print(key)
                print("Invalid key")

    def run(self):
        while not self.loop():
            self.blinker.blink(self.cursor)


if __name__ == "__main__":
    rom = memory.Memory(TOTAL_MEMORY)
    video_memory = rom.view(VIDEO_MEMORY_LOCATION, VIDEO_MEMORY_SIZE)
    video_memory.write(0, 0x20)
    app = EditorApp(video_memory)
    app.run()
    print(video_memory.dump())
