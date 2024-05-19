import unittest
from unittest.mock import MagicMock

from src.xsim.core.memory import Memory, MemoryView


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.memory = Memory(256)

    def test_read_write(self):
        # Initial value at address 0 should be 0
        self.assertEqual(self.memory.read(0), 0)

        # Write some values to memory
        self.memory.write(0, 0x41)
        self.memory.write(1, 0x42)
        self.memory.write(2, 0x43)
        self.memory.write(3, 0x44)

        # Read the values back and verify
        self.assertEqual(self.memory.read(0), 0x41)
        self.assertEqual(self.memory.read(1), 0x42)
        self.assertEqual(self.memory.read(2), 0x43)
        self.assertEqual(self.memory.read(3), 0x44)

    def test_callback_on_read(self):
        callback_mock = MagicMock()

        # Register the callback
        self.memory.on_read(callback_mock)

        # Read a value from memory
        self.memory.read(0)

        # Check if the callback was called with the correct arguments
        callback_mock.assert_called_once_with(0, 1)


class TestMemoryView(unittest.TestCase):
    def setUp(self):
        self.parent_memory = Memory(256)
        self.memory_view = MemoryView(self.parent_memory, 0, 16, origin=None)

    def test_read_write(self):
        # Initial value at address 0 should be 0
        self.assertEqual(self.memory_view.read(0), 0)

        # Write some values to the memory view
        self.memory_view.write(0, 0x41)
        self.memory_view.write(1, 0x42)
        self.memory_view.write(2, 0x43)
        self.memory_view.write(3, 0x44)

        # Read the values back and verify
        self.assertEqual(self.memory_view.read(0), 0x41)
        self.assertEqual(self.memory_view.read(1), 0x42)
        self.assertEqual(self.memory_view.read(2), 0x43)
        self.assertEqual(self.memory_view.read(3), 0x44)


if __name__ == "__main__":
    unittest.main()
