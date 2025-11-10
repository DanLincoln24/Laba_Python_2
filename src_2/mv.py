import shutil
from pathlib import Path
from log import log_command
from undo import undo_stackking


def mv_command(args: list, current_path: Path):
    if len(args) < 2:
        print("mv: требуется как минимум 2 аргумента")
        return

    sources = args[:-1]
    destination = args[-1]

    dest_path = (current_path / destination).resolve()

    for source in sources:
        src_path = (current_path / source).resolve()

        if not src_path.exists():
            print(f"mv: {src_path}: Нет такого файла или директории")
            continue

        try:
            # Регистрируем для отмены
            if dest_path.is_dir():
                final_dest = dest_path / src_path.name
            else:
                final_dest = dest_path
            undo_stackking('mv', src_path, final_dest)

            shutil.move(str(src_path), str(dest_path))

        except Exception as e:
            print(f"mv: {e}")
            log_command(f"mv {' '.join(args)}", False, str(e))

    log_command(f"mv {' '.join(args)}")