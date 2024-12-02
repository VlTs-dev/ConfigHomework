import json

# Определение структуры команды
COMMANDS = {
    "LOAD_CONST": 0x16,
    "LOAD_MEM": 0x52,
    "STORE_MEM": 0x8B,
    "UNARY_SQRT": 0x4F
}


def assemble(input_file, output_bin, log_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    binary_output = bytearray()
    log_output = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):  # Игнорируем пустые строки и комментарии
            continue

        parts = line.split()
        command = parts[0]
        if command not in COMMANDS:
            raise ValueError(f"Неизвестная команда: {command}")

        # Преобразуем в бинарный формат
        opcode = COMMANDS[command]
        operand = int(parts[1]) if len(parts) > 1 else 0

        binary_command = opcode.to_bytes(1, 'little') + operand.to_bytes(4, 'little')
        binary_output.extend(binary_command)

        # Добавляем в лог
        log_output.append({
            "command": command,
            "operand": operand,
            "binary": list(binary_command)
        })

    # Сохраняем бинарный файл
    with open(output_bin, 'wb') as f:
        f.write(binary_output)

    # Сохраняем лог
    with open(log_file, 'w') as f:
        json.dump(log_output, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    assemble("program.txt", "binary_output.bin", "log.json")
