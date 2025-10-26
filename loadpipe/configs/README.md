
# Конфіги `loadpipe`

Файл конфігурації — YAML. За замовчуванням очікується шлях `configs/config.yaml`.

## Розділи та поля

```yaml
runtime:
  cache_dir: ".cache/loadpipe"
  state_db: ".state/manifest.sqlite"
  cache_limit_gb: 30
  retries: 5
  log_dir: ".logs"

auth:
  # шлях до client_secrets.json (для OAuth) і файл токена
  client_secrets_path: ".secrets/client_secrets.json"
  token_path: ".secrets/token.json"
  scopes:
    - "https://www.googleapis.com/auth/drive"

source:
  folder_id: "DRIVE_FOLDER_ID"
  pattern: "*.zst"   # опційно

download:
  chunk_mb: 64

process:
  kind: "identity"   # placeholder

upload:
  folder_id: "DRIVE_TARGET_FOLDER_ID"
  name_suffix: ""    # опційно
```

## Використання
```bash
lp sync --config configs/config.yaml
```
