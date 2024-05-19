import unittest
from unittest.mock import MagicMock
from xsim.core import processor
from src.xsim.components.basic.instructions.stack import Push, Pop


class TestPushAndPopInstructions(unittest.TestCase):

    def setUp(self):
        self.context = MagicMock(spec=processor.ProcessorBase)
        self.context.registers = {"SP": 100}
        self.context.memory = MagicMock()

    def test_push_execute(self):
        Push.resolve_operand = MagicMock(return_value=42)

        Push.execute(self.context, source=("CONST", 42))

        self.assertEqual(self.context.registers["SP"], 98)  # Verificăm dacă SP-ul a fost actualizat corect
        self.context.memory.write.assert_called_with(98, 42, 2)  # Verificăm dacă valoarea a fost scrisă corect pe stivă

    def test_pop_execute(self):
        self.context.registers["SP"] = 98  # Simulăm o stivă cu o valoare la adresa 98

        self.context.memory.read.return_value = 42  # Valoarea citită de pe stivă

        Pop.execute(self.context, destination=("REG", "eax"))

        self.assertEqual(self.context.registers["eax"], 42)  # Verificăm dacă valoarea a fost încărcată corect în registrul "eax"
        self.assertEqual(self.context.registers["SP"], 100)  # Verificăm dacă SP-ul a fost actualizat corect


if __name__ == '__main__':
    unittest.main()
