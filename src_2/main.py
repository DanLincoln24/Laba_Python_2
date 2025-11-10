
import sys
import os
from pathlib import Path

# импорт всех модулей
from log import dict_logging, log_command
from history import add_to_history, show_history
from undo import undo_last_command
from ls import ls_command
from cd import cd_command
from cat import cat_command
from cp import cp_command
from mv import mv_command
from rm import rm_command
from zip import zip_command, unzip_command
from tar import tar_command, untar_command
from grep import grep_command


def display_prompt(current_path: Path) -> str:
    try:
        home = Path.home()
        if current_path == home:
            display_path = "~"
        elif home in current_path.parents:
            display_path = "~/" + str(current_path.relative_to(home))
        else:
            display_path = str(current_path)
    except:
        display_path = str(current_path)

    return f"\033[94m{display_path}\033[0m$ "


def main():
    dict_logging()
    current_path = Path.cwd()

    print("Добро пожаловать в Python Shell!")
    print("Для выхода введите 'exit' или 'quit'")

    while True:
        try:
            command = input(display_prompt(current_path)).strip()

            if not command:
                continue

            if command.lower() in ['exit', 'quit']:
                print("Выход из оболочки.")
                break

            # Логируем команду
            log_command(command)
            add_to_history(command)

            # Разбиваем команду на части
            parts = command.split()
            cmd = parts[0]
            args = parts[1:]

            # Обрабатываем команды
            if cmd == "history":
                show_history()
            elif cmd == "undo":
                undo_last_command(current_path)
            elif cmd == "zip":
                zip_command(args, current_path)
            elif cmd == "unzip":
                unzip_command(args, current_path)
            elif cmd == "tar":
                tar_command(args, current_path)
            elif cmd == "untar":
                untar_command(args, current_path)
            elif cmd == "grep":
                grep_command(args, current_path)
            elif cmd == "ls":
                ls_command(args, current_path)
            elif cmd == "cd":
                current_path = cd_command(args, current_path)
            elif cmd == "cat":
                cat_command(args, current_path)
            elif cmd == "cp":
                cp_command(args, current_path)
            elif cmd == "mv":
                mv_command(args, current_path)
            elif cmd == "rm":
                rm_command(args, current_path)
            else:
                print(f"Команда '{cmd}' не найдена")
                log_command(f"{cmd} {' '.join(args)}", False, "Command not found")

        except KeyboardInterrupt:
            print("\nДля выхода введите 'exit' или 'quit'")
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()