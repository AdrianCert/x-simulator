import unittest
from unittest.mock import MagicMock

from xsim.core import processor

from src.xsim.components.basic.instructions.base import BaseInstruction, Halt, Nop


class TestBaseInstruction(unittest.TestCase):
    def setUp(self):
        self.context = MagicMock(spec=processor.ProcessorBase)
        self.context.memory = MagicMock()
        self.context.registers = {}

    def test_compute_require_size_addr(self):
        size = BaseInstruction.compute_require_size(
            self.context, "ADDR", ("REG", "eax")
        )
        self.assertEqual(size, 2)

    def test_compute_require_size_reg(self):
        self.context.registers = {"eax": 4, "ebx": 2}
        size = BaseInstruction.compute_require_size(self.context, "REG", "eax")
        self.assertEqual(size, 4)

    def test_compute_require_size_default(self):
        size = BaseInstruction.compute_require_size(self.context, "UNKNOWN", "value")
        self.assertEqual(size, 1)

    def test_resolve_operand_const(self):
        operand_value = BaseInstruction.resolve_operand(
            self.context, "CONST", 123, size=1
        )
        self.assertEqual(operand_value, 123)

    def test_resolve_operand_reg(self):
        self.context.registers = {"eax": 10}
        operand_value = BaseInstruction.resolve_operand(
            self.context, "REG", "eax", size=1
        )
        self.assertEqual(operand_value, 10)

    def test_resolve_operand_default(self):
        with self.assertRaises(ValueError) as context:
            BaseInstruction.resolve_operand(self.context, "UNKNOWN", "value", size=1)
        self.assertEqual(str(context.exception), "Unknown operand type: UNKNOWN")


class TestNopInstruction(unittest.TestCase):
    def test_nop_execute(self):
        context = MagicMock(spec=processor.ProcessorBase)
        Nop.execute(context)
        context.assert_not_called()


class TestHaltInstruction(unittest.TestCase):
    def test_halt_execute(self):
        context = MagicMock(spec=processor.ProcessorBase)
        Halt.execute(context)
        self.assertTrue(context.halt)


if __name__ == "__main__":
    unittest.main()
