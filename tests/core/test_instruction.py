import unittest
from unittest.mock import MagicMock

from xsim.core.instruction import InstructionSet


class TestInstructionSet(unittest.TestCase):
    def setUp(self):
        self.instruction_set = InstructionSet()

    def test_get_instruction(self):
        # Test getting an existing instruction
        self.instruction_set.instruction_set = {"ADD": MagicMock()}
        instruction = self.instruction_set.get_instruction("ADD")
        self.assertIsInstance(instruction, MagicMock)

        # Test getting a non-existing instruction
        instruction = self.instruction_set.get_instruction("SUB")
        self.assertIsNone(instruction)

    def test_get_instruction_names(self):
        # Test getting instruction names
        self.instruction_set.instruction_set = {"ADD": MagicMock(), "SUB": MagicMock()}
        instruction_names = self.instruction_set.get_instruction_names()
        self.assertListEqual(instruction_names, ["ADD", "SUB"])

    def test_execute_existing_instruction(self):
        # Test executing an existing instruction
        instruction_mock = MagicMock()
        instruction_mock.execute.return_value = "Result"
        self.instruction_set.instruction_set = {"ADD": instruction_mock}
        result = self.instruction_set.execute("ADD", arg1=1, arg2=2)
        self.assertEqual(result, "Result")
        instruction_mock.execute.assert_called_once_with(self.instruction_set.context, {"arg1": 1, "arg2": 2})

    def test_execute_non_existing_instruction(self):
        # Test executing a non-existing instruction
        self.instruction_set.instruction_set = {}
        with self.assertRaises(ValueError):
            self.instruction_set.execute("SUB", arg1=1, arg2=2)


if __name__ == "__main__":
    unittest.main()