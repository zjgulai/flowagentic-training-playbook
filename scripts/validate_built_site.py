#!/usr/bin/env python3
"""Validate the packaged static site after PDF injection."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def _attribute_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return " ".join(str(item) for item in value)
    return ""


def _output_page(site: Path, doc_path: str) -> Path:
    relative = Path(doc_path).relative_to("docs")
    if relative.name == "index.md":
        return site / relative.parent / "index.html"
    return site / relative.with_suffix("") / "index.html"


def validate_release_screenshot_html(site: Path) -> list[str]:
    """Ensure the final HTML, not only frontmatter, contains every screenshot."""

    payload = yaml.safe_load(
        (ROOT / "data/manifests/screenshots.yml").read_text(encoding="utf-8")
    )
    items = payload.get("screenshots", []) if isinstance(payload, dict) else []
    by_doc: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in items:
        if isinstance(item, dict):
            by_doc[str(item.get("doc_path", ""))].append(item)
    errors: list[str] = []
    for doc_path, expected_items in sorted(by_doc.items()):
        page = _output_page(site, doc_path)
        if not page.is_file():
            errors.append(f"release screenshot page is missing: {doc_path}")
            continue
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        images = soup.find_all("img", attrs={"data-screenshot-id": True})
        actual: dict[str, Tag] = {}
        duplicates: set[str] = set()
        for image in images:
            identifier = _attribute_text(image.get("data-screenshot-id"))
            if identifier in actual:
                duplicates.add(identifier)
            actual[identifier] = image
        expected = {str(item.get("id", "")): item for item in expected_items}
        if set(actual) != set(expected):
            errors.append(f"release screenshot HTML ids do not match manifest: {doc_path}")
        if duplicates:
            errors.append(f"release screenshot HTML contains duplicate ids: {doc_path}")
        for identifier in sorted(set(actual) & set(expected)):
            image = actual[identifier]
            item = expected[identifier]
            src = _attribute_text(image.get("src"))
            parsed = urlsplit(src)
            if parsed.scheme or parsed.netloc or not parsed.path:
                errors.append(f"release screenshot HTML source is not local: {identifier}")
                continue
            resolved = (page.parent / unquote(parsed.path)).resolve()
            annotated = str(item.get("annotated_file", ""))
            try:
                public_relative = Path(annotated).relative_to("docs")
            except ValueError:
                errors.append(f"release screenshot manifest path is invalid: {identifier}")
                continue
            expected_path = (site / public_relative).resolve()
            if resolved != expected_path or not expected_path.is_file():
                errors.append(f"release screenshot HTML source mismatch: {identifier}")
            if _attribute_text(image.get("alt")).strip() != str(item.get("alt_text", "")).strip():
                errors.append(f"release screenshot HTML alt mismatch: {identifier}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, default=SITE)
    args = parser.parse_args()
    site = args.site_dir.resolve()
    errors: list[str] = []
    required = {
        "homepage": site / "index.html",
        "404": site / "404.html",
        "search": site / "search" / "search_index.json",
        "PDF": site / "assets" / "downloads" / "flowagentic-playbook.pdf",
    }
    for label, path in required.items():
        if not path.is_file():
            try:
                display_path = path.relative_to(ROOT)
            except ValueError:
                display_path = path
            errors.append(f"missing {label}: {display_path}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    homepage = BeautifulSoup(required["homepage"].read_text(encoding="utf-8"), "html.parser")
    if "FlowAgentic 培训与操作 Playbook" not in homepage.get_text(" ", strip=True):
        errors.append("homepage title is missing")
    pdf_links = [
        link
        for link in homepage.find_all("a", href=True)
        if _attribute_text(link.get("href")).endswith("flowagentic-playbook.pdf")
    ]
    if not pdf_links:
        errors.append("homepage does not expose the PDF download")
    runtime_config = homepage.find("script", id="__config")
    if not runtime_config:
        errors.append("homepage is missing Material runtime configuration")
    else:
        try:
            config = json.loads(runtime_config.get_text())
        except json.JSONDecodeError:
            errors.append("Material runtime configuration is invalid JSON")
        else:
            version = config.get("version", {})
            release_mode = os.getenv("PLAYBOOK_RELEASE_MODE") == "1"
            if release_mode:
                if version.get("provider") != "mike" or version.get("default") != "latest":
                    errors.append("mike version switcher is not configured for latest")
            elif version.get("provider") not in {None, ""}:
                errors.append("draft site must not request a missing mike versions index")

    not_found = BeautifulSoup(required["404"].read_text(encoding="utf-8"), "html.parser")
    not_found_text = not_found.get_text(" ", strip=True)
    if "页面未找到" not in not_found_text or "返回 Playbook 首页" not in not_found_text:
        errors.append("404 page is not the Chinese recovery page")

    search = json.loads(required["search"].read_text(encoding="utf-8"))
    search_docs = search.get("docs", [])
    if len(search_docs) < 600:
        errors.append(f"search index is unexpectedly small: {len(search_docs)} entries")
    search_blob = "\n".join(
        f"{item.get('title', '')}\n{item.get('text', '')}" for item in search_docs
    )
    catalog = json.loads((ROOT / "data" / "catalog" / "nodes.json").read_text(encoding="utf-8"))
    missing_nodes = [
        node["name"] for node in catalog["nodes"] if node["name"] not in search_blob
    ]
    if missing_nodes:
        errors.append(
            f"search index misses {len(missing_nodes)} node names; "
            f"examples: {', '.join(missing_nodes[:5])}"
        )
    node_pages = list((site / "19-reference" / "node-catalog").rglob("index.html"))
    if len(node_pages) != 27:
        errors.append(f"expected 27 node catalog pages, found {len(node_pages)}")

    pdf = required["PDF"]
    if pdf.read_bytes()[:5] != b"%PDF-":
        errors.append("site PDF download is not a PDF file")
    if pdf.stat().st_size < 100_000:
        errors.append("site PDF download is unexpectedly small")

    for path in site.rglob("*"):
        if not path.is_file():
            continue
        if path.stat().st_size < 200:
            prefix = path.read_bytes()[:120]
            if prefix.startswith(b"version https://git-lfs.github.com/spec/v1"):
                errors.append(f"Git LFS pointer leaked into site: {path.relative_to(site)}")

    if os.getenv("PLAYBOOK_RELEASE_MODE") == "1":
        errors.extend(validate_release_screenshot_html(site))

    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(
        f"built site: {len(search_docs)} search entries, "
        f"{len(node_pages)} node pages, {len(errors)} error(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
