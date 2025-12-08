import zstandard
import os
import json
import sys
import logging

log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


# (Функція read_and_decode)
def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
    chunk = reader.read(chunk_size)
    bytes_read += chunk_size
    if previous_chunk is not None:
        chunk = previous_chunk + chunk
    try:
        return chunk.decode()
    except UnicodeDecodeError:
        if bytes_read > max_window_size:
            raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
        return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)


# (Функція read_lines_zst)
def read_lines_zst(file_name):
    with open(file_name, 'rb') as file_handle:
        buffer = ''
        reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
        while True:
            chunk = read_and_decode(reader, 2**27, (2**29) * 2)
            if not chunk:
                break
            lines = (buffer + chunk).split("\n")
            for line in lines[:-1]:
                yield line, file_handle.tell()
            buffer = lines[-1]
        reader.close()


# ✅ НОВА ФУНКЦІЯ: зберігає знайдені колонки у файл
def extract_and_save_columns(zst_path, output_dir="."):
    """
    Знаходить колонки у ZST-файлі з JSON-рядками і зберігає результат у текстовий файл.
    """
    log.info(f"Відкриваємо {zst_path}, щоб подивитися колонки...")

    output_file = os.path.join(
        output_dir,
        f"columns_{os.path.splitext(os.path.basename(zst_path))[0]}.txt"
    )

    try:
        for line, _ in read_lines_zst(zst_path):
            try:
                obj = json.loads(line)
                columns = list(obj.keys())

                # Друк у консоль
                print("--- ЗНАЙДЕНО КОЛОНКИ ---")
                print(columns)
                print("-------------------------")

                # Збереження у файл
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(columns))

                log.info(f"✅ Колонки збережено у: {output_file}")
                return columns

            except json.JSONDecodeError:
                log.warning("Пошкоджений рядок, пробуємо наступний...")
                continue

    except Exception as err:
        log.error(f"Сталася помилка: {err}")
        return None


# --- Запуск із командного рядка ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Помилка: потрібно вказати шлях до вхідного ZST-файлу.")
        sys.exit(1)

    file_path = sys.argv[1]
    extract_and_save_columns(file_path, output_dir=".")
