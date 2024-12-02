# config_parser/lexer.py
import re

class Lexer:
    TOKENS = [
        ("COMMENT", r"NB\..*"),
        ("ASSIGN", r"="),
        ("AT_CONST", r"@\[[a-zA-Z][_a-zA-Z0-9]*\]"),
        ("COLON", r":"),
        ("SEMICOLON", r";"),
        ("LBRACE", r"\{"),
        ("RBRACE", r"\}"),
        ("LPAREN", r"list\("),
        ("RPAREN", r"\)"),
        ("STRING", r'"[^"]*"'),  # Добавлено: строковые значения в кавычках
        ("NUMBER", r"\d+"),
        ("IDENTIFIER", r"[a-zA-Z][_a-zA-Z0-9]*"),
        ("COMMA", r","),
        ("WHITESPACE", r"[ \t\n]+"),
    ]

    def __init__(self, text):
        self.text = text
        self.tokens = []
        self._tokenize()

    def _tokenize(self):
        index = 0
        while index < len(self.text):
            for token_type, pattern in self.TOKENS:
                regex = re.compile(pattern)
                match = regex.match(self.text, index)
                if match:
                    if token_type != "WHITESPACE":
                        self.tokens.append((token_type, match.group()))
                    index = match.end()
                    break
            else:
                raise SyntaxError(f"Invalid character at index {index}: {self.text[index]}")

    def get_tokens(self):
        return self.tokens
