import os
import argparse
import subprocess
import random
import sys
from glob import glob


def check_ffmpeg():
    """Проверяет, установлен ли FFmpeg в системе"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        return True
    except FileNotFoundError:
        print("Ошибка: FFmpeg не установлен или не найден в PATH")
        print("Установите FFmpeg и добавьте его в PATH")
        return False


def trackmix(source, destination=None, count=None, frame=10, log=False, extended=False):
    """
    Создает музыкальный микс из фрагментов MP3 файлов

    Параметры:
        source (str): Путь к директории с MP3 файлами
        destination (str): Путь к выходному файлу (по умолчанию mix.mp3 в source)
        count (int): Количество файлов для обработки (по умолчанию все MP3)
        frame (int): Длительность фрагмента в секундах (по умолчанию 10)
        log (bool): Выводить ли лог обработки
        extended (bool): Применять ли fade эффекты
    """
    # Проверяем наличие FFmpeg
    if not check_ffmpeg():
        return

    # Проверяем существование исходной директории
    if not os.path.exists(source):
        print(f"Ошибка: Директория '{source}' не существует")
        return

    # Если выходной файл не указан, создаем его в исходной директории
    if destination is None:
        destination = os.path.join(source, "mix.mp3")

    # Получаем список всех MP3 файлов в директории
    mp3_files = glob(os.path.join(source, "*.mp3"))

    if not mp3_files:
        print(f"Ошибка: В директории '{source}' не найдены MP3 файлы")
        return

    # Если указано количество файлов, берем только нужное количество
    if count is not None:
        count = min(count, len(mp3_files))
        mp3_files = mp3_files[:count]

    # Временная директория для фрагментов
    temp_dir = os.path.join(source, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Список временных файлов
        temp_files = []

        # Обрабатываем каждый файл
        for i, mp3_file in enumerate(mp3_files, 1):
            if log:
                print(f"--- processing file {i}: {os.path.basename(mp3_file)}")

            # Получаем длительность файла
            try:
                duration = float(subprocess.check_output([
                    'ffprobe', '-v', 'quiet',
                    '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1',
                    mp3_file
                ]))
            except subprocess.CalledProcessError:
                print(f"Ошибка при чтении файла: {mp3_file}")
                continue

            # Выбираем случайную позицию
            start = random.uniform(0, max(0, duration - frame))

            # Временный файл для фрагмента
            temp_file = os.path.join(temp_dir, f"temp_{i}.mp3")

            # Формируем команду FFmpeg
            ffmpeg_cmd = ['ffmpeg', '-y', '-i', mp3_file,
                          '-ss', str(start), '-t', str(frame)]

            # Добавляем fade эффекты если нужно
            if extended:
                ffmpeg_cmd.extend([
                    '-af', f'afade=t=in:st=0:d=1,afade=t=out:st={frame - 1}:d=1'
                ])

            ffmpeg_cmd.append(temp_file)

            # Выполняем команду
            try:
                subprocess.run(ffmpeg_cmd, capture_output=True, check=True)
                temp_files.append(temp_file)
            except subprocess.CalledProcessError:
                print(f"Ошибка при обработке файла: {mp3_file}")
                continue

        if not temp_files:
            print("Ошибка: Не удалось создать фрагменты")
            return

        # Создаем файл со списком для объединения
        concat_file = os.path.join(temp_dir, "files.txt")
        with open(concat_file, 'w', encoding='utf-8') as f:
            for temp_file in temp_files:
                f.write(f"file '{os.path.basename(temp_file)}'\n")

        # Объединяем все фрагменты
        try:
            subprocess.run([
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_file,
                '-c', 'copy',
                destination
            ], capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print("Ошибка при создании финального микса")
            return

        if log:
            print("--- done!")

    finally:
        # Удаляем временные файлы
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        if os.path.exists(concat_file):
            os.remove(concat_file)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Создание музыкального микса из MP3 файлов')
    parser.add_argument('--source', '-s', required=True,
                        help='Директория с MP3 файлами')
    parser.add_argument('--destination', '-d',
                        help='Путь к выходному файлу (по умолчанию mix.mp3)')
    parser.add_argument('--count', '-c', type=int,
                        help='Количество файлов для обработки')
    parser.add_argument('--frame', '-f', type=int, default=10,
                        help='Длительность фрагмента в секундах (по умолчанию 10)')
    parser.add_argument('--log', '-l', action='store_true',
                        help='Выводить лог обработки')
    parser.add_argument('--extended', '-e', action='store_true',
                        help='Применять fade эффекты')

    args = parser.parse_args()
    trackmix(
        args.source,
        args.destination,
        args.count,
        args.frame,
        args.log,
        args.extended
    )