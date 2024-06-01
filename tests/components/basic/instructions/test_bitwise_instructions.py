import unittest
from unittest.mock import MagicMock

from xsim.core import processor

from src.xsim.components.basic.instructions.bitwise import (
    And,
    Not,
    Or,
    Shl,
    Shr,
    Xor,
)


class TestBitwiseInstructionSet(unittest.TestCase):
    def setUp(self):
        self.context = MagicMock(spec=processor.ProcessorBase)
        self.context.memory = MagicMock()
        self.context.registers = {}

    def test_and_execute(self):
        And.resolve_operand = MagicMock(return_value=5)
        And.compute_result = MagicMock(return_value=4)

        And.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))

        self.assertEqual(self.context.registers["ebx"], 4)

    def test_or_execute(self):
        Or.resolve_operand = MagicMock(return_value=3)
        Or.compute_result = MagicMock(return_value=6)

        Or.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))

        self.assertEqual(self.context.registers["ebx"], 6)

    def test_xor_execute(self):
        Xor.resolve_operand = MagicMock(return_value=2)
        Xor.compute_result = MagicMock(return_value=3)

        Xor.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))

        self.assertEqual(self.context.registers["ebx"], 3)

    def test_not_execute(self):
        Not.resolve_operand = MagicMock(return_value=7)
        Not.compute_result = MagicMock(return_value=-8)

        Not.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))

        self.assertEqual(self.context.registers["ebx"], -8)

    def test_shl_execute(self):
        Shl.resolve_operand = MagicMock(return_value=4)
        Shl.compute_result = MagicMock(return_value=16)

        Shl.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))

        self.assertEqual(self.context.registers["ebx"], 16)

    def test_shr_execute(self):
        Shr.resolve_operand = MagicMock(return_value=8)
        Shr.compute_result = MagicMock(return_value=2)

        Shr.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))

        self.assertEqual(self.context.registers["ebx"], 2)


if __name__ == "__main__":
    unittest.main()
