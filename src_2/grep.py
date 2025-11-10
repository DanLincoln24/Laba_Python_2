import re
from pathlib import Path
from log import log_command
from undo import undo_stackking


def grep_command(args: list, current_path: Path):
    if len(args) < 2:
        print("grep: требуется 2 аргумента: шаблон и путь")
        return

    pattern = args[0]
    search_path = (current_path / args[1]).resolve()
    recursive = False
    ignore_case = False

    # Обработка опций
    other_args = []
    for arg in args[2:]:
        if arg == "-r":
            recursive = True
        elif arg == "-i":
            ignore_case = True
        else:
            other_args.append(arg)

    if not search_path.exists():
        print(f"grep: {search_path}: Нет такого файла или директории")
        return

    try:
        flags = re.IGNORECASE if ignore_case else 0
        regex = re.compile(pattern, flags)

        if search_path.is_file():
            search_in_file(search_path, regex)
        elif search_path.is_dir():
            if recursive:
                for file_path in search_path.rglob('*'):
                    if file_path.is_file():
                        search_in_file(file_path, regex)
            else:
                for file_path in search_path.iterdir():
                    if file_path.is_file():
                        search_in_file(file_path, regex)

        log_command(f"grep {' '.join(args)}")
    except Exception as e:
        print(f"grep: {e}")
        log_command(f"grep {' '.join(args)}", False, str(e))


def search_in_file(file_path: Path, regex: re.Pattern): #Поиск заданного шаблона в файле
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if regex.search(line):
                    print(f"{file_path}:{line_num}: {line.strip()}")
    except Exception:
        pass  # Игнорируем файлы которые не можем прочитать