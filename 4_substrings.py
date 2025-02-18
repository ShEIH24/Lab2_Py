import re


def find_numbers(file):
    pattern = r'\(\d{3}\)(?:\d{7}|\d{3}-\d{2}-\d{2})'
    try:
        with open(file, 'r', encoding='utf-8') as f:
            # Читаем файл построчно
            for line_num, line in enumerate(f, 1):
                # Ищем все совпадения в текущей строке
                for match in re.finditer(pattern, line):
                    print(f"Строка {line_num}, позиция {match.start() + 1} : найдено '{match.group()}'")

    except FileNotFoundError:
        print(f"Файл {file} не найден")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


find_numbers('numbers.txt')