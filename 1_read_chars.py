def read_chars(filename):
    char_count = {}

    try:
        with open(filename, encoding='utf-8') as f:
            for line in f:
                for char in line.lower():
                    if char.isalpha():
                        char_count[char] = char_count.get(char, 0) + 1

        # Сортируем символы по частоте (по убыванию)
        sorted_chars = sorted(char_count.keys(),
                              key=lambda x: char_count[x],
                              reverse=True)

        return sorted_chars

    except FileNotFoundError:
        return f"Ошибка: файл {filename} не найден"
    except Exception as e:
        return f"Произошла ошибка при чтении файла: {str(e)}"

print(read_chars('text1.txt'))
print(read_chars('text2.txt'))
print(read_chars('text3.txt'))