import argparse
import sys
from application import VirtualFileSystem
from terminal import uniq, head, wc
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ShellGUI:
    def __init__(self, root, vfs, hostname):
        self.vfs = vfs
        self.hostname = hostname
        self.root = root
        self.root.title("Linux Terminal Emulator")
        self.command_history = []
        self.history_index = -1

        # Terminal style
        self.output_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, bg="black", fg="white",
            font=("Courier", 12), insertbackground="white",
            width=80, height=24, state=tk.NORMAL
        )
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.output_area.insert(tk.END, f"{self.hostname}:{self.vfs.current_path}$ ")
        self.output_area.bind("<Return>", self.execute_command)
        self.output_area.bind("<BackSpace>", self.handle_backspace)
        self.output_area.bind("<Key>", self.handle_key)
        self.output_area.focus()

    def execute_command(self, event=None):
        # Получение текущей команды
        current_line = self.output_area.get("end-2l", "end-1c")
        command = current_line.split("$ ", 1)[-1].strip()
        self.command_history.append(command)
        self.history_index = len(self.command_history)
    
        # Удаляем текущий курсор
        self.output_area.delete("end-2c", "end-1c")
        self.output_area.insert(tk.END, "\n")

        try:
            if command == "exit":
                self.vfs._log_action("exit")  # Логируем выход
                self.root.destroy()  # Завершаем GUI
                sys.exit(0)  # Полное завершение программы
            elif command == "ls":
                contents = self.vfs.list_directory()
                self.display_output("\n".join(contents))
            elif command.startswith("cd "):
                path = command[3:].strip()
                self.vfs.change_directory(path)
            elif command.startswith("head "):
                filename = command[5:].strip()
                lines = self.vfs.read_file(filename)
                self.display_output("".join(head(lines)))
            elif command.startswith("uniq "):
                filename = command[5:].strip()
                lines = self.vfs.read_file(filename)
                self.display_output("".join(uniq(lines)))
            elif command.startswith("wc "):
                filename = command[3:].strip()
                lines = self.vfs.read_file(filename)
                counts = wc(lines)
                self.display_output(f"Lines: {counts['lines']}, Words: {counts['words']}, Characters: {counts['characters']}")
            elif command == "clear":
                self.output_area.delete("1.0", tk.END)
            else:
                self.display_output(f"{command}: command not found")
        except FileNotFoundError as e:
            self.display_output(f"Error: {e}")
        except Exception as e:
            self.display_output(f"Unexpected error: {e}")

        # Добавляем новое приглашение
        self.output_area.insert(tk.END, f"{self.hostname}:{self.vfs.current_path}$ ")
        self.output_area.see(tk.END)



    def handle_backspace(self, event):
        # Удаляем символ, если это возможно
        cursor_index = self.output_area.index(tk.INSERT)
        line_content = self.output_area.get("end-2l", "end-1c")
        if len(line_content.split("$ ", 1)[-1]) > 0:
            self.output_area.delete(cursor_index + "-1c", cursor_index)
        return "break"

    def handle_key(self, event):
        # Обработка клавиш для эмуляции поведения терминала
        if event.keysym == "Up":
            if self.history_index > 0:
                self.history_index -= 1
                command = self.command_history[self.history_index]
                self.replace_current_line(command)
        elif event.keysym == "Down":
            if self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                command = self.command_history[self.history_index]
                self.replace_current_line(command)
            else:
                self.replace_current_line("")
        return

    def replace_current_line(self, text):
        # Заменяем текущую команду на новую из истории
        self.output_area.delete("end-2l", "end-1c")
        self.output_area.insert("end-1c", f"{self.hostname}:{self.vfs.current_path}$ {text}")

    def display_output(self, message):
        # Показ вывода команды
        self.output_area.insert(tk.END, message + "\n")
        self.output_area.see(tk.END)


def main():
    parser = argparse.ArgumentParser(description="Linux Terminal Emulator")
    parser.add_argument("--hostname", required=True, help="Set hostname for shell prompt")
    parser.add_argument("--fs", required=True, help="Path to tar archive of virtual filesystem")
    parser.add_argument("--log", required=True, help="Path to log file")
    args = parser.parse_args()

    try:
        vfs = VirtualFileSystem(args.fs, args.log)
        root = tk.Tk()
        app = ShellGUI(root, vfs, args.hostname)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


