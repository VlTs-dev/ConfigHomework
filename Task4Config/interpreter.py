import json
import math

MEMORY = [0] * 1024  # Память виртуальной машины
ACCUMULATOR = 0      # Регистр-аккумулятор

def execute(binary_file, memory_output):
    global ACCUMULATOR, MEMORY

    # Чтение бинарного файла
    with open(binary_file, 'rb') as f:
        binary_data = f.read()

    # Выполнение команд
    for i in range(0, len(binary_data), 5):  # Каждая команда занимает 5 байт
        opcode = binary_data[i]  # 1 байт — код операции
        operand = int.from_bytes(binary_data[i+1:i+5], 'little')  # 4 байта — операнд

        if opcode == 0x16:  # LOAD_CONST
            ACCUMULATOR = operand
        elif opcode == 0x4F:  # UNARY_SQRT
            ACCUMULATOR = int(math.sqrt(ACCUMULATOR))
        elif opcode == 0x8B:  # STORE_MEM
            MEMORY[operand] = ACCUMULATOR
        else:
            raise ValueError(f"Неизвестный opcode: {opcode}")

    # Сохранение памяти в JSON-файл
    memory_dict = {i: val for i, val in enumerate(MEMORY) if val != 0}
    with open(memory_output, 'w') as f:
        json.dump(memory_dict, f, indent=4)

if __name__ == "__main__":
    execute("binary_output.bin", "memory_dump.json")
