#!/usr/bin/env python3
"""Scan final HTML/PDF artifacts with the same public-safety policy as sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from pypdf import PdfReader

try:
    from check_public_safety import scan_text
except ModuleNotFoundError:  # pragma: no cover - package import path
    from scripts.check_public_safety import scan_text


ROOT = Path(__file__).resolve().parents[1]
SITE_SUFFIXES = {".html", ".json", ".js", ".css", ".txt", ".xml"}


def _display(root: Path, path: Path, prefix: str) -> str:
    return f"{prefix}/{path.relative_to(root).as_posix()}"


def scan_site(site: Path) -> tuple[list[dict[str, object]], int]:
    findings: list[dict[str, object]] = []
    files = [
        path
        for path in site.rglob("*")
        if path.is_file() and path.suffix.lower() in SITE_SUFFIXES
    ]
    for path in sorted(files):
        text = path.read_text(encoding="utf-8", errors="replace")
        relative = path.relative_to(site).as_posix()
        current = scan_text(text, _display(site, path, "site"))
        # These immutable/generated dependency assets contain parser variables
        # such as ``token=`` and documentation-shaped addresses.  Their source
        # packages are separately digest/lock validated.  Keep high-confidence
        # secret and infrastructure rules, but suppress only the two contextual
        # patterns that cannot distinguish code tokens from credential values.
        dependency_asset = (
            relative.startswith("assets/vendor/")
            or relative.startswith("assets/javascripts/lunr/")
            or relative.startswith("assets/javascripts/workers/")
            or (
                relative.startswith("assets/javascripts/bundle.")
                and relative.endswith(".min.js")
            )
        )
        if dependency_asset:
            current = [
                item
                for item in current
                if item.get("kind") not in {"secret assignment", "email"}
            ]
        findings.extend(current)
    return findings, len(files)


def _resolved(value: Any) -> Any:
    return value.get_object() if hasattr(value, "get_object") else value


def scan_pdf(pdf: Path) -> tuple[list[dict[str, object]], int, int]:
    findings: list[dict[str, object]] = []
    reader = PdfReader(str(pdf), strict=True)
    display = "pdf/flowagentic-playbook.pdf"
    metadata_text = "\n".join(
        f"{key}:{value}" for key, value in (reader.metadata or {}).items()
    )
    findings.extend(scan_text(metadata_text, display))

    attachments = getattr(reader, "attachments", {})
    if attachments:
        findings.append({"file": display, "line": 0, "kind": "PDF embedded file"})

    link_count = 0
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        findings.extend(scan_text(text, f"{display}#page-{page_number}"))
        annotations = _resolved(page.get("/Annots", [])) or []
        for annotation_ref in annotations:
            annotation = _resolved(annotation_ref)
            if not isinstance(annotation, dict):
                continue
            action = _resolved(annotation.get("/A"))
            if not isinstance(action, dict) or "/URI" not in action:
                continue
            link_count += 1
            uri = str(action.get("/URI", ""))
            findings.extend(scan_text(uri, f"{display}#link-{link_count}"))
            parsed = urlsplit(uri)
            if parsed.scheme and parsed.scheme.lower() not in {"http", "https", "mailto"}:
                findings.append(
                    {"file": display, "line": 0, "kind": "unsafe PDF URI scheme"}
                )
    return findings, len(reader.pages), link_count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    site = args.site_dir.resolve()
    pdf = args.pdf.resolve()
    if not site.is_dir() or not pdf.is_file():
        print("ERROR: final site or PDF artifact is missing", file=sys.stderr)
        return 1

    findings, site_files = scan_site(site)
    pdf_findings, pdf_pages, pdf_links = scan_pdf(pdf)
    findings.extend(pdf_findings)
    receipt = {
        "schema_version": 1,
        "site_files_scanned": site_files,
        "pdf_pages_scanned": pdf_pages,
        "pdf_links_scanned": pdf_links,
        "site_tree_sha256": hashlib.sha256(
            "\n".join(
                f"{path.relative_to(site).as_posix()}:{hashlib.sha256(path.read_bytes()).hexdigest()}"
                for path in sorted(site.rglob("*"))
                if path.is_file()
            ).encode("utf-8")
        ).hexdigest(),
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "findings": len(findings),
        "status": "passed" if not findings else "failed",
    }
    if args.receipt:
        receipt_path = args.receipt.resolve()
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    for item in findings:
        print(f"ERROR: {item['file']}:{item['line']}: {item['kind']}", file=sys.stderr)
    print(
        f"artifact safety: {site_files} site files, {pdf_pages} PDF pages, "
        f"{pdf_links} PDF links, {len(findings)} finding(s)"
    )
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
