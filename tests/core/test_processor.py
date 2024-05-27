import unittest
from unittest.mock import MagicMock

from xsim.core.memory import Memory, MemoryView
from xsim.core.processor import ProcessorBase, ProcessorRegister, ProcessorRegisters


class TestProcessorRegister(unittest.TestCase):

    def test_init(self):
        register = ProcessorRegister("r0", 2)
        self.assertEqual(register.name, "r0")
        self.assertEqual(register.size, 2)
        self.assertIsInstance(register.value, Memory)

    def test_bind(self):
        register = ProcessorRegister("r0", 2)
        memory = Memory(4)
        view = memory.view(0, 4)
        register.bind(view)
        self.assertIsInstance(register.value, MemoryView)
        self.assertEqual(register.value, view)

    def test_get(self):
        register = ProcessorRegister("r0", 2)
        register.set(42)
        self.assertEqual(register.get(), 42)

    def test_set(self):
        register = ProcessorRegister("r0", 2)
        register.set(42)
        self.assertEqual(register.get(), 42)


class TestProcessorRegisters(unittest.TestCase):

    def setUp(self):
        self.memory_view = Memory(100)
        self.registers = [
            {"name": "r0", "size": 2},
            {"name": "r1", "size": 2},
            {"name": "r2", "size": 2},
            {"name": "r3", "size": 2},
        ]
        self.processor_registers = ProcessorRegisters(self.memory_view, self.registers)

    def test_get_existing_register_by_name(self):
        self.processor_registers.take = MagicMock(
            return_value=MagicMock(get=MagicMock(return_value=42))
        )
        value = self.processor_registers["r0"]
        self.assertEqual(value, 42)
        self.processor_registers.take.assert_called_once_with("r0")

    def test_get_existing_register_by_index(self):
        self.processor_registers.take = MagicMock(
            return_value=MagicMock(get=MagicMock(return_value=42))
        )
        value = self.processor_registers[0]
        self.assertEqual(value, 42)
        self.processor_registers.take.assert_called_once_with(0)

    def test_set_existing_register_by_name(self):
        self.processor_registers.take = MagicMock()
        self.processor_registers["r0"] = 42
        self.processor_registers.take.assert_called_once_with("r0")
        self.processor_registers.take.return_value.set.assert_called_once_with(42)

    def test_set_existing_register_by_index(self):
        self.processor_registers.take = MagicMock()
        self.processor_registers[0] = 42
        self.processor_registers.take.assert_called_once_with(0)
        self.processor_registers.take.return_value.set.assert_called_once_with(42)


class TestProcessorBase(unittest.TestCase):

    def setUp(self):
        self.processor = ProcessorBase(
            2048 * 2,
            {
                "memory_mapped": [0, 16],
                "registers": [
                    {"name": "r0", "size": 2},
                    {"name": "r1", "size": 2},
                    {"name": "r2", "size": 2},
                    {"name": "r3", "size": 2},
                    {"name": "r4", "size": 2},
                    {"name": "r5", "size": 2},
                    {"name": "r6", "size": 2},
                    {"name": "r7", "size": 2},
                    {"name": "pc", "size": 2},
                    {"name": "ir", "size": 2},
                    {"name": "mar", "size": 2},
                    {"name": "mdr", "size": 2},
                    {"name": "sp", "size": 2},
                    {"name": "sr", "size": 2},
                    {"name": "lr", "size": 2},
                    {"name": "sreg", "size": 1},
                ],
            },
            flags_names=["I", "T", "H", "S", "V", "P", "Z", "C"],
        )
        self.mock_dbc = MagicMock()

    def test_make_registers_space(self):
        # Verifies if the registers space is created correctly
        registers_spec = {
            "memory_mapped": [0, 16],
            "registers": [
                {"name": "r0", "size": 2},
                {"name": "r1", "size": 2},
                {"name": "r2", "size": 2},
                {"name": "r3", "size": 2},
                {"name": "r4", "size": 2},
                {"name": "r5", "size": 2},
                {"name": "r6", "size": 2},
                {"name": "r7", "size": 2},
                {"name": "pc", "size": 2},
                {"name": "ir", "size": 2},
                {"name": "mar", "size": 2},
                {"name": "mdr", "size": 2},
                {"name": "sp", "size": 2},
                {"name": "sr", "size": 2},
                {"name": "lr", "size": 2},
                {"name": "sreg", "size": 1},
            ],
        }
        registers_space = self.processor.make_registers_space(registers_spec)
        self.assertEqual(registers_space.memory.size, 16)

    def test_attach_debugger(self):
        # Verifies if the debugger is attached correctly
        self.processor.attach_debugger(self.mock_dbc)
        self.assertEqual(self.processor.dbc, self.mock_dbc)

    def test_detach_debugger(self):
        # Verifies if the debugger is detached correctly
        self.processor.dbc = self.mock_dbc
        self.processor.detach_debugger()
        self.assertIsNone(self.processor.dbc)


if __name__ == "__main__":
    unittest.main()
