#!/usr/bin/env python3
"""Scan public-site inputs for obvious secrets and private infrastructure data."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import re
import shutil
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".md",
    ".yml",
    ".yaml",
    ".json",
    ".csv",
    ".txt",
    ".js",
    ".css",
    ".html",
    ".py",
    ".sh",
    ".toml",
}
IGNORED_PARTS = {
    ".git",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    "artifacts",
    "node_modules",
    "output",
    "site",
    "tmp",
}
IGNORED_FILES = {"package-lock.json", "uv.lock"}

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "secret assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|token|password|client[_-]?secret)\s*[:=]\s*['\"]?([^\s'\"<{][^\s'\"]{7,})"
    ),
    "absolute user path": re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    "known production host": re.compile(r"(?i)flowise\.lute-tlz-dddd\.top"),
    "UUID": re.compile(
        r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
    ),
}
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
IPV4_RE = re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])")

# Screenshot OCR is deliberately implemented with the system Tesseract binary
# instead of an optional Python wrapper.  Release validation must fail closed
# when either the engine or the Chinese/English language data is absent.
OCR_LANGUAGES = ("chi_sim", "eng")
OCR_PSM = "11"
SCREENSHOT_SOURCE_ROOT = ROOT / "data" / "screenshots" / "source"
SCREENSHOT_PUBLIC_ROOT = ROOT / "docs" / "assets" / "screenshots"
IMAGE_SUFFIXES = {".png", ".webp"}

IMAGE_SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Bearer token": re.compile(r"(?i)\bbearer[:=]?[A-Za-z0-9._~+/=-]{12,}\b"),
    "credential value": re.compile(
        r"(?i)\b(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token|token|password|"
        r"client[_ -]?secret|authorization|cookie|set-cookie)\s*[:=]\s*"
        r"(?:bearer\s+)?([^\s'\"<{][^\s'\"]{7,})"
    ),
    "absolute user path": re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/"),
    "known production host": re.compile(r"(?i)flowise\.lute-tlz-dddd\.top"),
    "internal domain": re.compile(
        r"(?i)\b(?:[a-z0-9-]+\.)+(?:internal|intranet|corp|lan|local)\b"
    ),
    "UUID": re.compile(
        r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
        r"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
    ),
}

# Screenshots are documentary evidence, not general-purpose image assets. No
# author-supplied metadata is necessary to render them. The only allowlisted
# entries are fixed-type scalar fields emitted by Pillow/libwebp for a plain
# static WebP. This rejects PNG tEXt/iTXt and WebP EXIF/XMP/ICC/comment payloads
# (including unknown future keys) instead of maintaining a fragile denylist.
ALLOWED_IMAGE_METADATA_KEYS: dict[str, frozenset[str]] = {
    "PNG": frozenset(),
    # Pillow/libwebp exposes these decoder-generated scalar fields even for a
    # plain static WebP. They cannot carry arbitrary text or binary profiles.
    "WEBP": frozenset({"loop", "background", "timestamp", "duration"}),
}


class OCRUnavailable(RuntimeError):
    """Raised when screenshots cannot be inspected with the fixed OCR contract."""


def _looks_redacted(value: str) -> bool:
    compact = re.sub(r"\s+", "", value).strip(".,;:，。；：")
    lowered = compact.lower()
    if lowered in {
        "redacted",
        "masked",
        "hidden",
        "已脱敏",
        "已遮罩",
        "已隐藏",
    }:
        return True
    return bool(compact) and all(character in "*•●·xX#-—_" for character in compact)


def image_ruleset_sha256() -> str:
    """Return a stable digest so receipts are invalidated when rules change."""

    material = [
        "image-secret-rules-v2",
        "ocr-token-normalization-v1",
        "email-allowlist-v1",
        "private-ip-v1",
        "static-image-metadata-allowlist-v2",
        "webp-render-scalar-types-v1",
    ]
    material.extend(
        f"{label}:{pattern.pattern}" for label, pattern in sorted(IMAGE_SECRET_PATTERNS.items())
    )
    material.extend(
        f"metadata:{image_format}:{','.join(sorted(keys))}"
        for image_format, keys in sorted(ALLOWED_IMAGE_METADATA_KEYS.items())
    )
    return hashlib.sha256("\n".join(material).encode("utf-8")).hexdigest()


@lru_cache(maxsize=1)
def ocr_engine_info() -> dict[str, Any]:
    executable = shutil.which("tesseract")
    if not executable:
        raise OCRUnavailable("tesseract executable is unavailable")
    version_result = subprocess.run(
        [executable, "--version"],
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )
    if version_result.returncode != 0 or not version_result.stdout.strip():
        raise OCRUnavailable("tesseract version probe failed")
    version = version_result.stdout.splitlines()[0].strip()
    languages_result = subprocess.run(
        [executable, "--list-langs"],
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )
    if languages_result.returncode != 0:
        raise OCRUnavailable("tesseract language probe failed")
    installed = {
        line.strip()
        for line in languages_result.stdout.splitlines()
        if line.strip() and not line.lower().startswith("list of available languages")
    }
    missing = sorted(set(OCR_LANGUAGES) - installed)
    if missing:
        raise OCRUnavailable(
            "required tesseract language data is unavailable: " + ", ".join(missing)
        )
    return {
        "executable": executable,
        "engine": "tesseract",
        "version": version,
        "languages": list(OCR_LANGUAGES),
        "psm": OCR_PSM,
    }


def normalize_ocr_text(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.replace("\r\n", "\n").split("\n")).strip()


def _ocr_scan_variants(line: str) -> tuple[str, ...]:
    """Return safe OCR normalizations without exposing reconstructed values.

    Tesseract commonly inserts spaces or punctuation between individual ASCII
    glyphs (for example ``a d m i n @ corp . test`` or a split UUID).  Scanning
    only the raw OCR line lets those artifacts bypass otherwise sound regular
    expressions.  The variants retain structural characters used by email,
    URL, UUID and key formats while removing common OCR separator noise.
    """

    compact_space = re.sub(r"\s+", "", line)
    compact_noise = re.sub(
        r"[\s,，;；'\"`|!！?？()（）\[\]{}<>《》]+",
        "",
        line,
    )
    ascii_signal = re.sub(r"[^A-Za-z0-9@._%+:/=\-]+", "", line)
    return tuple(dict.fromkeys((line, compact_space, compact_noise, ascii_signal)))


def _metadata_value_text(value: Any) -> str:
    """Extract bounded textual metadata for secret classification only."""

    if isinstance(value, str):
        return value[:65536]
    if isinstance(value, bytes):
        return value[:65536].decode("utf-8", errors="ignore")
    if isinstance(value, (list, tuple)):
        return "\n".join(_metadata_value_text(item) for item in value)[:65536]
    if isinstance(value, dict):
        return "\n".join(
            f"{_metadata_value_text(key)}:{_metadata_value_text(item)}"
            for key, item in value.items()
        )[:65536]
    return ""


def _allowed_metadata_value_is_safe(image_format: str, key: str, value: Any) -> bool:
    if image_format != "WEBP":
        return False
    if key in {"loop", "timestamp", "duration"}:
        return isinstance(value, int) and not isinstance(value, bool) and value >= 0
    if key == "background":
        return (
            isinstance(value, tuple)
            and len(value) == 4
            and all(
                isinstance(channel, int)
                and not isinstance(channel, bool)
                and 0 <= channel <= 255
                for channel in value
            )
        )
    return False


def scan_image_metadata(path: Path) -> list[dict[str, object]]:
    """Reject nonessential image metadata and scan any textual payload.

    Findings contain only the evidence path and a rule class; neither metadata
    keys nor values are returned because either may themselves be sensitive.
    """

    relative = str(path.relative_to(ROOT))
    findings: list[dict[str, object]] = []
    with Image.open(path) as image:
        image.load()
        image_format = str(image.format or "").upper()
        allowed = ALLOWED_IMAGE_METADATA_KEYS.get(image_format, frozenset())
        if image.getexif():
            findings.append({"file": relative, "line": 0, "kind": "image EXIF metadata"})
        for key, value in image.info.items():
            normalized_key = str(key).casefold()
            if normalized_key not in allowed or not _allowed_metadata_value_is_safe(
                image_format, normalized_key, value
            ):
                findings.append(
                    {"file": relative, "line": 0, "kind": "image nonessential metadata"}
                )
            metadata_text = _metadata_value_text({key: value})
            for finding in scan_ocr_text(metadata_text, relative):
                findings.append(
                    {
                        "file": relative,
                        "line": 0,
                        "kind": str(finding["kind"]).replace("image OCR", "image metadata"),
                    }
                )
    # A single metadata field can be exposed through multiple Pillow aliases.
    # Keep reports concise while retaining every distinct risk class.
    unique: dict[tuple[object, object, object], dict[str, object]] = {}
    for finding in findings:
        key = (finding.get("file"), finding.get("line"), finding.get("kind"))
        unique[key] = finding
    return list(unique.values())


def extract_image_text(path: Path) -> tuple[str, dict[str, Any]]:
    info = ocr_engine_info()
    environment = os.environ.copy()
    environment.setdefault("OMP_THREAD_LIMIT", "1")
    result = subprocess.run(
        [
            str(info["executable"]),
            str(path),
            "stdout",
            "-l",
            "+".join(OCR_LANGUAGES),
            "--psm",
            OCR_PSM,
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
        env=environment,
    )
    if result.returncode != 0:
        raise OCRUnavailable(f"tesseract failed for {path.name} with exit {result.returncode}")
    return normalize_ocr_text(result.stdout), info


def scan_ocr_text(text: str, relative: str) -> list[dict[str, object]]:
    """Scan OCR output without ever returning the matched sensitive value."""

    findings: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for variant in _ocr_scan_variants(line):
            for label, pattern in IMAGE_SECRET_PATTERNS.items():
                for match in pattern.finditer(variant):
                    if label == "credential value" and _looks_redacted(match.group(1)):
                        continue
                    findings.append(
                        {
                            "file": relative,
                            "line": line_number,
                            "kind": f"image OCR {label}",
                        }
                    )
            for match in EMAIL_RE.finditer(variant):
                domain = match.group(1).lower()
                if domain not in {
                    "example.com",
                    "example.org",
                    "example.net",
                    "training.invalid",
                }:
                    findings.append(
                        {"file": relative, "line": line_number, "kind": "image OCR email"}
                    )
            for match in IPV4_RE.finditer(variant):
                try:
                    address = ipaddress.ip_address(match.group(0))
                except ValueError:
                    continue
                if (
                    address.is_private
                    and not address.is_loopback
                    and not address.is_unspecified
                ) or address.is_link_local:
                    findings.append(
                        {
                            "file": relative,
                            "line": line_number,
                            "kind": "image OCR private IP",
                        }
                    )
    unique: dict[tuple[object, object, object], dict[str, object]] = {}
    for finding in findings:
        key = (finding.get("file"), finding.get("line"), finding.get("kind"))
        unique[key] = finding
    return list(unique.values())


def scan_image(path: Path) -> tuple[dict[str, Any], list[dict[str, object]]]:
    relative = str(path.relative_to(ROOT))
    metadata_findings = scan_image_metadata(path)
    text, info = extract_image_text(path)
    evidence = {
        "engine": info["engine"],
        "engine_version": info["version"],
        "languages": info["languages"],
        "psm": info["psm"],
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "character_count": len(text),
        "ruleset_sha256": image_ruleset_sha256(),
    }
    return evidence, metadata_findings + scan_ocr_text(text, relative)


def iter_screenshot_images() -> list[Path]:
    paths: list[Path] = []
    for root in (SCREENSHOT_SOURCE_ROOT, SCREENSHOT_PUBLIC_ROOT):
        if not root.exists():
            continue
        paths.extend(
            path
            for path in root.rglob("*")
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
        )
    return sorted(paths)


def iter_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix in TEXT_SUFFIXES
        and path.name not in IGNORED_FILES
        and not any(part in IGNORED_PARTS for part in path.relative_to(ROOT).parts)
        and "assets/vendor" not in path.as_posix()
    )


def scan_text(text: str, relative: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                findings.append({"file": relative, "line": line_number, "kind": label})
        for match in EMAIL_RE.finditer(line):
            domain = match.group(1).lower()
            if domain not in {"example.com", "example.org", "example.net", "training.invalid"}:
                findings.append({"file": relative, "line": line_number, "kind": "email"})
        for match in IPV4_RE.finditer(line):
            try:
                address = ipaddress.ip_address(match.group(0))
            except ValueError:
                continue
            # Literal loopback is an intentional safety property of the bundled
            # mock API. Other private/link-local addresses can reveal topology.
            if (
                address.is_private
                and not address.is_loopback
                and not address.is_unspecified
            ) or address.is_link_local:
                findings.append({"file": relative, "line": line_number, "kind": "private IP"})
    return findings


def scan_file(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return scan_text(text, str(path.relative_to(ROOT)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--release",
        action="store_true",
        default=os.getenv("PLAYBOOK_RELEASE_MODE") == "1",
    )
    args = parser.parse_args()
    findings = [item for path in iter_files() for item in scan_file(path)]
    image_paths = iter_screenshot_images()
    for path in image_paths:
        try:
            _, image_findings = scan_image(path)
            findings.extend(image_findings)
        except OCRUnavailable:
            # Do not include executable paths or OCR stderr in the public report.
            # Any checked-in screenshot without a reproducible OCR scan is unsafe.
            findings.append(
                {
                    "file": str(path.relative_to(ROOT)),
                    "line": 0,
                    "kind": "image OCR unavailable",
                }
            )
    if args.json:
        print(
            json.dumps(
                {
                    "findings": findings,
                    "images_scanned": len(image_paths),
                    "release_mode": args.release,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for item in findings:
            print(f"ERROR: {item['file']}:{item['line']}: {item['kind']}", file=sys.stderr)
        print(
            f"public-safety scan: {len(findings)} finding(s), "
            f"{len(image_paths)} screenshot image(s) OCR-scanned"
        )
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
