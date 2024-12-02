import sys
import assembler
import interpreter
import json

# Устанавливаем UTF-8 для вывода, чтобы избежать проблем с кодировкой
sys.stdout.reconfigure(encoding='utf-8')

def test_uvm():
    assembler.assemble("program.txt", "binary_output.bin", "log.json")
    interpreter.execute("binary_output.bin", "memory_dump.json")

    with open("memory_dump.json", "r") as f:
        memory = json.load(f)  # Загружаем JSON-файл как словарь

    # Проверяем, что по адресу 100 записано значение 12
    assert int(memory["100"]) == 12, "Ошибка: результат вычисления некорректен!"


if __name__ == "__main__":
    test_uvm()
    print("Все тесты пройдены!")  # Здесь используется русский текст
