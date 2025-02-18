import os
import re


def rename_music_files(music_dir, tracklist_path):
    """
    Переименовывает музыкальные файлы в директории согласно списку треков из текстового файла.

    Args:
        music_dir (str): Путь к директории с музыкальными файлами
        tracklist_path (str): Путь к текстовому файлу со списком треков
    """
    # Читаем файл со списком треков и создаем словарь {название: номер}
    tracks = {}
    with open(tracklist_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Ищем строки формата "01. Freefall [6:12]"
            if match := re.match(r'(\d+)\.\s+(.+?)\s*\[\d+:\d+\]', line.strip()):
                tracks[match.group(2).strip()] = match.group(1)

    # Получаем список музыкальных файлов из директории
    music_files = [f for f in os.listdir(music_dir)
                   if f.lower().endswith(('.mp3', '.flac', '.m4a', '.wav'))]

    # Для каждого трека из списка ищем и переименовываем файл
    for song_name, track_number in tracks.items():
        # Ищем файл с соответствующим названием (без учета регистра)
        matching_file = next(
            (f for f in music_files
             if os.path.splitext(f)[0].lower() == song_name.lower()),
            None
        )

        if matching_file:
            # Формируем новое имя, сохраняя оригинальное расширение
            new_name = f"{track_number}. {song_name}{os.path.splitext(matching_file)[1]}"
            try:
                # Переименовываем файл
                os.rename(
                    os.path.join(music_dir, matching_file),
                    os.path.join(music_dir, new_name)
                )
                print(f"Переименован: {matching_file} -> {new_name}")
            except OSError as e:
                print(f"Ошибка при переименовании {matching_file}: {e}")
        else:
            print(f"Не найден файл для трека: {song_name}")

rename_music_files(r'D:\Users\korol\ИВТ\2kurs\2semestr\Programming\Lab2_Py\music_example', r'D:\Users\korol\ИВТ\2kurs\2semestr\Programming\Lab2_Py\music_example\names.txt')