"""Shared logging setup for backend scripts and application runtime."""

from __future__ import annotations

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from app.utils.paths import Paths


class _ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[35m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        original = record.levelname
        if record.levelno in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelno]}{record.levelname}{self.RESET}"
        try:
            return super().format(record)
        finally:
            record.levelname = original


def _resolved_level(level: str) -> int:
    return getattr(logging, level.upper(), logging.INFO)


def _build_console_handler(level: int, use_colors: bool) -> logging.Handler:
    log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter_cls = _ColorFormatter if use_colors else logging.Formatter
    console_handler.setFormatter(formatter_cls(log_format, datefmt=date_format))
    return console_handler


def _build_file_handler(
    log_dir: Path,
    log_file: str,
    level: int,
    max_bytes: int,
    backup_count: int,
) -> Optional[logging.Handler]:
    log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    Paths.ensure_dir(log_dir)
    target_path = log_dir / log_file
    try:
        file_handler = RotatingFileHandler(
            target_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
    except PermissionError:
        pid_target = target_path.with_name(f"{target_path.stem}.{os.getpid()}{target_path.suffix}")
        try:
            file_handler = RotatingFileHandler(
                pid_target,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
        except PermissionError:
            return None
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    return file_handler


def reset_logging(name: Optional[str] = None) -> logging.Logger:
    """Remove handlers so tests can start from a clean logger state."""
    logger = logging.getLogger(name)
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    logger.propagate = False
    return logger


def setup_logging(
    name: Optional[str] = None,
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_dir: Optional[Path] = None,
    use_colors: bool = True,
    max_bytes: int = 2 * 1024 * 1024,
    backup_count: int = 3,
    clear_handlers: bool = True,
) -> logging.Logger:
    """Create a stable logger configuration for scripts and runtime tools."""
    logger = logging.getLogger(name)
    resolved_level = _resolved_level(level)
    logger.setLevel(resolved_level)
    logger.propagate = False

    if clear_handlers:
        reset_logging(name)
        logger.setLevel(resolved_level)
    logger.addHandler(_build_console_handler(resolved_level, use_colors))

    if log_file:
        target_dir = Path(log_dir) if log_dir else Paths.logs()
        file_handler = _build_file_handler(
            log_dir=target_dir,
            log_file=log_file,
            level=resolved_level,
            max_bytes=max_bytes,
            backup_count=backup_count,
        )
        if file_handler is not None:
            logger.addHandler(file_handler)

    return logger


def setup_app_logging(
    level: str = "INFO",
    log_file: str = "app.log",
    log_dir: Optional[Path] = None,
    use_colors: bool = False,
) -> logging.Logger:
    """Configure root/application loggers once for the FastAPI runtime."""
    resolved_level = _resolved_level(level)
    root_logger = logging.getLogger()
    reset_logging()
    root_logger.setLevel(resolved_level)
    root_logger.propagate = False

    root_logger.addHandler(_build_console_handler(resolved_level, use_colors))
    file_handler = _build_file_handler(
        log_dir=Path(log_dir) if log_dir else Paths.logs(),
        log_file=log_file,
        level=resolved_level,
        max_bytes=2 * 1024 * 1024,
        backup_count=3,
    )
    if file_handler is not None:
        root_logger.addHandler(file_handler)

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        external_logger = logging.getLogger(logger_name)
        reset_logging(logger_name)
        external_logger.setLevel(resolved_level)
        external_logger.propagate = True

    return root_logger


def setup_production_logging(name: Optional[str] = None) -> logging.Logger:
    return setup_logging(name=name, level="INFO", log_file="app.log", use_colors=False)


def setup_debug_logging(name: Optional[str] = None) -> logging.Logger:
    return setup_logging(name=name, level="DEBUG", log_file="debug.log")


def setup_script_logging(
    name: Optional[str] = None,
    log_file: str = "script.log",
    level: str = "INFO",
) -> logging.Logger:
    return setup_logging(name=name, level=level, log_file=log_file)


def setup_dataset_logging(
    name: Optional[str] = None,
    log_file: str = "dataset_validation.log",
    level: str = "INFO",
) -> logging.Logger:
    """Convenience logger for dataset validation and audit scripts."""
    return setup_logging(name=name, level=level, log_file=log_file)
