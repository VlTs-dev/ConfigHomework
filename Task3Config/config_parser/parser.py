# config_parser/parser.py
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def _current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _consume(self, token_type):
        token = self._current_token()
        if token and token[0] == token_type:
            self.position += 1
            return token
        raise SyntaxError(
            f"Syntax Error: Expected {token_type}, but got {token[1]} (type: {token[0]}) at position {self.position}")

    def parse(self):
        result = {}
        while self._current_token():
            identifier = self._consume("IDENTIFIER")
            self._consume("COLON")
            value = self._parse_value()
            self._consume("SEMICOLON")
            result[identifier[1]] = value
        return result

    def _parse_value(self):
        token = self._current_token()
        if token[0] == "NUMBER":
            return int(self._consume("NUMBER")[1])
        elif token[0] == "STRING":
            return self._consume("STRING")[1].strip('"')  # Убираем кавычки из строки
        elif token[0] == "LBRACE":
            return self._parse_dict()
        elif token[0] == "LPAREN":
            return self._parse_list()
        elif token[0] == "AT_CONST":
            return {"const_ref": token[1][2:-1]}
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def _parse_dict(self):
        self._consume("LBRACE")
        result = {}
        while self._current_token() and self._current_token()[0] != "RBRACE":
            key = self._consume("IDENTIFIER")
            self._consume("COLON")
            value = self._parse_value()
            self._consume("SEMICOLON")
            result[key[1]] = value
        self._consume("RBRACE")
        return result

    def _parse_list(self):
        self._consume("LPAREN")
        result = []
        while self._current_token() and self._current_token()[0] != "RPAREN":
            result.append(self._parse_value())
            if self._current_token() and self._current_token()[0] == "COMMA":
                self._consume("COMMA")
        self._consume("RPAREN")
        return result
