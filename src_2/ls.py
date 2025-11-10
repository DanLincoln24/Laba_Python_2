import os
import stat
from datetime import datetime
from pathlib import Path
from log import log_command
from undo import undo_stackking


def ls_command(args: list, current_path: Path):
    path = current_path
    detailed = False

    # Обработка аргументов
    for arg in args:
        if arg == "-l":
            detailed = True
        else:
            path = (current_path / arg).resolve()

    if not path.exists() or not path.is_dir():
        print(f"ls: {path}: Нет такой директории")
        log_command(f"ls {' '.join(args)}", False, "No such directory")
        return

    # Получаем список файлов и сортируем
    try:
        items = list(path.iterdir())
        items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        for item in items:
            if detailed:
                # Получаем информацию о файле
                stat_info = item.stat()
                size = stat_info.st_size
                mtime = datetime.fromtimestamp(stat_info.st_mtime)
                permissions = get_permissions(item)

                print(f"{permissions} {size:8} {mtime:%Y-%m-%d %H:%M} {item.name}")
            else:
                print(item.name)

        log_command(f"ls {' '.join(args)}")
    except Exception as e:
        print(f"ls: {e}")
        log_command(f"ls {' '.join(args)}", False, str(e))


def get_permissions(path: Path) -> str:
    try:
        mode = path.stat().st_mode
        permissions = [] # Получение прав доступа в формате 'ls -l'

        # Тип файла
        if path.is_dir():
            permissions.append('d')
        else:
            permissions.append('-')

        # Права доступа пользователя
        permissions.append('r' if mode & stat.S_IRUSR else '-')
        permissions.append('w' if mode & stat.S_IWUSR else '-')
        permissions.append('x' if mode & stat.S_IXUSR else '-')

        # Права доступа группы
        permissions.append('r' if mode & stat.S_IRGRP else '-')
        permissions.append('w' if mode & stat.S_IWGRP else '-')
        permissions.append('x' if mode & stat.S_IXGRP else '-')

        # остальные права доступа
        permissions.append('r' if mode & stat.S_IROTH else '-')
        permissions.append('w' if mode & stat.S_IWOTH else '-')
        permissions.append('x' if mode & stat.S_IXOTH else '-')

        return ''.join(permissions)
    except:
        return '??????????'