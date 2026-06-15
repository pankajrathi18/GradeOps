"""Unit tests for local file storage."""

from types import SimpleNamespace

import app.services.storage as storage_module
from app.services.storage import StorageService


def _storage_service(monkeypatch, tmp_path):
    monkeypatch.setattr(
        storage_module,
        "get_settings",
        lambda: SimpleNamespace(
            storage_backend="local",
            s3_bucket=None,
            upload_dir=tmp_path,
            s3_prefix="gradeops",
        ),
    )
    return StorageService()


def test_save_upload_file_writes_nested_local_path(monkeypatch, tmp_path):
    storage = _storage_service(monkeypatch, tmp_path)

    saved_path = storage.save_upload_file(b"exam contents", "submissions/42", "exam.pdf")

    assert saved_path == tmp_path / "submissions" / "42" / "exam.pdf"
    assert saved_path.read_bytes() == b"exam contents"
    assert storage.resolve_local_path(str(saved_path)) == saved_path


def test_s3_key_normalizes_prefix_and_path_separators(monkeypatch, tmp_path):
    storage = _storage_service(monkeypatch, tmp_path)

    assert storage._s3_key(r"\submissions\42\exam.pdf") == "gradeops/submissions/42/exam.pdf"
