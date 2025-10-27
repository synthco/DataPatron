from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Optional


class LoadpipeError(Exception):
    """Базовий виняток пакета."""

    default_message = "Невідома помилка Loadpipe."

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        hint: Optional[str] = None,
        context: Optional[Mapping[str, Any]] = None,
    ) -> None:
        final_message = (message or self.default_message).strip()
        super().__init__(final_message)
        self.message = final_message
        self.hint = hint
        self.context = dict(context or {})

    def __str__(self) -> str:
        if self.hint:
            return f"{self.message} (hint: {self.hint})"
        return self.message

    def as_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"type": self.__class__.__name__, "message": self.message}
        if self.hint:
            data["hint"] = self.hint
        if self.context:
            data["context"] = self.context
        return data


class AuthError(LoadpipeError):
    """Помилка авторизації Google OAuth."""

    default_message = "Операція авторизації не вдалася."

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        path: Optional[Path | str] = None,
        hint: Optional[str] = None,
        context: Optional[Mapping[str, Any]] = None,
    ) -> None:
        ctx = dict(context or {})
        if path is not None:
            ctx.setdefault("path", str(path))
            hint = hint or "Перевірте client_secrets.json та токен авторизації."
        super().__init__(message, hint=hint, context=ctx)


class ConfigError(LoadpipeError):
    """Помилка валідaції конфігурації."""

    default_message = "Конфігурацію не вдалося опрацювати."

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        path: Optional[Path | str] = None,
        hint: Optional[str] = None,
        context: Optional[Mapping[str, Any]] = None,
    ) -> None:
        ctx = dict(context or {})
        if path is not None:
            ctx.setdefault("path", str(path))
            hint = hint or "Перевірте файл конфігурації та його схему."
        super().__init__(message, hint=hint, context=ctx)


class RateLimitError(LoadpipeError):
    """Перевищено ліміт запитів до API."""

    default_message = "Перевищено ліміт запитів."

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        retry_after: Optional[int] = None,
        hint: Optional[str] = None,
        context: Optional[Mapping[str, Any]] = None,
    ) -> None:
        ctx = dict(context or {})
        if retry_after is not None:
            ctx.setdefault("retry_after", retry_after)
            hint = hint or f"Спробуйте повторити через {retry_after} секунд."
        super().__init__(message, hint=hint, context=ctx)


class ResumeMismatchError(LoadpipeError):
    """Конфлікт кешованих метаданих завантаження."""

    default_message = "Збережені метадані не збігаються з файлом на сервері."


class IntegrityError(LoadpipeError):
    """Проблема з цілісністю локального сховища."""

    default_message = "Маніфест або кеш пошкоджено."

