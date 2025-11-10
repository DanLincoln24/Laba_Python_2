import shutil
from pathlib import Path
from log import log_command
from undo import undo_stackking


def cp_command(args: list, current_path: Path):
    """Команда cp - копирование файлов/директорий"""
    if len(args) < 2:
        print("cp: требуется как минимум 2 аргумента")
        return

    recursive = False
    sources = []
    destination = None

    # Парсинг аргументов
    for arg in args:
        if arg == "-r":
            recursive = True
        else:
            if destination is None and len(sources) > 0 and arg == args[-1]:
                destination = arg
            else:
                sources.append(arg)

    if not sources or destination is None:
        print("cp: требуется источник и назначение")
        return

    dest_path = (current_path / destination).resolve()

    for source in sources:
        src_path = (current_path / source).resolve()

        if not src_path.exists():
            print(f"cp: {src_path}: Нет такого файла или директории")
            continue

        try:
            if src_path.is_dir() and not recursive:
                print(f"cp: {src_path}: Это директория (используйте -r)")
                continue

            if src_path.is_dir():
                shutil.copytree(src_path, dest_path / src_path.name if dest_path.is_dir() else dest_path)
            else:
                if dest_path.is_dir():
                    shutil.copy2(src_path, dest_path / src_path.name)
                else:
                    shutil.copy2(src_path, dest_path)

            # Регистрируем для отмены
            if dest_path.is_dir():
                final_dest = dest_path / src_path.name
            else:
                final_dest = dest_path
            undo_stackking('cp', final_dest)

        except Exception as e:
            print(f"cp: {e}")
            log_command(f"cp {' '.join(args)}", False, str(e))

    log_command(f"cp {' '.join(args)}")