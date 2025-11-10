import shutil
from datetime import datetime
from pathlib import Path
from log import log_command
from undo import undo_stackking

def rm_command(args: list, current_path: Path):
    """Команда rm - удаление файлов/директорий"""
    if not args:
        print("rm: требуется аргумент")
        return

    recursive = False
    targets = []

    for arg in args:
        if arg == "-r":
            recursive = True
        else:
            targets.append(arg)

    for target in targets:
        target_path = (current_path / target).resolve()

        # Защита от удаления корневых директорий
        if str(target_path) in ['/', '\\'] or target_path.parent == target_path:
            print("rm: запрещено удалять корневую директорию")
            continue

        if not target_path.exists():
            print(f"rm: {target_path}: Нет такого файла или директории")
            continue

        try:
            if target_path.is_dir():
                if not recursive:
                    print(f"rm: {target_path}: Это директория (используйте -r)")
                    continue

                # Запрос подтверждения для директорий
                response = input(f"Удалить директорию '{target_path}'? [y/N]: ")
                if response.lower() != 'y':
                    continue

            # Создаем временную копию для возможного восстановления
            temp_backup = Path(".trash") / f"{target_path.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            temp_backup.parent.mkdir(exist_ok=True)

            if target_path.is_dir():
                shutil.copytree(target_path, temp_backup)
                shutil.rmtree(target_path)
            else:
                shutil.copy2(target_path, temp_backup)
                target_path.unlink()

            # Регистрируем для отмены
            undo_stackking('rm', temp_backup, target_path)

        except Exception as e:
            print(f"rm: {e}")
            log_command(f"rm {' '.join(args)}", False, str(e))

    log_command(f"rm {' '.join(args)}")