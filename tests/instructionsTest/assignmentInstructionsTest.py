import unittest
from unittest.mock import MagicMock, create_autospec
from xsim.core import processor
from src.xsim.components.basic.instructions.assignment import Mov


class TestMovInstruction(unittest.TestCase):

    def setUp(self):
        self.context = create_autospec(processor.ProcessorBase)
        self.context.memory = MagicMock()
        self.context.registers = {}

    def test_mov_to_register(self):
        Mov.resolve_operand = MagicMock(return_value=42)
        Mov.compute_require_size = MagicMock(return_value=4)

        Mov.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))
        self.assertEqual(self.context.registers["ebx"], 42)
        Mov.resolve_operand.assert_called_with(self.context, "REG", "eax", size=4)
        Mov.compute_require_size.assert_called_with(self.context, "REG", "ebx")

    def test_mov_to_memory(self):
        Mov.resolve_operand = MagicMock(side_effect=[42, 0x1000])
        Mov.compute_require_size = MagicMock(return_value=4)

        Mov.execute(self.context, source=("REG", "eax"), destination=("ADDR", ("IMM", 0x1000)))
        self.context.memory.write.assert_called_with(0x1000, 42, size=4)
        Mov.resolve_operand.assert_any_call(self.context, "REG", "eax", size=4)
        Mov.resolve_operand.assert_any_call(self.context, "IMM", 0x1000)
        Mov.compute_require_size.assert_called_with(self.context, "ADDR", ("IMM", 0x1000))

    def test_mov_unknown_destination_type(self):
        Mov.resolve_operand = MagicMock(return_value=42)
        Mov.compute_require_size = MagicMock(return_value=4)

        with self.assertRaises(ValueError) as context:
            Mov.execute(self.context, source=("REG", "eax"), destination=("UNKNOWN", "ebx"))
        self.assertEqual(str(context.exception), "Unknown destination type: UNKNOWN")
        Mov.resolve_operand.assert_called_with(self.context, "REG", "eax", size=4)
        Mov.compute_require_size.assert_called_with(self.context, "UNKNOWN", "ebx")


if __name__ == '__main__':
    unittest.main()
