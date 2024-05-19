import unittest
from unittest.mock import MagicMock

from xsim.core.memory import Memory, MemoryView
from xsim.core.processor import ProcessorRegister, ProcessorRegisters


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
        self.processor_registers.take = MagicMock(return_value=MagicMock(get=MagicMock(return_value=42)))
        value = self.processor_registers["r0"]
        self.assertEqual(value, 42)
        self.processor_registers.take.assert_called_once_with("r0")

    def test_get_existing_register_by_index(self):
        self.processor_registers.take = MagicMock(return_value=MagicMock(get=MagicMock(return_value=42)))
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


if __name__ == '__main__':
    unittest.main()