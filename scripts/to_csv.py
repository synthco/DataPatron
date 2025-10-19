# this converts a zst file to csv
#
# it's important to note that the resulting file will likely be quite large
# and you probably won't be able to open it in excel or another csv reader
#
# arguments are inputfile, outputfile, fields
# call this like
# python to_csv.py wallstreetbets_submissions.zst wallstreetbets_submissions.csv author,selftext,title

import zstandard
import os
import json
import sys
from datetime import datetime
import logging.handlers
import csv

log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


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
    log.info(f"Decoding error with {bytes_read:,} bytes, reading another chunk")
    return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)


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


if __name__ == "__main__":
  # --- БЛОК НАЛАШТУВАНЬ (РЕДАГУЙ ЦЕ!) ---
  
  # 1. Вкажи тут сабредіти, які ти хочеш відфільтрувати
  # Це найважливіший фільтр!
  TARGET_SUBREDDITS = {"ukraine", "war", "russia", "putin", "nazi", "nato", "corrupt", "zelenskyy", "khokhol", "liberation", "donbas", "bandera"}
  
  # 2. Вкажи, скільки МАКСИМУМ рядків ти хочеш зберегти
  # 1,000,000 — це вже буде великий CSV, але керований.
  # Для тесту можеш поставити 10000
  MAX_LINES_TO_SAVE = 20_000
  
  # 3. Назва вихідного файлу
  OUTPUT_FILE_NAME = "test_filtered_data_2025_07.csv"
  
  # 4. Заголовки для твого CSV файлу
  CSV_HEADER = ['id', 'author', 'subreddit', 'created_utc', 'text', 'score']
  # --- ---

  if len(sys.argv) < 2:
      print("Помилка: Потрібно вказати шлях до вхідного ZST файлу.")
      print(f"Приклад: python {sys.argv[0]} /шлях/до/RC_2025-07.zst")
      sys.exit(1)
      
  file_path = sys.argv[1]
  
  # Переконуємося, що вихідний файл збережеться в тій же папці, що і скрипт
  script_dir = os.path.dirname(os.path.abspath(__file__))
  output_file_path = os.path.join(script_dir, OUTPUT_FILE_NAME)
  
  file_size = os.stat(file_path).st_size
  file_lines = 0
  file_bytes_processed = 0
  created = None
  bad_lines = 0
  lines_saved = 0  # Лічильник збережених рядків

  try:
    with open(output_file_path, 'w', newline='', encoding='utf-8') as f_out:
      writer = csv.writer(f_out)
      writer.writerow(CSV_HEADER)
      
      log.info(f"Розпочато обробку {file_path}.")
      log.info(f"Фільтруємо за сабредітами: {TARGET_SUBREDDITS}")
      log.info(f"Результат буде збережено у {output_file_path}")

      for line, file_bytes_processed in read_lines_zst(file_path):
        try:
          obj = json.loads(line)
          
          # --- ЛОГІКА ФІЛЬТРАЦІЇ ---
          if obj.get('subreddit') in TARGET_SUBREDDITS:
            row = [
                obj.get('id'),
                obj.get('author'),
                obj.get('subreddit'),
                obj.get('created_utc'),
                obj.get('body'),  # 'body' для коментарів
                obj.get('score')
            ]
            writer.writerow(row)
            lines_saved += 1
          # --- ---
          
          created = datetime.utcfromtimestamp(int(obj['created_utc']))
          
        except (KeyError, json.JSONDecodeError) as err:
          bad_lines += 1
        
        file_lines += 1
        
        # Лог прогресу
        if file_lines % 1000 == 0:
          log.info(f"{created.strftime('%Y-%m-%d %H:%M:%S')} : Оброблено: {file_lines:,} : Збережено: {lines_saved:,} : {(file_bytes_processed / file_size) * 100:.0f}%")

        # --- ЛОГІКА ЛІМІТУ ---
        if lines_saved >= MAX_LINES_TO_SAVE:
          log.info(f"Досягнуто ліміту в {lines_saved:,} рядків. Зупиняємось.")
          break # Виходимо з головного циклу
          
  except Exception as err:
    log.info(err)

  log.info(f"Завершено. Всього оброблено: {file_lines:,}. Збережено у CSV: {lines_saved:,}. Пошкоджених рядків: {bad_lines:,}")

