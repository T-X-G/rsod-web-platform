"""Composable YOLO dataset validation utilities for RSOD workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple

import cv2
import numpy as np


VALIDATOR_REGISTRY: Dict[str, Callable[["DataValidator"], List["CheckResult"]]] = {}
IGNORED_NAMES = {".ds_store"}
DEFAULT_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")
DEFAULT_LABEL_EXTENSIONS = (".txt",)
DEFAULT_CLASSES: Tuple[str, ...] = ()


class CheckLevel(str, Enum):
    PASS = "pass"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class CheckContext:
    train_root: Optional[Path] = None
    images_dir: Optional[Path] = None
    labels_dir: Optional[Path] = None
    classes: Sequence[str] = field(default_factory=lambda: list(DEFAULT_CLASSES))
    image_extensions: Sequence[str] = field(
        default_factory=lambda: list(DEFAULT_IMAGE_EXTENSIONS)
    )
    label_extensions: Sequence[str] = field(
        default_factory=lambda: list(DEFAULT_LABEL_EXTENSIONS)
    )
    ignored_names: Set[str] = field(default_factory=lambda: set(IGNORED_NAMES))
    extra: Dict[str, Any] = field(default_factory=dict)

    def normalized_image_extensions(self) -> Set[str]:
        return {ext.lower() for ext in self.image_extensions}

    def normalized_label_extensions(self) -> Set[str]:
        return {ext.lower() for ext in self.label_extensions}


@dataclass
class CheckResult:
    name: str
    level: CheckLevel
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.level != CheckLevel.ERROR


@dataclass
class ValidationReport:
    results: List[CheckResult] = field(default_factory=list)

    @property
    def errors(self) -> List[CheckResult]:
        return [result for result in self.results if result.level == CheckLevel.ERROR]

    @property
    def warnings(self) -> List[CheckResult]:
        return [result for result in self.results if result.level == CheckLevel.WARNING]

    @property
    def infos(self) -> List[CheckResult]:
        return [result for result in self.results if result.level == CheckLevel.INFO]

    @property
    def passes(self) -> List[CheckResult]:
        return [result for result in self.results if result.level == CheckLevel.PASS]

    @property
    def ok(self) -> bool:
        return not self.errors

    def summary(self) -> Dict[str, int]:
        return {
            "total": len(self.results),
            "pass": len(self.passes),
            "info": len(self.infos),
            "warning": len(self.warnings),
            "error": len(self.errors),
        }


def build_report(results: Sequence[CheckResult]) -> ValidationReport:
    return ValidationReport(results=list(results))


def validate_upload_payload(
    filename: str,
    content_type: Optional[str],
    content: bytes,
    allowed_extensions: Sequence[str],
    allowed_mime_types: Sequence[str],
) -> ValidationReport:
    """Validate a single uploaded image before it enters the YOLO pipeline."""
    results: List[CheckResult] = []
    suffix = Path(filename or "").suffix.lower()
    normalized_extensions = {extension.lower() for extension in allowed_extensions}
    normalized_mime_types = {mime.lower() for mime in allowed_mime_types}

    if not filename:
        results.append(
            CheckResult(
                name="upload_filename",
                level=CheckLevel.ERROR,
                message="Uploaded file must include a filename.",
            )
        )
    elif suffix not in normalized_extensions:
        results.append(
            CheckResult(
                name="upload_extension",
                level=CheckLevel.ERROR,
                message=(
                    f"Unsupported image extension '{suffix or '<none>'}'. "
                    f"Allowed: {sorted(normalized_extensions)}"
                ),
            )
        )
    else:
        results.append(
            CheckResult(
                name="upload_extension",
                level=CheckLevel.PASS,
                message=f"Image extension '{suffix}' is allowed.",
            )
        )

    if not content:
        results.append(
            CheckResult(
                name="upload_content",
                level=CheckLevel.ERROR,
                message="Uploaded image is empty.",
            )
        )
    else:
        results.append(
            CheckResult(
                name="upload_content",
                level=CheckLevel.PASS,
                message=f"Uploaded image size is {len(content)} bytes.",
            )
        )

    normalized_content_type = (content_type or "").lower().strip()
    if normalized_content_type and normalized_content_type not in normalized_mime_types:
        results.append(
            CheckResult(
                name="upload_mime_type",
                level=CheckLevel.ERROR,
                message=(
                    f"Unsupported MIME type '{normalized_content_type}'. "
                    f"Allowed: {sorted(normalized_mime_types)}"
                ),
            )
        )
    elif normalized_content_type:
        results.append(
            CheckResult(
                name="upload_mime_type",
                level=CheckLevel.PASS,
                message=f"MIME type '{normalized_content_type}' is allowed.",
            )
        )
    else:
        results.append(
            CheckResult(
                name="upload_mime_type",
                level=CheckLevel.WARNING,
                message="Upload MIME type is missing and could not be validated.",
            )
        )

    if content:
        image = cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            results.append(
                CheckResult(
                    name="upload_image_decode",
                    level=CheckLevel.ERROR,
                    message="Uploaded file could not be decoded as an image.",
                )
            )
        else:
            height, width = image.shape[:2]
            results.append(
                CheckResult(
                    name="upload_image_decode",
                    level=CheckLevel.PASS,
                    message=f"Image decoded successfully ({width}x{height}).",
                    details={"width": width, "height": height},
                )
            )

    return build_report(results)


def register_validator(
    name: str,
) -> Callable[[Callable[["DataValidator"], List[CheckResult]]], Callable[["DataValidator"], List[CheckResult]]]:
    def decorator(
        func: Callable[["DataValidator"], List[CheckResult]]
    ) -> Callable[["DataValidator"], List[CheckResult]]:
        VALIDATOR_REGISTRY[name] = func
        return func

    return decorator


def list_validators() -> List[str]:
    return sorted(VALIDATOR_REGISTRY)


class DataValidator:
    """Run composable validation rules against a YOLO dataset layout."""

    def __init__(self, context: CheckContext):
        self.context = context
        self._image_cache: Optional[List[Path]] = None
        self._label_cache: Optional[List[Path]] = None

    def _is_ignored(self, path: Path) -> bool:
        return path.name.lower() in self.context.ignored_names

    def _list_files(self, directory: Optional[Path], extensions: Set[str]) -> List[Path]:
        if directory is None or not directory.exists() or not directory.is_dir():
            return []
        return sorted(
            path
            for path in directory.iterdir()
            if path.is_file()
            and not self._is_ignored(path)
            and path.suffix.lower() in extensions
        )

    def image_files(self) -> List[Path]:
        if self._image_cache is None:
            self._image_cache = self._list_files(
                self.context.images_dir,
                self.context.normalized_image_extensions(),
            )
        return self._image_cache

    def label_files(self) -> List[Path]:
        if self._label_cache is None:
            self._label_cache = self._list_files(
                self.context.labels_dir,
                self.context.normalized_label_extensions(),
            )
        return self._label_cache

    def validate(self, selected: Optional[Sequence[str]] = None) -> ValidationReport:
        names = list(selected) if selected else list_validators()
        results: List[CheckResult] = []
        for name in names:
            validator = VALIDATOR_REGISTRY.get(name)
            if validator is None:
                results.append(
                    CheckResult(
                        name=name,
                        level=CheckLevel.ERROR,
                        message=f"Validator '{name}' is not registered.",
                    )
                )
                continue
            results.extend(validator(self))
        return ValidationReport(results=results)

    def validate_and_report(
        self,
        logger=None,
        selected: Optional[Sequence[str]] = None,
    ) -> bool:
        report = self.validate(selected=selected)
        if logger:
            emitters = {
                CheckLevel.PASS: logger.info,
                CheckLevel.INFO: logger.info,
                CheckLevel.WARNING: logger.warning,
                CheckLevel.ERROR: logger.error,
            }
            emit = logger.info
        else:
            emitters = {level: print for level in CheckLevel}
            emit = print

        emit("=" * 60)
        emit("YOLO dataset validation report")
        emit("=" * 60)
        for result in report.results:
            prefix = result.level.value.upper().rjust(7)
            emitters[result.level](f"[{prefix}] {result.name}: {result.message}")
        summary = report.summary()
        emit("-" * 60)
        emit(
            "Summary: total={total}, pass={pass_}, info={info}, warning={warning}, error={error}".format(
                total=summary["total"],
                pass_=summary["pass"],
                info=summary["info"],
                warning=summary["warning"],
                error=summary["error"],
            )
        )
        emit("-" * 60)
        return report.ok

    def _parse_label_line(self, label_path: Path, line_number: int, line: str) -> Tuple[int, List[float]]:
        parts = line.split()
        if len(parts) != 5:
            raise ValueError(
                f"{label_path.name}:{line_number} must contain 5 columns, got {len(parts)}."
            )
        try:
            class_id = int(parts[0])
        except ValueError as exc:
            raise ValueError(
                f"{label_path.name}:{line_number} has a non-integer class id."
            ) from exc
        try:
            bbox = [float(value) for value in parts[1:]]
        except ValueError as exc:
            raise ValueError(
                f"{label_path.name}:{line_number} has non-numeric bbox values."
            ) from exc
        return class_id, bbox

    def iter_label_entries(self):
        for label_path in self.label_files():
            text = label_path.read_text(encoding="utf-8").strip()
            if not text:
                yield label_path, None, None, None
                continue
            for line_number, line in enumerate(text.splitlines(), start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                class_id, bbox = self._parse_label_line(label_path, line_number, stripped)
                yield label_path, line_number, class_id, bbox


@register_validator("directories")
def validate_directories(validator: DataValidator) -> List[CheckResult]:
    results: List[CheckResult] = []
    for field_name, path in (
        ("train_root", validator.context.train_root),
        ("images_dir", validator.context.images_dir),
        ("labels_dir", validator.context.labels_dir),
    ):
        if path is None:
            results.append(
                CheckResult(
                    name="directories",
                    level=CheckLevel.ERROR,
                    message=f"{field_name} is not configured.",
                )
            )
        elif not path.exists():
            results.append(
                CheckResult(
                    name="directories",
                    level=CheckLevel.ERROR,
                    message=f"{field_name} does not exist: {path}",
                )
            )
        elif not path.is_dir():
            results.append(
                CheckResult(
                    name="directories",
                    level=CheckLevel.ERROR,
                    message=f"{field_name} is not a directory: {path}",
                )
            )
        else:
            results.append(
                CheckResult(
                    name="directories",
                    level=CheckLevel.PASS,
                    message=f"{field_name} is ready: {path}",
                )
            )
    return results


@register_validator("image_files")
def validate_image_files(validator: DataValidator) -> List[CheckResult]:
    image_files = validator.image_files()
    if not image_files:
        return [
            CheckResult(
                name="image_files",
                level=CheckLevel.ERROR,
                message="No image files were found.",
            )
        ]
    return [
        CheckResult(
            name="image_files",
            level=CheckLevel.PASS,
            message=f"Found {len(image_files)} image files.",
        )
    ]


@register_validator("label_files")
def validate_label_files(validator: DataValidator) -> List[CheckResult]:
    label_files = validator.label_files()
    if not label_files:
        return [
            CheckResult(
                name="label_files",
                level=CheckLevel.ERROR,
                message="No label files were found.",
            )
        ]
    return [
        CheckResult(
            name="label_files",
            level=CheckLevel.PASS,
            message=f"Found {len(label_files)} label files.",
        )
    ]


@register_validator("image_label_match")
def validate_image_label_match(validator: DataValidator) -> List[CheckResult]:
    image_stems = {path.stem for path in validator.image_files()}
    label_stems = {path.stem for path in validator.label_files()}

    missing_labels = sorted(image_stems - label_stems)
    extra_labels = sorted(label_stems - image_stems)
    results: List[CheckResult] = []

    if missing_labels:
        results.append(
            CheckResult(
                name="image_label_match",
                level=CheckLevel.ERROR,
                message=f"{len(missing_labels)} images do not have matching labels.",
                details={"missing_labels": missing_labels[:20]},
            )
        )

    if extra_labels:
        results.append(
            CheckResult(
                name="image_label_match",
                level=CheckLevel.ERROR,
                message=f"{len(extra_labels)} labels do not have matching images.",
                details={"extra_labels": extra_labels[:20]},
            )
        )

    if not results:
        results.append(
            CheckResult(
                name="image_label_match",
                level=CheckLevel.PASS,
                message="Every image has a matching label and no extra labels were found.",
            )
        )
    return results


@register_validator("yolo_label_format")
def validate_yolo_label_format(validator: DataValidator) -> List[CheckResult]:
    results: List[CheckResult] = []
    empty_files: List[str] = []
    for label_path, line_number, _, _ in validator.iter_label_entries():
        if line_number is None:
            empty_files.append(label_path.name)
            continue
    for label_path in validator.label_files():
        lines = label_path.read_text(encoding="utf-8").splitlines()
        for line_number, raw_line in enumerate(lines, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                validator._parse_label_line(label_path, line_number, stripped)
            except ValueError as exc:
                results.append(
                    CheckResult(
                        name="yolo_label_format",
                        level=CheckLevel.ERROR,
                        message=str(exc),
                    )
                )
    if empty_files:
        results.append(
            CheckResult(
                name="yolo_label_format",
                level=CheckLevel.WARNING,
                message=f"{len(empty_files)} label files are empty.",
                details={"empty_labels": empty_files[:20]},
            )
        )
    if not results:
        results.append(
            CheckResult(
                name="yolo_label_format",
                level=CheckLevel.PASS,
                message="All YOLO label files use the expected 5-column format.",
            )
        )
    return results


@register_validator("class_id_validation")
def validate_class_ids(validator: DataValidator) -> List[CheckResult]:
    class_ids: Set[int] = set()
    invalid: List[str] = []
    has_class_config = bool(validator.context.classes)
    max_allowed = len(validator.context.classes) - 1 if has_class_config else None

    for label_path in validator.label_files():
        for line_number, raw_line in enumerate(label_path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                class_id, _ = validator._parse_label_line(label_path, line_number, stripped)
            except ValueError:
                continue
            class_ids.add(class_id)
            if class_id < 0:
                invalid.append(f"{label_path.name}:{line_number} has a negative class id.")
            elif max_allowed is not None and class_id > max_allowed:
                invalid.append(
                    f"{label_path.name}:{line_number} exceeds allowed class id range 0..{max_allowed}."
                )

    results = [
        CheckResult(
            name="class_id_validation",
            level=CheckLevel.INFO,
            message=f"Discovered class ids: {sorted(class_ids)}",
            details={"class_ids": sorted(class_ids)},
        )
    ]
    if invalid:
        results.append(
            CheckResult(
                name="class_id_validation",
                level=CheckLevel.ERROR,
                message=f"Found {len(invalid)} invalid class id entries.",
                details={"examples": invalid[:20]},
            )
        )
    elif not has_class_config:
        results.append(
            CheckResult(
                name="class_id_validation",
                level=CheckLevel.INFO,
                message=(
                    "No class list is configured, so only negative class ids were checked. "
                    "Upper-bound class id validation was skipped."
                ),
            )
        )
    else:
        results.append(
            CheckResult(
                name="class_id_validation",
                level=CheckLevel.PASS,
                message="All class ids are valid for the configured dataset.",
            )
        )
    return results


@register_validator("yolo_bbox_range")
def validate_yolo_bbox_range(validator: DataValidator) -> List[CheckResult]:
    invalid: List[str] = []
    for label_path in validator.label_files():
        for line_number, raw_line in enumerate(label_path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                _, bbox = validator._parse_label_line(label_path, line_number, stripped)
            except ValueError:
                continue
            x_center, y_center, width, height = bbox
            if not (0.0 <= x_center <= 1.0 and 0.0 <= y_center <= 1.0):
                invalid.append(f"{label_path.name}:{line_number} has center values outside 0..1.")
            if not (0.0 < width <= 1.0 and 0.0 < height <= 1.0):
                invalid.append(f"{label_path.name}:{line_number} has width/height outside 0..1.")
    if invalid:
        return [
            CheckResult(
                name="yolo_bbox_range",
                level=CheckLevel.ERROR,
                message=f"Found {len(invalid)} bbox values outside the normalized 0..1 range.",
                details={"examples": invalid[:20]},
            )
        ]
    return [
        CheckResult(
            name="yolo_bbox_range",
            level=CheckLevel.PASS,
            message="All YOLO bbox values are normalized to the expected range.",
        )
    ]


@register_validator("dataset_stats")
def collect_dataset_stats(validator: DataValidator) -> List[CheckResult]:
    image_count = len(validator.image_files())
    label_count = len(validator.label_files())
    matched = len(
        {path.stem for path in validator.image_files()}
        & {path.stem for path in validator.label_files()}
    )
    non_empty_labels = 0
    total_boxes = 0
    class_ids: Set[int] = set()

    for label_path in validator.label_files():
        lines = [line.strip() for line in label_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if lines:
            non_empty_labels += 1
        for line_number, line in enumerate(lines, start=1):
            try:
                class_id, _ = validator._parse_label_line(label_path, line_number, line)
            except ValueError:
                continue
            class_ids.add(class_id)
            total_boxes += 1

    return [
        CheckResult(
            name="dataset_stats",
            level=CheckLevel.INFO,
            message=(
                f"images={image_count}, labels={label_count}, matched={matched}, "
                f"boxes={total_boxes}, non_empty_labels={non_empty_labels}, "
                f"class_ids={sorted(class_ids)}"
            ),
            details={
                "images": image_count,
                "labels": label_count,
                "matched": matched,
                "boxes": total_boxes,
                "non_empty_labels": non_empty_labels,
                "class_ids": sorted(class_ids),
            },
        )
    ]
