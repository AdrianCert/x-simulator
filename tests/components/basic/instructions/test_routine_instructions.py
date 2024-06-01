import unittest
from unittest.mock import MagicMock

from xsim.core import processor

from src.xsim.components.basic.instructions.routine import Call, Ret


class TestCallAndRetInstructions(unittest.TestCase):
    def setUp(self):
        self.context = MagicMock(spec=processor.ProcessorBase)
        self.context.registers = {"PC": 0, "SP": 100}
        self.context.memory = MagicMock()

    def test_call_execute(self):
        Call.resolve_operand = MagicMock(return_value=200)

        Call.execute(self.context, destination=("ADDR", 200))

        self.assertEqual(
            self.context.registers["SP"], 98
        )  # Verificăm dacă SP-ul a fost actualizat corect
        self.context.memory.write.assert_called_with(
            98, 0, 2
        )  # Verificăm dacă adresa de retur a fost scrisă în memorie
        self.assertEqual(
            self.context.registers["PC"], 200
        )  # Verificăm dacă PC-ul a fost setat la adresa de apel

    def test_ret_execute(self):
        self.context.memory.read.return_value = (
            300  # Adresa de retur citită din memorie
        )

        Ret.execute(self.context)

        self.assertEqual(
            self.context.registers["PC"], 300
        )  # Verificăm dacă PC-ul a fost setat la adresa de retur
        self.assertEqual(
            self.context.registers["SP"], 102
        )  # Verificăm dacă SP-ul a fost actualizat corect


if __name__ == "__main__":
    unittest.main()
