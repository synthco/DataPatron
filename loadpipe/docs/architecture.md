
# Архітектура (спрощено)

- `adapters/gdrive.py`: доступ до Google Drive (листинг, скачування діапазонами, resumable upload).
- `io/download.py` / `io/upload.py`: ітератори, що відновлюються, оновлюють маніфест і логують прогрес.
- `state/manifest.py` + `state/schema.sql`: SQLite-маніфест (WAL) для докачок/дозаливок.
- `config.py`: dataclass-конфіги, валідація, `from_file()`.
- `log.py`: JSON-логер у stdout та файл `.logs/`.
- `processing/`: конвеєр обробки (поки `identity`).
- `cli.py`: команди `auth`, `list`, `pull`, `push`, `sync`.
