"""Shared file helpers for the FastAPI backend."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Optional, Union

from fastapi import UploadFile

from app.config import settings
from app.utils.paths import Paths


PathLike = Union[str, Path]


def ensure_directories() -> None:
    """Create the runtime directories required by the backend."""
    Paths.init_runtime_dirs()


def generate_unique_filename(original_filename: Optional[str]) -> str:
    """Generate a collision-resistant upload filename."""
    suffix = Path(original_filename or "").suffix.lower()
    return f"temp_{uuid.uuid4().hex}{suffix}"


async def save_upload_file(
    file: UploadFile,
    upload_dir: PathLike,
    content: bytes | None = None,
) -> str:
    """Persist an uploaded file to disk and return the generated filename."""
    target_dir = Paths.ensure_dir(upload_dir)
    filename = generate_unique_filename(file.filename)
    file_path = target_dir / filename
    payload = content if content is not None else await file.read()
    file_path.write_bytes(payload)
    return filename


def get_file_path(filename: str, directory: PathLike) -> Path:
    return Path(directory) / filename


def get_static_file_url(filename: str, directory: str) -> str:
    base_url = settings.public_base_url.rstrip("/")
    directory = directory.strip("/").replace("\\", "/")
    return f"{base_url}/{directory}/{filename}"


def get_proxy_file_url(bucket: str, filename: str) -> str:
    base_url = settings.public_base_url.rstrip("/")
    return f"{base_url}/api/detection/files/{bucket}/{filename}"


def extract_object_filename(object_key: Optional[str]) -> str:
    if not object_key:
        return ""
    return Path(object_key).name
