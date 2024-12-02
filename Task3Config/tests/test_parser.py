# tests/test_parser.py
from config_parser.lexer import Lexer
from config_parser.parser import Parser


def test_parser():
    text = "name: 123; config: list(1, 2, 3);"
    lexer = Lexer(text)
    tokens = lexer.get_tokens()

    parser = Parser(tokens)
    result = parser.parse()

    assert result == {
        "name": 123,
        "config": [1, 2, 3],
    }
