
# loadpipe

Мінімальний каркас CLI-пакета для синхронізації файлів (Google Drive ⇄ локально) з підтримкою відновлення, кешу та ідемпотентності.

## Швидкий старт
```bash
# всередині репозиторію
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
lp --help
lp version
```

> Примітка: файл конфігу за замовчуванням — `configs/config.yaml`. Див. приклад у каталозі `configs/`.
