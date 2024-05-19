import unittest
from unittest.mock import MagicMock
from src.xsim.components.basic.processor import BasicProcessor


class TestBasicProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = BasicProcessor(
            2048 * 2,
            {
                "memory_mapped": [0, 16],
                "registers": [
                    ("r0", 2), ("r1", 2), ("r2", 2), ("r3", 2), ("r4", 2),
                    ("r5", 2), ("r6", 2), ("r7", 2), ("pc", 2), ("ir", 2),
                    ("mar", 2), ("mdr", 2), ("sp", 2), ("sr", 2), ("lr", 2),
                    ("sreg", 1),
                ],
            },
            flags_names=["I", "T", "H", "S", "V", "P", "Z", "C"]
        )
        self.mock_instruction = MagicMock()

    def test_update_program(self):
        # Verificăm dacă programul este actualizat corect
        program_data = [{"name": "mock_instruction", "params": {}}]
        self.processor.update_program(program_data)
        self.assertEqual(self.processor.program_data, program_data)

    def test_execute_instruction(self):
        # Verificăm dacă instrucția este executată corect
        instruction_data = {"name": "mock_instruction", "params": {}}
        self.processor.instruction_set.get_instruction = MagicMock(return_value=self.mock_instruction)

        self.processor.execute_instruction(instruction_data)

        self.mock_instruction.execute.assert_called_once_with(self.processor, **instruction_data["params"])

    def test_execute(self):
        # Verificăm dacă procesorul rulează corect
        program_data = [{"name": "mock_instruction", "params": {}}]
        self.processor.update_program(program_data)
        self.processor.execute_instruction = MagicMock()

        list(self.processor.execute())

        self.processor.execute_instruction.assert_called_once_with(program_data[0])


if __name__ == '__main__':
    unittest.main()
