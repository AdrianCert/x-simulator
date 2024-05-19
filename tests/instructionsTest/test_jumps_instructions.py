import unittest
from unittest.mock import MagicMock
from xsim.core import processor
from src.xsim.components.basic.instructions.jumps import Jmp, Jz, Jeq, Jne, Jnz, Jl, Jg, Jge, Jle


class TestJumpInstructions(unittest.TestCase):

    def setUp(self):
        self.context = MagicMock(spec=processor.ProcessorBase)
        self.context.registers = {"PC": 0, "SREG": 0}
        self.context.flags_mask = {"Z": 1, "S": 2}

    def test_jmp_execute(self):
        Jmp.resolve_operand = MagicMock(return_value=100)

        Jmp.execute(self.context, address=("ADDR", 100))

        self.assertEqual(self.context.registers["PC"], 100)

    def test_jz_execute(self):
        self.context.registers["SREG"] = 1  # Setăm flag-ul Z

        Jz.resolve_operand = MagicMock(return_value=200)

        Jz.execute(self.context, address=("ADDR", 200))

        self.assertEqual(self.context.registers["PC"], 200)

    def test_jeq_execute(self):
        self.context.registers["SREG"] = 1  # Setăm flag-ul Z

        Jeq.resolve_operand = MagicMock(return_value=300)

        Jeq.execute(self.context, address=("ADDR", 300))

        self.assertEqual(self.context.registers["PC"], 300)

    def test_jne_execute(self):
        Jne.resolve_operand = MagicMock(return_value=400)

        Jne.execute(self.context, address=("ADDR", 400))

        self.assertEqual(self.context.registers["PC"], 400)

    def test_jnz_execute(self):
        self.context.registers["SREG"] = 0  # Resetează flag-ul Z

        Jnz.resolve_operand = MagicMock(return_value=500)

        Jnz.execute(self.context, address=("ADDR", 500))

        self.assertEqual(self.context.registers["PC"], 500)

    # Se pot adăuga și alte teste pentru celelalte instrucțiuni...

if __name__ == '__main__':
    unittest.main()
