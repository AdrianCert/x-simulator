import typing
from pathlib import Path

from lark import Lark, Transformer, v_args


class AssemblyTransformer(Transformer):
    def __init__(
        self,
        register_names: typing.Optional[typing.List[str]] = None,
        **kwargs,
    ):
        self.register_names = register_names or []

    @v_args(tree=True)
    def numerical(self, operand: str = ""):
        # print(args, kwargs)
        return

    @v_args(inline=True)
    def numerical_dec(self, token):
        return int(token)

    @v_args(inline=True)
    def numerical_hex(self, token):
        return int(token, 16)

    @v_args(inline=True)
    def const(self, const):
        return "CONST", const

    @v_args(inline=True)
    def reg(self, reg):
        if reg not in self.register_names:
            raise ValueError(f"Register {reg} not found in {self.register_names}")
        return "REG", str(reg)

    @v_args(inline=True)
    def addr(self, addr):
        return "ADDR", addr

    @v_args(inline=True)
    def instruction_name(self, name):
        return str(name)

    @v_args(inline=True)
    def term(self, term):
        return term

    @v_args(inline=True)
    def factor(self, factor):
        return factor

    @v_args(inline=True)
    def operand(self, operand):
        return operand

    @v_args(inline=True)
    def instruction(self, instruction_name, *args):
        return {
            "name": instruction_name,
            "params": dict(zip(["destination", "source"], args)),
        }

    @v_args(inline=True)
    def add(self, a, b):
        return "EXPR", (a, "+", b)

    @v_args(inline=True)
    def sub(self, a, b):
        return "EXPR", (a, "-", b)

    @v_args(inline=True)
    def mul(self, a, b):
        return "EXPR", (a, "*", b)

    @v_args(inline=True)
    def div(self, a, b):
        return "EXPR", (a, "/", b)

    @v_args(inline=True)
    def expr(self, expr):
        return expr

    @v_args(inline=True)
    def instructions(self, *instructions):
        return [x for x in instructions if isinstance(x, dict)]

    @v_args(inline=True)
    def start(self, instructions):
        return instructions


class AssemblyParser:
    """
    This class is responsible for parsing make files (a subset of grammar is available)

    The `MakeParser` class provides methods for loading and parsing make files. It uses
    a grammar to define the syntax of the make file and a parser to parse the make
    file contents.

    Example:

        >>> parser = AssemblyParser()
        >>> result = parser.load('Makefile')

    """

    class Grammar:
        r"""
        start: instructions
        instructions: (instruction NEWLINE)* instruction NEWLINE*
        instruction: instruction_name
        | instruction_name operand
        | instruction_name operand "," operand

        instruction_name: INSTRUCTION
        INSTRUCTION: "MOV" | "ADD" | "SUB" | "MUL" | "DIV" | "JMP" | "JZ" | "JNZ" | "JG" | "JL" | "JGE" | "JLE" | "CALL" | "RET" | "NOP"
        operand: addr | const | reg

        expr: term
            | expr "+" term   -> add
            | expr "-" term   -> sub

        term: factor
            | term "*" factor -> mul
            | term "/" factor -> div

        factor: const
            | "(" expr ")"
            | reg

        const: numerical_hex | numerical_dec
        numerical_hex: /0[Xx][0-9a-fA-F]+/
        numerical_dec: /[1-9][0-9]*/
        reg: /[a-z]+[0-9]*/
        addr: "[" (const | reg | expr) "]"

        %import common.LETTER
        %import common.UCASE_LETTER
        %import common.LCASE_LETTER
        %import common.DIGIT
        %import common.WS_INLINE
        %import common.NUMBER
        %import common.HEXDIGIT
        %import common.NEWLINE

        %ignore WS_INLINE
        """

        _parser: Lark = None
        _vars: typing.Dict[str, str] = {}
        _conf_transform: typing.Dict[str, typing.Any] = {}
        _tree: typing.Any = None

        @classmethod
        def source(cls):
            return cls.__doc__

        @classmethod
        def parser(cls, **kwargs):
            if cls._parser is None:
                cls._parser = Lark(
                    cls.source(),
                    parser="cyk",
                    transformer=AssemblyTransformer(**kwargs),
                )
            return cls._parser

        @classmethod
        def parse(cls, text: str, **kwargs):
            return cls.parser(**kwargs).parse(text)

        @classmethod
        def last_tree(cls):
            return cls._tree

    @classmethod
    def loads(cls, text, **kwargs):
        return cls.Grammar.parse(text=text, **kwargs)

    @classmethod
    def load(cls, fp: typing.Union[str, Path, typing.TextIO], **kwargs):
        if isinstance(fp, str):
            fp = Path(fp)
        if isinstance(fp, Path):
            fp = fp.open("r")
        return cls.loads(fp.read(), **kwargs)


test_prg = """MOV 0x10
NOP
MOV [100]
DIV [r1], 0xFF
JMP [r2]
MOV [r2 + 0x10],0x11
"""

if __name__ == "__main__":
    parser = AssemblyParser.loads(test_prg, register_names=["r1", "r2"])
    print(*parser, sep="\n")
