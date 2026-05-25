"""Path helpers for the RSOD backend."""

from __future__ import annotations

import inspect
import os
from pathlib import Path
from typing import Dict, Optional, Union


PathLike = Union[str, os.PathLike[str], Path]


def _clean_override(value: Optional[str]) -> Optional[str]:
    """Normalize blank environment variables to ``None``."""
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def find_project_root(
    start_path: Optional[PathLike] = None,
    marker_file: str = ".rsod_platform",
) -> Path:
    """Find the backend root by walking upwards until the marker file appears."""
    if start_path is None:
        caller = inspect.stack()[1]
        current = Path(caller.filename).resolve().parent
    else:
        current = Path(start_path).resolve()
        if current.is_file():
            current = current.parent

    for candidate in [current, *current.parents]:
        if (candidate / marker_file).exists():
            return candidate

    raise FileNotFoundError(
        f"Could not locate '{marker_file}' from '{current}'. "
        "Set RSOD_BACKEND_ROOT if the backend lives outside the default tree."
    )


class Paths:
    """Centralized path resolver for backend scripts and utilities."""

    _cache: Dict[str, Path] = {}

    @classmethod
    def reset_cache(cls) -> None:
        """Clear cached paths. Useful for tests that patch env vars."""
        cls._cache.clear()

    @classmethod
    def _resolve_override(cls, env_name: str) -> Optional[Path]:
        value = _clean_override(os.getenv(env_name))
        return Path(value).expanduser().resolve() if value else None

    @classmethod
    def _get_cached(cls, key: str, factory) -> Path:
        if key not in cls._cache:
            cls._cache[key] = factory()
        return cls._cache[key]

    @classmethod
    def root(cls) -> Path:
        return cls._get_cached(
            "root",
            lambda: cls._resolve_override("RSOD_BACKEND_ROOT")
            or find_project_root(Path(__file__)),
        )

    @classmethod
    def app(cls) -> Path:
        return cls.root() / "app"

    @classmethod
    def data(cls) -> Path:
        return cls._get_cached(
            "data",
            lambda: cls._resolve_override("RSOD_DATA_ROOT") or cls.root() / "data",
        )

    @classmethod
    def rsod_data(cls) -> Path:
        return cls._get_cached(
            "rsod_data",
            lambda: cls._resolve_override("RSOD_RSOD_DATA_ROOT")
            or cls.data() / "rsod",
        )

    @classmethod
    def train_root(cls) -> Path:
        return cls._get_cached(
            "train_root",
            lambda: cls._resolve_override("RSOD_TRAIN_ROOT")
            or cls.rsod_data() / "train",
        )

    @classmethod
    def train_images(cls) -> Path:
        return cls._get_cached(
            "train_images",
            lambda: cls._resolve_override("RSOD_TRAIN_IMAGES_ROOT")
            or cls.train_root() / "images",
        )

    @classmethod
    def train_labels(cls) -> Path:
        return cls._get_cached(
            "train_labels",
            lambda: cls._resolve_override("RSOD_TRAIN_LABELS_ROOT")
            or cls.train_root() / "labels",
        )

    @classmethod
    def models(cls) -> Path:
        return cls._get_cached(
            "models",
            lambda: cls._resolve_override("RSOD_MODELS_ROOT")
            or cls.root() / "models",
        )

    @classmethod
    def static(cls) -> Path:
        return cls._get_cached(
            "static",
            lambda: cls._resolve_override("RSOD_STATIC_ROOT")
            or cls.root() / "static",
        )

    @classmethod
    def uploads(cls) -> Path:
        return cls._get_cached(
            "uploads",
            lambda: cls._resolve_override("RSOD_UPLOAD_ROOT")
            or cls.static() / "uploads",
        )

    @classmethod
    def results(cls) -> Path:
        return cls._get_cached(
            "results",
            lambda: cls._resolve_override("RSOD_RESULTS_ROOT")
            or cls.static() / "results",
        )

    @classmethod
    def logs(cls) -> Path:
        return cls._get_cached(
            "logs",
            lambda: cls._resolve_override("RSOD_LOG_ROOT")
            or cls.data() / "logs",
        )

    @staticmethod
    def ensure_dir(path: PathLike) -> Path:
        resolved = Path(path)
        resolved.mkdir(parents=True, exist_ok=True)
        return resolved

    @classmethod
    def init_runtime_dirs(cls) -> None:
        for path in (
            cls.data(),
            cls.rsod_data(),
            cls.train_root(),
            cls.models(),
            cls.static(),
            cls.uploads(),
            cls.results(),
            cls.logs(),
        ):
            cls.ensure_dir(path)
