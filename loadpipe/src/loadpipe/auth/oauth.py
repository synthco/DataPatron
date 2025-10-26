
"""Google OAuth (локальний) — плейсхолдер для M1/M2.

Реальні виклики будуть додані в LP-4.x. Зараз надаємо сигнатури, щоб CLI не падав.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from ..errors import AuthError

class DummyCreds:
    """Плейсхолдер об'єкт облікових даних."""
    def __init__(self) -> None:
        self.token = "DUMMY"

def login(auth_config) -> None:
    """Плейсхолдер логіну: пояснення та виняток, якщо немає client_secrets.json."""
    import os
    path = getattr(auth_config, "client_secrets_path", ".secrets/client_secrets.json")
    if not os.path.exists(path):
        raise AuthError(f"Не знайдено {path}. Додайте client_secrets.json та повторіть.")
    # Реалізація буде додана пізніше (відкриття браузера, збереження токена)
    # Тимчасово просто створимо порожній token.json, якщо його нема.
    token_path = getattr(auth_config, "token_path", ".secrets/token.json")
    os.makedirs(os.path.dirname(token_path), exist_ok=True)
    if not os.path.exists(token_path):
        with open(token_path, "w", encoding="utf-8") as f:
            f.write("{}")

def credentials(auth_config) -> Any:
    """Повернути облікові дані (тимчасово DummyCreds)."""
    # Пізніше тут буде завантаження/оновлення токена через google-auth-oauthlib.
    return DummyCreds()
