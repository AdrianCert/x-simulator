import contextlib
import dataclasses
import json
import typing
from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Footer, Input, Label, TextArea
from textual.widgets.text_area import Selection

from xsim.components.basic.processor import BasicProcessor
from xsim.core import asm_parser, memory, processor


class AppConstrains:
    MEMORY_MULTIPLE = 1024
    MEMORY_KB_LIMIT = 64
    CLOCK_SPEED_LIMIT = 100


@dataclasses.dataclass
class AppConfiguration:
    memory_size: int = 2048
    registers_spec: dict = dataclasses.field(default_factory=dict)
    flags_names: list = dataclasses.field(default_factory=list)
    video_memory_size: int = 300
    video_memory_location: int = 0x100
    video_memory_w_size: int = 30
    video_memory_h_size: int = 10
    keyboard_memory_location: int = 0xFF
    clock_speed: int = 1
    program_path: str = "program.s"
    program: list = dataclasses.field(default_factory=list)
    register_names: list = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.validate_memory_size()
        self.validate_video_memory()
        self.validate_kb_memory()
        self.validate_registers_spec()
        self.validate_clock_speed()
        self.validate_flags_names()
        self.set_default_memory_mapped_registers()
        self.augment_fields()

    def augment_fields(self):
        self.register_names = [
            item["name"] for item in self.registers_spec["registers"]
        ]
        for _ in range(2):
            try:
                self.program = asm_parser.AssemblyParser.load(
                    self.program_path, register_names=self.register_names
                )
                break
            except Exception as exc:
                last_exc = exc
                continue
        if not self.program:
            raise last_exc
            # raise ValueError("Program path must be valid")

    def validate_clock_speed(self):
        if self.clock_speed < 0:
            raise ValueError("Clock speed must be a positive integer")

        if self.clock_speed > AppConstrains.CLOCK_SPEED_LIMIT:
            raise ValueError("Clock speed must be less than 100")

    def validate_memory_size(self):
        constrains = AppConstrains

        if self.memory_size < 0:
            raise ValueError("Memory size must be a positive integer")

        size_kb, remainder = divmod(self.memory_size, constrains.MEMORY_MULTIPLE)
        if remainder:
            raise ValueError("Memory size must be a multiple of 1024")

        if size_kb > constrains.MEMORY_KB_LIMIT:
            raise ValueError("Memory size must be less than 64KB")

    def validate_kb_memory(self):
        if self.keyboard_memory_location < 0:
            raise ValueError("Keyboard memory location must be a positive integer")
        if self.keyboard_memory_location + 1 > self.memory_size:
            raise ValueError("Keyboard memory location must be within memory size")

    def validate_video_memory(self):
        if self.video_memory_size < 0:
            raise ValueError("Video memory size must be a positive integer")

        if self.video_memory_location < 0:
            raise ValueError("Video memory location must be a positive integer")

        if self.video_memory_w_size < 0:
            raise ValueError("Video memory width size must be a positive integer")

        if self.video_memory_h_size < 0:
            raise ValueError("Video memory height size must be a positive integer")

        if self.video_memory_size < self.video_memory_w_size * self.video_memory_h_size:
            raise ValueError("Video memory size must be greater than width * height")

        if self.video_memory_location + self.video_memory_size > self.memory_size:
            raise ValueError("Video memory location must be within memory size")

    def validate_registers_spec(self):
        if not self.registers_spec:
            raise ValueError("Registers spec must be provided")

        if not self.registers_spec.get("registers"):
            raise ValueError("Registers must be provided")

    def validate_flags_names(self):
        if not self.flags_names:
            raise ValueError("Flags names must be provided")

    def set_default_memory_mapped_registers(self):
        if not self.registers_spec.get("memory_mapped"):
            self.registers_spec["memory_mapped"] = [0, 0]

    @classmethod
    def load(cls, path: str):
        data = json.loads(Path(path).read_text())
        return cls(**data)


