from __future__ import annotations

from pathlib import Path

import pytest

from loadpipe.errors import ResumeMismatchError
from loadpipe.state.manifest import Manifest


def _manifest(tmp_path: Path) -> Manifest:
    return Manifest(tmp_path / "manifest.sqlite")


def test_upsert_and_get_download(tmp_path):
    manifest = _manifest(tmp_path)

    manifest.upsert_download(
        file_id="file-1",
        name="report.csv",
        etag="etag-123",
        modified="2024-06-01T10:00:00Z",
        bytes_done=128,
        updated_at="2024-06-01T10:01:00Z",
    )

    record = manifest.get_download("file-1")
    assert record is not None
    assert record["file_id"] == "file-1"
    assert record["etag"] == "etag-123"
    assert record["bytes_done"] == 128


def test_upsert_download_detects_etag_mismatch(tmp_path):
    manifest = _manifest(tmp_path)
    manifest.upsert_download(
        file_id="file-2",
        name="photo.jpg",
        etag="etag-original",
        modified="2024-05-10T08:00:00Z",
        bytes_done=256,
        updated_at="2024-05-10T08:10:00Z",
    )

    with pytest.raises(ResumeMismatchError):
        manifest.upsert_download(
            file_id="file-2",
            name="photo.jpg",
            etag="etag-new",
            modified="2024-05-10T08:00:00Z",
            bytes_done=512,
            updated_at="2024-05-10T09:00:00Z",
        )


def test_upsert_download_detects_modified_mismatch(tmp_path):
    manifest = _manifest(tmp_path)
    manifest.upsert_download(
        file_id="file-3",
        name="presentation.pptx",
        etag="etag-777",
        modified="2024-05-01T00:00:00Z",
        bytes_done=1024,
        updated_at="2024-05-01T00:10:00Z",
    )

    with pytest.raises(ResumeMismatchError):
        manifest.upsert_download(
            file_id="file-3",
            name="presentation.pptx",
            etag="etag-777",
            modified="2024-05-02T00:00:00Z",
            bytes_done=2048,
            updated_at="2024-05-02T00:10:00Z",
        )
