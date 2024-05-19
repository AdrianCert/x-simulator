import unittest
from unittest.mock import MagicMock, create_autospec
from xsim.core import const, processor
from src.xsim.components.basic.instructions.arithmetic import Add, Sub, Cmp, ArithmeticInstructionSet


class TestArithmeticInstructionSet(unittest.TestCase):

    def setUp(self):
        self.context = create_autospec(processor.ProcessorBase)
        self.context.memory = MagicMock()
        self.context.registers = MagicMock()
        self.sreg_mock = MagicMock()
        self.context.registers.take.return_value = self.sreg_mock
        self.context.flags_mask = {
            "S": 0x80,
            "Z": 0x40,
            "P": 0x20,
            "C": 0x10,
        }
        self.sreg_mock.get.return_value = 0

    # Teste pentru clasa Add
    def test_add_registers(self):
        Add.resolve_operand = MagicMock(side_effect=[3, 2])
        Add.compute_require_size = MagicMock(return_value=2)

        self.context.registers.__getitem__.side_effect = lambda key: 2 if key == "ebx" else None
        self.context.registers.__setitem__.side_effect = lambda key, value: self.context.registers.__dict__.update({key: value})

        Add.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))
        self.assertEqual(self.context.registers.__dict__["ebx"], 5)
        Add.resolve_operand.assert_any_call(self.context, "REG", "eax", size=2)
        Add.resolve_operand.assert_any_call(self.context, "REG", "ebx", size=2)

    def test_add_flags(self):
        Add.resolve_operand = MagicMock(side_effect=[3, 2])
        Add.compute_require_size = MagicMock(return_value=2)

        Add.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))
        self.sreg_mock.set.assert_called_once()

    # Teste pentru clasa Sub
    def test_sub_registers(self):
        Sub.resolve_operand = MagicMock(side_effect=[2, 5])
        Sub.compute_require_size = MagicMock(return_value=2)

        self.context.registers.__getitem__.side_effect = lambda key: 5 if key == "ebx" else None
        self.context.registers.__setitem__.side_effect = lambda key, value: self.context.registers.__dict__.update({key: value})

        Sub.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))
        self.assertEqual(self.context.registers.__dict__["ebx"], 3)
        Sub.resolve_operand.assert_any_call(self.context, "REG", "eax", size=2)
        Sub.resolve_operand.assert_any_call(self.context, "REG", "ebx", size=2)

    def test_sub_flags(self):
        Sub.resolve_operand = MagicMock(side_effect=[2, 5])
        Sub.compute_require_size = MagicMock(return_value=2)

        Sub.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))
        self.sreg_mock.set.assert_called_once()

    # Teste pentru clasa Cmp
    def test_cmp_registers(self):
        Cmp.resolve_operand = MagicMock(side_effect=[3, 5])
        Cmp.compute_require_size = MagicMock(return_value=2)

        Cmp.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))
        self.context.registers.__setitem__.assert_not_called()
        Cmp.resolve_operand.assert_any_call(self.context, "REG", "eax", size=2)
        Cmp.resolve_operand.assert_any_call(self.context, "REG", "ebx", size=2)

    def test_cmp_flags(self):
        Cmp.resolve_operand = MagicMock(side_effect=[3, 5])
        Cmp.compute_require_size = MagicMock(return_value=2)

        Cmp.execute(self.context, source=("REG", "eax"), destination=("REG", "ebx"))
        self.sreg_mock.set.assert_called_once()

    # Test negativ
    def test_arithmetic_invalid_destination_type(self):
        Add.resolve_operand = MagicMock(return_value=3)
        Add.compute_require_size = MagicMock(return_value=2)

        try:
            Add.execute(self.context, source=("REG", "eax"), destination=("UNKNOWN", "ebx"))
        except ValueError as e:
            self.assertEqual(str(e), "Unknown destination type: UNKNOWN")


if __name__ == '__main__':
    unittest.main()