class KeyboardComponent(Widget):
    DEFAULT_CSS = """
    KeyboardComponent {
        content-align: center middle;
    }
    """

    preview = reactive("")

    def __init__(
        self,
        memory_map: memory.MemoryView,
        buffer_size: int = 10,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.cursor = -1
        self.read_cursor = -1
        self.buffer_size = buffer_size
        self.buffer = bytearray([0x20] * self.buffer_size)
        self.memory_map = memory_map
        self.preview = self.buffer.decode("utf-8")

    def setup_memory_map(self):
        self.memory_map.on_read(self.on_memory_read)

    def on_memory_read(self, address: int, value: int) -> None:
        self.read_cursor = (self.read_cursor + 1) % self.buffer_size
        self.memory_map.write(0, self.buffer[self.read_cursor])

    def compose(self) -> ComposeResult:
        label_value = "keyboard buffer: " + self.preview
        yield Label(label_value, id="keyboard_label")
        yield Input(placeholder="Type here", id="keyboard_input")

    @on(Input.Changed)
    def on_input(self, event: Input.Changed) -> None:
        byte = event.value.encode("utf-8")
        if not byte:
            return
        byte = byte[0]

        self.query_one(Input).clear()
        self.cursor = (self.cursor + 1) % self.buffer_size
        self.buffer[self.cursor] = byte

        if self.read_cursor == -1:
            self.read_cursor = 0
            self.memory_map.write(0, self.buffer[self.cursor])

        self.preview = self.buffer.decode("utf-8")
        label = self.query_one(Label)
        label.update("keyboard buffer: " + self.preview)


class DisplayComponent(Widget):
    DEFAULT_CSS = """
    DisplayComponent {
        content-align: center middle;
    }
    """

    def __init__(
        self,
        video_memory: memory.MemoryView,
        screen_size: typing.Tuple[int, int],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.memory: memory.MemoryView = video_memory
        self.w_size, self.h_size = screen_size
        self.memory_size = self.w_size * self.h_size
        self.fill(" ")
        self.memory.on_write(self.trigger_update)

    def fill(self, value: str):
        for i in range(self.memory_size):
            self.memory.write(i, value.encode("utf-8")[0])

    def trigger_update(self, *args, **kwargs) -> None:
        self.refresh()

    def render(self) -> str:
        stream = self.memory.mv.tobytes().decode("utf-8")
        screen_lines = [
            stream[i : i + self.w_size] for i in range(0, len(stream), self.w_size)
        ]
        return "".join(
            [
                "/" + "-" * self.w_size + "\\\n|",
                "|\n|".join(screen_lines),
                "|\n\\" + "-" * self.w_size + "/",
            ]
        )


class Simulator(App):
    class Execute(Message):
        pass

    class Resource:
        program: typing.List[dict]
        processor: BasicProcessor
        execute: typing.Optional[typing.Callable]
        config: AppConfiguration
        video_memory: memory.MemoryView
        kb_memory: memory.MemoryView

    def __init__(self, config: AppConfiguration, **kwargs) -> None:
        super().__init__(**kwargs)
        self.resource = self.Resource()
        self.resource.program = config.program
        self.resource.processor = BasicProcessor(
            rom_size=config.memory_size,
            registers_spec=config.registers_spec,
            flags_names=config.flags_names,
        )
        self.resource.execute = None
        self.resource.config = config
        self.setup_simulator()

    def setup_simulator(self):
        self.resource.processor.update_program(self.resource.program)
        self.resource.video_memory = self.resource.processor.memory.view(
            address=self.resource.config.video_memory_location,
            size=self.resource.config.video_memory_size,
            restrict_access_at_time=1,
        )
        self.resource.kb_memory = self.resource.processor.memory.view(
            address=self.resource.config.keyboard_memory_location,
            restrict_access_at_time=1,
        )

    BINDINGS = [
        ("r", "run", "RUN/STOP"),
        ("s", "step", "step"),
        # ("b", "back", "breakpoint"),
        # ("c", "forward", "continue"),
    ]
    CSS_PATH = Path(__file__).parent / "gui.tcss"
    current_line = reactive(0)

    def compose(self) -> ComposeResult:
        code_source = Path(self.resource.config.program_path).read_text()
        code_editor = TextArea.code_editor(code_source, id="editor", read_only=True)
        code_editor.selection = Selection(
            (self.current_line, 0), (self.current_line, 0)
        )

        display = DisplayComponent(
            video_memory=self.resource.video_memory,
            screen_size=(
                self.resource.config.video_memory_w_size,
                self.resource.config.video_memory_h_size,
            ),
            id="display",
        )

        with Container(id="main"):
            with Vertical(id="left"):
                yield display
                yield KeyboardComponent(self.resource.kb_memory, id="keyboard")
            yield code_editor
        yield Footer()

    def action_step(self) -> None:
        if self.resource.execute is None:
            self.resource.execute = self.resource.processor.execute()
        self.post_message(self.Execute())

    def action_run(self) -> None:
        if self.resource.execute is None:
            self.resource.execute = self.resource.processor.execute()
            self.process_clock.resume()
        else:
            self.process_clock.pause()
            self.resource.execute = None
            self.current_line = 0
            text = self.query_one(TextArea)
            text.selection = Selection((self.current_line, 0), (self.current_line, 0))

    def on_simulator_execute(self, message: Execute) -> None:
        if self.resource.execute is None:
            return
        with contextlib.suppress(StopIteration):
            processor_state: processor.ProcessorBase = next(self.resource.execute)
            self.current_line = processor_state.pc.get()
            text = self.query_one(TextArea)
            text.selection = Selection((self.current_line, 0), (self.current_line, 0))
            return
        self.resource.execute = None

    def on_mount(self) -> None:
        def process_tick():
            self.post_message(self.Execute())

        self.process_clock = self.set_interval(
            1 / self.resource.config.clock_speed, process_tick, pause=True
        )


def main():
    config = AppConfiguration.load("config.json")
    app = Simulator(config=config)
    app.run()


if __name__ == "__main__":
    main()
