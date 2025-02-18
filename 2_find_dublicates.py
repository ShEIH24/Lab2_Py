import os
import hashlib
from collections import defaultdict


def get_file_hash(filepath):
    """Вычисляет MD5-хеш файла"""
    md5_hash = hashlib.md5()

    with open(filepath, 'rb') as f:
        # Читаем файл блоками по 8192 байта
        while chunk := f.read(8192):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()


def find_duplicates(directory):
    """
    Находит дубликаты файлов в директории и подпапках.
    Возвращает словарь, где ключ - хеш, значение - список путей к файлам
    """
    hash_dict = defaultdict(list)

    # Обходим все файлы в директории и подпапках
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_hash = get_file_hash(filepath)
                hash_dict[file_hash].append(filepath)
            except:
                continue

    # Оставляем только группы с дубликатами (больше одного файла)
    return {hash_val: paths for hash_val, paths in hash_dict.items()
            if len(paths) > 1}


def print_duplicates(duplicates):
    """Выводит найденные группы дубликатов"""
    if not duplicates:
        print("Дубликаты не найдены")
        return

    for hash_val, file_list in duplicates.items():
        print(f"\nДубликаты (MD5: {hash_val}):")
        for file_path in file_list:
            print(f"- {file_path}")

directory = r'D:\Users\korol\ИВТ\2kurs\2semestr\Programming\Lab2_Py'
dupes = find_duplicates(directory)
print_duplicates(dupes)