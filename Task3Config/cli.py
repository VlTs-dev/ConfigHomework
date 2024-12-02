# cli.py
import sys
import argparse
from config_parser.lexer import Lexer
from config_parser.parser import Parser
from config_parser.translator import Translator


def main():
    parser = argparse.ArgumentParser(description="Convert configuration language to YAML.")
    parser.add_argument("input_file", help="Path to the input file")
    args = parser.parse_args()

    try:
        with open(args.input_file, "r") as file:
            text = file.read()

        lexer = Lexer(text)
        tokens = lexer.get_tokens()

        parser = Parser(tokens)
        parsed_data = parser.parse()

        yaml_output = Translator.to_yaml(parsed_data)
        print(yaml_output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
