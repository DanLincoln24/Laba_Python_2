import logging
from datetime import datetime


def dict_logging():
    logging.basicConfig(
        filename='log_file',
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ) #Настройка логирования


def log_command(command: str, success: bool = True, error_msg: str = ""):

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if success:
        logging.info(f"[{timestamp}] {command}")
    else:
        logging.error(f"[{timestamp}] {command} - {error_msg}") #логирование команды
