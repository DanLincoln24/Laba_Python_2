import os
from pathlib import Path
from log import log_command
from undo import undo_stackking


def cd_command(args: list, current_path: Path) -> Path:
    if not args:
        target = Path.home()
    else:
        target = args[0]

    try:
        if target == "~":
            new_path = Path.home()
        elif target == "..":
            new_path = current_path.parent
        elif target == "-":
            # Возврат к предыдущей директории (базовый вариант)
            new_path = Path.home()
        else:
            new_path = (current_path / target).resolve()

        if new_path.exists() and new_path.is_dir():
            os.chdir(new_path)
            log_command(f"cd {' '.join(args)}")
            return new_path
        else:
            print(f"cd: {target}: Нет такой директории")
            log_command(f"cd {' '.join(args)}", False, "No such directory")
            return current_path
    except Exception as e:
        print(f"cd: {e}")
        log_command(f"cd {' '.join(args)}", False, str(e))
        return current_path


