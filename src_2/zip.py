import zipfile
from pathlib import Path
from log import log_command
from undo import undo_stackking

def zip_command(args: list, current_path: Path):
    if len(args) < 2:
        print("zip: требуется 2 аргумента: папка и имя архива")
        return #Создание ZIP архива

    folder = (current_path / args[0]).resolve()
    archive_name = (current_path / args[1]).resolve()

    if not folder.exists() or not folder.is_dir():
        print(f"zip: {folder}: Нет такой директории")
        return

    try:
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in folder.rglob('*'):
                # Вычисляем относительный путь для архива
                arcname = file_path.relative_to(folder.parent)
                zipf.write(file_path, arcname)

        print(f"Создан архив: {archive_name}")
        log_command(f"zip {' '.join(args)}")
    except Exception as e:
        print(f"zip: {e}")
        log_command(f"zip {' '.join(args)}", False, str(e))


def unzip_command(args: list, current_path: Path):
    if not args:
        print("unzip: требуется аргумент - имя архива")
        return #Распаковка ZIP архива

    archive_name = (current_path / args[0]).resolve()

    if not archive_name.exists():
        print(f"unzip: {archive_name}: Нет такого файла")
        return

    try:
        with zipfile.ZipFile(archive_name, 'r') as zipf:
            zipf.extractall(current_path)

        print(f"Распакован архив: {archive_name}")
        log_command(f"unzip {' '.join(args)}")
    except Exception as e:
        print(f"unzip: {e}")
        log_command(f"unzip {' '.join(args)}", False, str(e))