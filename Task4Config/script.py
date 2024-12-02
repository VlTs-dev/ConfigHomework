def read_binary_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    print("Содержимое файла в шестнадцатеричном формате:")
    for i in range(0, len(data), 5):  # Команды по 5 байт
        print(data[i:i+5].hex().upper())

if __name__ == "__main__":
    read_binary_file("binary_output.bin")
