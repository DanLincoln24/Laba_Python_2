import os
from datetime import datetime
from pathlib import Path

# Глобальная переменная для истории
command_history = []


def add_to_history(command: str): #Добавление команды в историю
    command_history.append({
        'command': command,
        'timestamp': datetime.now(),
        'cwd': Path.cwd()
    })
    # Сохраняем в файл
    save_history_to_file()


def save_history_to_file():

    try:
        with open('.history', 'w', encoding='utf-8') as f:
            for i, item in enumerate(command_history[-100:], 1):  # последние 100 команд
                f.write(f"{i}: {item['timestamp']} - {item['cwd']} - {item['command']}\n")
    except Exception as e:
        print(f"Ошибка сохранения истории: {e}") #Сохранение истории в файл


def load_history(): #Загрузка истории из файла
    global command_history
    try:
        if Path('.history').exists():
            with open('.history', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    # Парсим строку истории
                    parts = line.split(' - ', 2)
                    if len(parts) == 3:
                        command_history.append({
                            'command': parts[2].strip(),
                            'timestamp': datetime.fromisoformat(parts[0].split(': ', 1)[1]),
                            'cwd': Path(parts[1])
                        })
    except Exception as e:
        print(f"Ошибка загрузки истории: {e}")


def show_history():
    if not command_history:
        print("История команд пуста") #Показывает историю команд
        return

    start_idx = max(0, len(command_history) - 10)  # будет выводить Последние 10 команд
    for i, item in enumerate(command_history[start_idx:], start_idx + 1):
        print(f"{i}: {item['command']}")


# Загружаем историю при импорте модуля
load_history()