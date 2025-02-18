import os
import shutil
import argparse
from datetime import datetime


def reorganize(source, days, size):
    """
    Реорганизует файлы в указанной директории:
    - перемещает старые файлы в папку Archive
    - перемещает маленькие файлы в папку Small
    """
    # Проверяем существование исходной директории
    if not os.path.exists(source):
        print(f"Ошибка: Директория '{source}' не существует")
        return

    # Списки для хранения файлов
    archive_files = []
    small_files = []

    # Текущая дата для сравнения
    current_date = datetime.now()

    # Проверяем все файлы в директории
    for filename in os.listdir(source):
        path = os.path.join(source, filename)

        # Пропускаем папки
        if os.path.isdir(path):
            continue

        # Получаем информацию о файле
        stats = os.stat(path)
        days_old = (current_date - datetime.fromtimestamp(stats.st_mtime)).days

        # Проверяем условия и добавляем файлы в соответствующие списки
        if days_old > days:
            archive_files.append(filename)
        if stats.st_size < size:
            small_files.append(filename)

    # Обрабатываем старые файлы
    if archive_files:
        archive_dir = os.path.join(source, 'Archive')
        os.makedirs(archive_dir, exist_ok=True)
        for file in archive_files:
            shutil.move(os.path.join(source, file),
                        os.path.join(archive_dir, file))
        print(f"Перемещено {len(archive_files)} файлов в Archive")

    # Обрабатываем маленькие файлы
    small_files = [f for f in small_files if f not in archive_files]  # Исключаем уже перемещенные
    if small_files:
        small_dir = os.path.join(source, 'Small')
        os.makedirs(small_dir, exist_ok=True)
        for file in small_files:
            shutil.move(os.path.join(source, file),
                        os.path.join(small_dir, file))
        print(f"Перемещено {len(small_files)} файлов в Small")


if __name__ == '__main__':
    # Настраиваем параметры командной строки
    parser = argparse.ArgumentParser(description='Сортировка файлов по размеру и дате изменения')
    parser.add_argument('--source', required=True, help='Путь к директории')
    parser.add_argument('--days', type=int, required=True, help='Пороговое значение дней')
    parser.add_argument('--size', type=int, required=True, help='Пороговое значение размера в байтах')

    # Получаем аргументы и запускаем основную функцию
    args = parser.parse_args()
    reorganize(args.source, args.days, args.size)