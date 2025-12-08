# DataPatron

Репозиторій для дослідження Computational Social Science (KMA 2025): робота з Reddit-дампами, очищення даних та побудова локальної аналітики.

## Статус компонентів
- `loadpipe/` — внутрішній CLI для синку з Google Drive, **заморожений** і не використовувався під час дослідження; лишається в коді лише як архів.
- Робочі скрипти та ноутбуки знаходяться в `notebooks/` і `scripts/`.

## Швидкий старт
1. Python 3.10+.
2. Віртуальне середовище:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Дані очікуються в `data/` (див. шляхи всередині скриптів).

## Корисні файли
- `notebooks/Loading/to_csv.py` — конвертація `.zst` у відфільтрований CSV.
- `notebooks/Loading/columns_data.py` — швидке отримання списку колонок із `.zst`.
- `notebooks/Loading/db /init_db.py` — створення `reddit.db` у `data/` з CSV.

## Примітки
- Не коміть `.env`, кеші та великі дані; `.gitignore` вже містить основні винятки.
