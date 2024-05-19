import unittest
from unittest.mock import MagicMock

import intervaltree
from xsim.core.memory import Memory, MemoryView


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


class TestGetLimitAccessAtTime(unittest.TestCase):
    def setUp(self):
        self.memory = Memory(256)

    def test_limit_less_than_size(self):
        # Set up restricts
        self.memory.restricts["access_at_time"] = intervaltree.IntervalTree()
        self.memory.restricts["access_at_time"].add(
            intervaltree.Interval(0, 10, data=5)
        )

        # Test when limit is less than size
        address = 0
        size = 8
        limit = self.memory.get_limit_access_at_time(address, size)
        self.assertEqual(limit, 5)

    def test_limit_greater_than_size(self):
        # Set up restricts
        self.memory.restricts["access_at_time"] = intervaltree.IntervalTree()
        self.memory.restricts["access_at_time"].add(
            intervaltree.Interval(0, 10, data=15)
        )

        # Test when limit is greater than size
        address = 0
        size = 8
        limit = self.memory.get_limit_access_at_time(address, size)
        self.assertEqual(limit, 8)

    def test_no_restricts(self):
        # Test when there are no restricts set
        address = 0
        size = 8
        limit = self.memory.get_limit_access_at_time(address, size)
        self.assertEqual(limit, 8)


class TestMemoryDumping(unittest.TestCase):
    def setUp(self):
        self.memory = Memory(256)

    def test_dump_with_size_and_address(self):
        # Set up memory values
        self.memory.write(0, 0x41)
        self.memory.write(1, 0x42)
        self.memory.write(2, 0x43)
        self.memory.write(3, 0x44)

        # Dump memory with size and address
        dump_result = self.memory.dump(size=4, address=0, bytes_per_row=16)

        # Verify the dumped result
        expected_result = "41 42 43 44"
        self.assertEqual(dump_result, expected_result)

    def test_dump_with_address_only(self):
        # Set up memory values
        self.memory.write(0, 0x41)
        self.memory.write(1, 0x42)
        self.memory.write(2, 0x43)
        self.memory.write(3, 0x44)

        # Dump memory with address only
        dump_result = self.memory.dump(size=2, address=2, bytes_per_row=16)

        # Verify the dumped result
        expected_result = "43 44"
        self.assertEqual(dump_result, expected_result)

    def test_dump_with_size_only(self):
        # Set up memory values
        self.memory.write(0, 0x41)
        self.memory.write(1, 0x42)
        self.memory.write(2, 0x43)
        self.memory.write(3, 0x44)

        # Dump memory with size only
        dump_result = self.memory.dump(size=2, bytes_per_row=16)

        # Verify the dumped result
        expected_result = "41 42"
        self.assertEqual(dump_result, expected_result)

    def test_dump_without_size_and_address(self):
        # Set up memory values
        self.memory.write(0, 0x41)
        self.memory.write(1, 0x42)
        self.memory.write(2, 0x43)
        self.memory.write(3, 0x44)

        # Dump memory without size and address
        dump_result = self.memory.dump(size=4, bytes_per_row=16)

        # Verify the dumped result
        expected_result = "41 42 43 44"
        self.assertEqual(dump_result, expected_result)


class TestMemoryHooks(unittest.TestCase):
    def setUp(self):
        self.memory = Memory(256)

    def test_on_write_callback(self):
        callback_mock = MagicMock()

        # Register the callback
        self.memory.on_write(callback_mock)

        # Write a value to memory
        self.memory.write(0, 0x41)

        # Check if the callback was called with the correct arguments
        callback_mock.assert_called_once()

    def test_on_write_callback_with_memory_view(self):
        callback_mock = MagicMock()

        # Create a memory view
        memory_view = MemoryView(self.memory, 0, 16, origin=None)

        # Register the callback
        memory_view.on_write(callback_mock)

        # Write a value to the memory view
        memory_view.write(0, 0x41)

        # Check if the callback was called with the correct arguments
        callback_mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
