import tarfile
from pathlib import Path
from log import log_command


def tar_command(args: list, current_path: Path):
    if len(args) < 2:
        print("tar: требуется 2 аргумента: папка и имя архива")
        return #Создание TAR архива

    folder = (current_path / args[0]).resolve()
    archive_name = (current_path / args[1]).resolve()

    if not folder.exists() or not folder.is_dir():
        print(f"tar: {folder}: Нет такой директории")
        return

    try:
        with tarfile.open(archive_name, 'w:gz') as tar:
            tar.add(folder, arcname=folder.name)

        print(f"Создан архив: {archive_name}")
        log_command(f"tar {' '.join(args)}")
    except Exception as e:
        print(f"tar: {e}")
        log_command(f"tar {' '.join(args)}", False, str(e))


def untar_command(args: list, current_path: Path):
    if not args:
        print("untar: требуется аргумент - имя архива")
        return #Распаковка TAR архива

    archive_name = (current_path / args[0]).resolve()

    if not archive_name.exists():
        print(f"untar: {archive_name}: Нет такого файла")
        return

    try:
        with tarfile.open(archive_name, 'r:gz') as tar:
            tar.extractall(current_path)

        print(f"Распакован архив: {archive_name}")
        log_command(f"untar {' '.join(args)}")
    except Exception as e:
        print(f"untar: {e}")
        log_command(f"untar {' '.join(args)}", False, str(e))