import re

def find_word (text):
    return list(map(lambda x: x[0] + x[1], re.findall(r'(\b[A-Z][a-z]+\d{2}\b)|(\b[A-Z][a-z]+\d{4}\b)', text)))


message = input('Введите текст: ')
print(find_word(message))
