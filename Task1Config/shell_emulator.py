import argparse
import os
import tarfile
import tkinter as tk
from tkinter import scrolledtext
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime

class ShellEmulator:
    def __init__(self, username, hostname, tar_path, log_path, script_path):
        self.username = username
        self.hostname = hostname
        self.log_path = log_path
        self.script_path = script_path
        self.cwd = "/"
        self.fs = {}
        self.load_filesystem(tar_path)
        self.log_root = Element("session")
        self.init_gui()

    def load_filesystem(self, tar_path):
        with tarfile.open(tar_path, "r:") as tar:
            for member in tar.getmembers():
                # Нормализуем путь, убирая "./" в начале
                normalized_path = member.name if not member.name.startswith("./") else member.name[2:]

                if member.isfile():
                    extracted_file = tar.extractfile(member)
                    if extracted_file is not None:
                        try:
                            self.fs[normalized_path] = extracted_file.read().decode('utf-8')
                        except UnicodeDecodeError:
                            self.fs[normalized_path] = extracted_file.read()
                else:
                    self.fs[normalized_path] = None
        # Отладочный вывод для проверки содержимого файловой системы
        print("Содержимое файловой системы (нормализованное):", self.fs)

    def init_gui(self):
        self.root = tk.Tk()
        self.root.title("Shell Emulator")
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind("<Return>", self.on_enter)
        self.prompt()

    def log(self, command):
        action = SubElement(self.log_root, "action")
        SubElement(action, "user").text = self.username
        SubElement(action, "timestamp").text = datetime.now().isoformat()
        SubElement(action, "command").text = command

    def save_log(self):
        with open(self.log_path, "wb") as f:
            f.write(tostring(self.log_root))

    def prompt(self):
        self.text_area.insert(tk.END, f"{self.username}@{self.hostname}:{self.cwd}$ ")

    def execute_command(self, command):
        parts = command.strip().split()
        if not parts:
            return
        cmd, *args = parts
        self.text_area.insert(tk.END, "\n")
        if cmd == "ls":
            self.ls()
        elif cmd == "cd":
            self.cd(args)
        elif cmd == "exit":
            self.save_log()
            self.root.destroy()
        elif cmd == "find":
            self.find(args)
        elif cmd == "rmdir":
            self.rmdir(args)

        else:
            self.text_area.insert(tk.END, "Unknown command\n")
        self.prompt()

    def ls(self):
        files = [f for f in self.fs if f.startswith(self.cwd) and f != self.cwd]
        self.text_area.insert(tk.END, "\n".join(files) + "\n")

    def cd(self, args):
        if len(args) != 1:
            self.text_area.insert(tk.END, "Usage: cd <directory>\n")
            return
        path = args[0]
        if path in self.fs and self.fs[path] is None:
            self.cwd = path
        else:
            self.text_area.insert(tk.END, "Directory not found\n")

    def find(self, args):
        query = args[0] if args else ""
        results = [f for f in self.fs if query in f]
        self.text_area.insert(tk.END, "\n".join(results) + "\n")

    def rmdir(self, args):
        path = args[0] if args else ""
        if path in self.fs:
            del self.fs[path]
            self.text_area.insert(tk.END, f"Removed {path}\n")
        else:
            self.text_area.insert(tk.END, "Directory not found\n")

    def on_enter(self, event):
        command = self.text_area.get("end-2l", "end-1c").split("$ ")[-1]
        self.log(command)
        self.execute_command(command.strip())
        return "break"

    def run_script(self):
        if os.path.exists(self.script_path):
            with open(self.script_path, "r") as f:
                for line in f:
                    self.log(line.strip())
                    self.execute_command(line.strip())

    def run(self):
        self.run_script()
        self.root.mainloop()




def main():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--username", required=True, help="Username for the prompt")
    parser.add_argument("--hostname", required=True, help="Hostname for the prompt")
    parser.add_argument("--tar_path", required=True, help="Path to tar file containing virtual filesystem")
    parser.add_argument("--log_path", required=True, help="Path to XML log file")
    parser.add_argument("--script_path", required=True, help="Path to startup script")
    args = parser.parse_args()
    emulator = ShellEmulator(args.username, args.hostname, args.tar_path, args.log_path, args.script_path)
    emulator.run()


if __name__ == "__main__":
    main()
