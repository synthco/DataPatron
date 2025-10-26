
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Any

@dataclass
class FileMeta:
    id: str
    name: str
    size: Optional[int] = None
    md5: Optional[str] = None
    mime: Optional[str] = None
    modified: Optional[str] = None

@dataclass
class UploadSession:
    session_url: str
    name: str
    folder_id: str
    total: Optional[int] = None

def build_service(credentials: Any) -> Any:
    """Побудувати клієнт Drive (плейсхолдер)."""
    return object()

def list_files(service: Any, folder_id: str, pattern: Optional[str] = None) -> List[FileMeta]:
    """Повернути список файлів (плейсхолдер)."""
    # Поки що — повертаємо фіктивний один запис, щоб CLI показав таблицю.
    return [FileMeta(id="demo123", name="example.zst", size=12345678, mime="application/zstd", modified="2025-01-01T00:00:00Z")]

def stat(service: Any, file_id: str) -> FileMeta:
    return FileMeta(id=file_id, name="example.bin", size=1024, mime="application/octet-stream", modified="2025-01-01T00:00:00Z")

def download_range(service: Any, file_id: str, start: int, end: int) -> bytes:
    # Плейсхолдер діапазонного завантаження
    n = end - start + 1
    return b"\x00" * max(0, n)

def begin_resumable_upload(service: Any, name: str, folder_id: str, size: Optional[int] = None, mime: str = "application/octet-stream") -> UploadSession:
    return UploadSession(session_url="https://upload.example/session/abc", name=name, folder_id=folder_id, total=size)

def upload_chunk(service: Any, session: UploadSession, data: bytes, start: int, end: int, total: Optional[int] = None) -> int:
    # Повертаємо скільки відвантажено (плейсхолдер)
    return len(data)
