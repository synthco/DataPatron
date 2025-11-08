from __future__ import annotations

import logging
import sys
import types
from typing import Iterable, Optional


googleapiclient = types.ModuleType("googleapiclient")
googleapiclient.discovery = types.ModuleType("googleapiclient.discovery")
googleapiclient.errors = types.ModuleType("googleapiclient.errors")


class _DummyHttpError(Exception):
    pass


def _dummy_build(*args, **kwargs):  # pragma: no cover - helper for optional dependency
    raise NotImplementedError


googleapiclient.discovery.build = _dummy_build  # type: ignore[attr-defined]
googleapiclient.errors.HttpError = _DummyHttpError  # type: ignore[attr-defined]

sys.modules.setdefault("googleapiclient", googleapiclient)
sys.modules.setdefault("googleapiclient.discovery", googleapiclient.discovery)
sys.modules.setdefault("googleapiclient.errors", googleapiclient.errors)

import loadpipe.io.upload as upload_mod


class DummyManifest:
    def __init__(self, record: Optional[dict[str, object]] = None) -> None:
        self.record = dict(record or {})
        self.upserts: list[dict[str, object]] = []

    def get_upload(self, session_id: str) -> Optional[dict[str, object]]:
        if self.record.get("session_id") == session_id:
            return dict(self.record)
        return None

    def upsert_upload(
        self,
        *,
        session_id: str,
        file_id: Optional[str] = None,
        name: Optional[str] = None,
        folder_id: Optional[str] = None,
        bytes_done: int = 0,
        total: Optional[int] = None,
        updated_at: Optional[str] = None,
    ) -> dict[str, object]:
        entry: dict[str, object] = {
            "session_id": session_id,
            "file_id": file_id,
            "name": name,
            "folder_id": folder_id,
            "bytes_done": bytes_done,
            "total": total,
            "updated_at": updated_at,
        }
        self.upserts.append(entry)
        self.record = dict(entry)
        return dict(entry)


class DummyService:
    pass


def _data_chunks(payload: bytes, chunk_size: int) -> Iterable[bytes]:
    for idx in range(0, len(payload), chunk_size):
        yield payload[idx : idx + chunk_size]


def test_resume_uses_remote_offset_when_server_is_behind(monkeypatch) -> None:
    manifest = DummyManifest(
        {
            "session_id": "session",
            "name": "file.bin",
            "folder_id": "folder",
            "bytes_done": 10,
            "total": 20,
        }
    )

    remote_offsets = [4]
    monkeypatch.setattr(
        upload_mod.gdrive,
        "query_upload_status",
        lambda service, session, total=None: remote_offsets.pop(0),
    )

    starts: list[int] = []

    def _upload_chunk(service, session, chunk, start, end, total=None):
        starts.append(start)
        return end + 1

    monkeypatch.setattr(upload_mod.gdrive, "upload_chunk", _upload_chunk)

    data = list(_data_chunks(b"0123456789abcdefghij", 10))
    logger = logging.getLogger("loadpipe.test")

    result = list(
        upload_mod.upload_iter(
            DummyService(),
            manifest,
            data_iter=data,
            name="file.bin",
            folder_id="folder",
            logger=logger,
            total=20,
            session_url="session",
        )
    )

    assert starts[0] == 4
    assert result[-1] == 20
    assert manifest.upserts[0]["bytes_done"] == 4


def test_resume_advances_to_remote_offset_when_ahead(monkeypatch) -> None:
    manifest = DummyManifest(
        {
            "session_id": "session",
            "name": "file.bin",
            "folder_id": "folder",
            "bytes_done": 10,
            "total": 30,
        }
    )

    remote_offsets = [14]
    monkeypatch.setattr(
        upload_mod.gdrive,
        "query_upload_status",
        lambda service, session, total=None: remote_offsets.pop(0),
    )

    starts: list[int] = []

    def _upload_chunk(service, session, chunk, start, end, total=None):
        starts.append(start)
        return end + 1

    monkeypatch.setattr(upload_mod.gdrive, "upload_chunk", _upload_chunk)

    data = list(_data_chunks(b"0123456789abcdefghijklmnopqrst", 10))
    logger = logging.getLogger("loadpipe.test")

    result = list(
        upload_mod.upload_iter(
            DummyService(),
            manifest,
            data_iter=data,
            name="file.bin",
            folder_id="folder",
            logger=logger,
            total=30,
            session_url="session",
        )
    )

    assert starts[0] == 14
    assert result[-1] == 30
    assert manifest.upserts[0]["bytes_done"] == 14
