"""Centralized logging configuration using loguru."""
from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from app.config.settings import settings


def setup_logging() -> None:
    """Configure loguru sinks for stdout and rotating file."""
    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Console
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.log_level,
        backtrace=settings.app_debug,
        diagnose=settings.app_debug,
        enqueue=True,
    )

    # Rotating file
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        str(log_path),
        format=log_format,
        level=settings.log_level,
        rotation=settings.log_max_bytes,
        retention=settings.log_backup_count,
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=False,
    )

    logger.info("Logging initialized | level={} env={}", settings.log_level, settings.app_env)


__all__ = ["logger", "setup_logging"]
