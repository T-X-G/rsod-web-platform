#!/usr/bin/env python3
"""Validate and summarize a YOLO training dataset."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from app.config import settings
from app.utils.logging_utils import setup_dataset_logging
from app.utils.paths import Paths
from app.utils.validation import CheckContext, DataValidator


@dataclass
class AuditPlan:
    train_root: Path
    images_dir: Path
    labels_dir: Path
    classes: Sequence[str]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a YOLO training dataset.")
    parser.add_argument("--train-root", type=Path, default=Paths.train_root())
    parser.add_argument("--images-dir", type=Path)
    parser.add_argument("--labels-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--log-level", default="INFO")
    parser.add_argument("--log-file")
    parser.add_argument(
        "--classes",
        nargs="*",
        default=list(settings.target_names),
        help="Override the configured class list for class-id validation.",
    )
    return parser


def build_plan(args: argparse.Namespace) -> AuditPlan:
    train_root = args.train_root.expanduser().resolve()
    images_dir = (
        args.images_dir.expanduser().resolve()
        if args.images_dir
        else train_root / "images"
    )
    labels_dir = (
        args.labels_dir.expanduser().resolve()
        if args.labels_dir
        else train_root / "labels"
    )

    return AuditPlan(
        train_root=train_root,
        images_dir=images_dir,
        labels_dir=labels_dir,
        classes=list(args.classes),
    )


def build_context(plan: AuditPlan) -> CheckContext:
    return CheckContext(
        train_root=plan.train_root,
        images_dir=plan.images_dir,
        labels_dir=plan.labels_dir,
        classes=list(plan.classes),
    )


def audit_dataset(plan: AuditPlan, strict: bool, dry_run: bool, logger) -> bool:
    validator = DataValidator(build_context(plan))
    report = validator.validate()
    validator.validate_and_report(logger=logger)
    if dry_run:
        logger.info("Dry run enabled, no files will be written.")
    if strict and report.warnings:
        logger.error("Strict mode treats warnings as failures.")
        return False
    return report.ok


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    log_file = args.log_file if args.log_file is not None else (
        None if args.dry_run else "dataset_validation.log"
    )
    logger = setup_dataset_logging(
        name="convert_rsod",
        level=args.log_level,
        log_file=log_file,
    )

    try:
        plan = build_plan(args)
        logger.info("Backend root: %s", Paths.root())
        logger.info("Train root: %s", plan.train_root)
        logger.info("Images dir: %s", plan.images_dir)
        logger.info("Labels dir: %s", plan.labels_dir)

        passed = audit_dataset(
            plan,
            strict=args.strict,
            dry_run=args.dry_run,
            logger=logger,
        )
        if not passed:
            logger.error("Dataset audit failed.")
            return 1

        logger.info("Dataset audit finished successfully.")
        return 0
    except Exception as exc:
        logger.exception("Dataset audit failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
