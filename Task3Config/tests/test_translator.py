import yaml
from config_parser.translator import Translator


def test_translator_to_yaml():
    # Пример данных для трансляции
    parsed_data = {
        "name": "Alice",
        "age": 30,
        "roles": ["admin", "editor"],
        "settings": {
            "theme": "dark",
            "notifications": True
        }
    }

    yaml_result = Translator.to_yaml(parsed_data)

    expected_output = """\
age: 30
name: Alice
roles:
- admin
- editor
settings:
  notifications: true
  theme: dark
"""
    # Сравниваем Python-объекты, а не строки
    yaml_result_parsed = yaml.safe_load(yaml_result)
    expected_output_parsed = yaml.safe_load(expected_output)

    assert yaml_result_parsed == expected_output_parsed, "YAML output does not match expected result"
