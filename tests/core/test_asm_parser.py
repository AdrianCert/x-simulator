import unittest

import coverage

from src.xsim.core.asm_parser import AssemblyTransformer


class TestAssemblyTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = AssemblyTransformer(register_names=["r1", "r2"])

    def test_numerical_hex(self):
        result = self.transformer.numerical_hex("0xAB")
        self.assertEqual(result, 171)

    def test_numerical_dec(self):
        result = self.transformer.numerical_dec("123")
        self.assertEqual(result, 123)

    def test_const(self):
        result = self.transformer.const(42)
        self.assertEqual(result, ("CONST", 42))

    def test_reg(self):
        result = self.transformer.reg("r1")
        self.assertEqual(result, ("REG", "r1"))

    def test_add(self):
        result = self.transformer.add(2, 3)
        expected = ("EXPR", (2, "+", 3))
        self.assertEqual(result, expected)

    # def test_addr(self):
    #     result = self.transformer.addr("r1")
    #     expected = ("ADDR", ("REG", "r1"))
    #     self.assertEqual(result, expected)

    def test_div(self):
        result = self.transformer.div(6, 3)
        expected = ("EXPR", (6, "/", 3))
        self.assertEqual(result, expected)

    def test_instruction_name(self):
        result = self.transformer.instruction_name("NOP")
        self.assertEqual(result, "NOP")

    def test_instruction(self):
        result = self.transformer.instruction("MOV", ("REG", "r1"), ("REG", "r2"))
        expected = {
            "name": "MOV",
            "params": {"destination": ("REG", "r1"), "source": ("REG", "r2")},
        }
        self.assertEqual(result, expected)

    def test_mul(self):
        result = self.transformer.mul(2, 3)
        expected = ("EXPR", (2, "*", 3))
        self.assertEqual(result, expected)

    def test_sub(self):
        result = self.transformer.sub(3, 1)
        expected = ("EXPR", (3, "-", 1))
        self.assertEqual(result, expected)

    def test_expr(self):
        result = self.transformer.expr(("REG", "r1"))
        self.assertEqual(result, ("REG", "r1"))

    def test_instructions(self):
        result = self.transformer.instructions(
            {"name": "NOP", "params": {}},
            {
                "name": "MOV",
                "params": {"destination": ("REG", "r1"), "source": ("REG", "r2")},
            },
        )
        expected = [
            {"name": "NOP", "params": {}},
            {
                "name": "MOV",
                "params": {"destination": ("REG", "r1"), "source": ("REG", "r2")},
            },
        ]
        self.assertEqual(result, expected)

    def test_start(self):
        result = self.transformer.start(
            [
                {"name": "NOP", "params": {}},
                {
                    "name": "MOV",
                    "params": {"destination": ("REG", "r1"), "source": ("REG", "r2")},
                },
            ]
        )
        expected = [
            {"name": "NOP", "params": {}},
            {
                "name": "MOV",
                "params": {"destination": ("REG", "r1"), "source": ("REG", "r2")},
            },
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
    cov = coverage.Coverage()
