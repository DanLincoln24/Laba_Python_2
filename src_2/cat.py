from pathlib import Path
from log import log_command


def cat_command(args: list, current_path: Path):
    if not args:
        print("cat: требуется аргумент - имя файла")
        return

    file_path = (current_path / args[0]).resolve()

    if not file_path.exists():
        print(f"cat: {file_path}: Нет такого файла")
        log_command(f"cat {' '.join(args)}", False, "File not found")
        return

    if file_path.is_dir():
        print(f"cat: {file_path}: Это директория")
        log_command(f"cat {' '.join(args)}", False, "Is a directory")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        log_command(f"cat {' '.join(args)}")
    except UnicodeDecodeError:
        print(f"cat: {file_path}: Невозможно прочитать файл")
        log_command(f"cat {' '.join(args)}", False, "Cannot read binary file")
    except Exception as e:
        print(f"cat: {e}")
        log_command(f"cat {' '.join(args)}", False, str(e))