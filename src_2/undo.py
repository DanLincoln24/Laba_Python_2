import shutil
from datetime import datetime
from pathlib import Path

# Стек для отмены действий
undo_stack = []


def undo_stackking(action_type: str, source: Path, destination: Path = None):
    undo_stack.append({
        'type': action_type,
        'source': source,
        'destination': destination,
        'timestamp': datetime.now()
    }) #делаем стек последних команд для возможной отмены


def undo_last_command(current_path: Path): #отмена последней команды
    if not undo_stack:
        print("Нет действий для отмены")
        return

    last_action = undo_stack.pop()

    try:
        if last_action['type'] == 'cp':
            # Удаляем скопированный файл
            if last_action['source'].is_dir():
                shutil.rmtree(last_action['source'])
            else:
                last_action['source'].unlink()
            print(f"Отменено копирование: {last_action['source']}")

        elif last_action['type'] == 'mv':
            # Возвращаем на исходное место
            shutil.move(str(last_action['destination']), str(last_action['source']))
            print(f"Отменено перемещение: {last_action['destination']} -> {last_action['source']}")

        elif last_action['type'] == 'rm':
            # Восстанавливаем из временной копии
            if last_action['source'].is_dir():
                shutil.copytree(last_action['source'], last_action['destination'])
                shutil.rmtree(last_action['source'])
            else:
                shutil.copy2(last_action['source'], last_action['destination'])
                last_action['source'].unlink()
            print(f"Отменено удаление: {last_action['destination']}")

        from log import log_command
        log_command("undo", True, f"Undid {last_action['type']}")

    except Exception as e:
        print(f"Ошибка при отмене: {e}")
        from log import log_command
        log_command("undo", False, str(e))