#!/usr/bin/env python3
"""Validate the generated Chinese PDF before visual page inspection."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader
import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "output" / "pdf" / "flowagentic-playbook.pdf"
REQUIRED_SECTIONS = (
    "产品定位与学习路径",
    "系统认知",
    "登录、导航与账户",
    "凭据完整 SOP",
    "核心节点与执行模型",
    "执行记录与调试",
    "自定义助手",
    "模板市场",
    "Tools 与 MCP",
    "检索质量评估",
    "API、Embed 与 SDK",
    "贯穿实验",
    "优化方法",
    "标准诊断流程",
    "架构与扩展",
    "运维原则",
    "受限与实验能力附录",
    "课程路径",
    "参考入口",
)


def embeds_noto_sans_cjk(font_names: list[str]) -> bool:
    """Accept the equivalent PostScript spellings emitted by PDF generators."""

    return any(
        "notosanscjk" in re.sub(r"[^a-z0-9]", "", name.casefold())
        for name in font_names
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="?", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--render-sample", action="store_true")
    parser.add_argument("--require-noto", action="store_true")
    args = parser.parse_args()
    path = args.pdf.resolve()
    errors: list[str] = []
    if not path.is_file():
        print(f"ERROR: PDF does not exist: {path}", file=sys.stderr)
        return 1

    reader = PdfReader(str(path))
    if len(reader.pages) < 5:
        errors.append(f"unexpectedly short PDF: {len(reader.pages)} pages")
    title = (reader.metadata or {}).get("/Title", "")
    if "FlowAgentic" not in title:
        errors.append("PDF metadata title does not identify FlowAgentic")
    external_uris: list[str] = []
    for page_number, page in enumerate(reader.pages, start=1):
        for annotation_ref in page.get("/Annots", []):
            annotation = annotation_ref.get_object()
            action = annotation.get("/A")
            if not action:
                continue
            uri = action.get("/URI")
            if not uri:
                continue
            uri_text = str(uri)
            external_uris.append(uri_text)
            if uri_text.startswith("file:") or "://playbook.invalid" in uri_text:
                errors.append(
                    f"page {page_number} contains a local-only link: {uri_text[:120]}"
                )

    extracted: list[str] = []
    blank_pages: list[int] = []
    with pdfplumber.open(path) as document:
        for index, page in enumerate(document.pages):
            text = page.extract_text() or ""
            extracted.append(text)
            if len(re.sub(r"\s+", "", text)) < 5:
                blank_pages.append(index + 1)
            if "\ufffd" in text:
                errors.append(f"page {index + 1} contains replacement glyphs")
            if page.width <= 0 or page.height <= 0:
                errors.append(f"page {index + 1} has invalid dimensions")
    joined = "\n".join(extracted)
    compact = re.sub(r"\s+", "", joined)
    if len(re.findall(r"[\u4e00-\u9fff]", joined)) < 100:
        errors.append("too little extractable Chinese text; fonts may not be embedded correctly")
    for required in ("FlowAgentic", "版本", "参考"):
        if required not in joined:
            errors.append(f"required text is missing: {required}")
    if blank_pages:
        errors.append(f"PDF contains {len(blank_pages)} unexpectedly blank page(s)")
    for section in REQUIRED_SECTIONS:
        if section not in joined:
            errors.append(f"PDF section is missing: {section}")

    release = yaml.safe_load((ROOT / "data/release.yml").read_text(encoding="utf-8"))
    baseline = release.get("fact_baseline", {}) if isinstance(release, dict) else {}
    expected_version = str(baseline.get("product_version", ""))
    expected_sha = str(baseline.get("release_sha", ""))
    if expected_version not in joined:
        errors.append("PDF does not contain the fact-baseline product version")
    if expected_sha not in compact:
        errors.append("PDF does not contain the complete fact-baseline release SHA")

    fonts = subprocess.run(
        ["pdffonts", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if fonts.returncode != 0:
        errors.append("pdffonts could not inspect embedded fonts")
    else:
        font_rows = [line for line in fonts.stdout.splitlines()[2:] if line.strip()]
        if not font_rows:
            errors.append("PDF contains no inspectable fonts")
        font_names: list[str] = []
        for row in font_rows:
            font_names.append(row.split()[0])
            flags = re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", row)
            if not flags or flags.group(1) != "yes":
                errors.append("PDF contains a font that is not embedded")
        require_noto = args.require_noto or os.getenv("PLAYBOOK_RELEASE_MODE") == "1"
        if require_noto and not embeds_noto_sans_cjk(font_names):
            errors.append("PDF does not embed the required Noto Sans CJK font")

    if os.getenv("PLAYBOOK_RELEASE_MODE") == "1":
        manifest = yaml.safe_load(
            (ROOT / "data/manifests/screenshots.yml").read_text(encoding="utf-8")
        )
        expected_images = len(manifest.get("screenshots", [])) if isinstance(manifest, dict) else 0
        image_objects = 0
        for page in reader.pages:
            resources = page.get("/Resources") or {}
            xobjects = resources.get("/XObject") if hasattr(resources, "get") else None
            get_object = getattr(xobjects, "get_object", None)
            if callable(get_object):
                xobjects = get_object()
            if not isinstance(xobjects, dict):
                continue
            for value in xobjects.values():
                obj = value.get_object() if hasattr(value, "get_object") else value
                if isinstance(obj, dict) and obj.get("/Subtype") == "/Image":
                    image_objects += 1
        if expected_images and image_objects < expected_images:
            errors.append("PDF contains fewer image objects than the screenshot manifest")

    if args.render_sample and not errors:
        output_dir = ROOT / "tmp" / "pdfs"
        output_dir.mkdir(parents=True, exist_ok=True)
        pages = sorted({1, max(1, len(reader.pages) // 2), len(reader.pages)})
        for page_number in pages:
            subprocess.run(
                [
                    "pdftoppm",
                    "-f",
                    str(page_number),
                    "-l",
                    str(page_number),
                    "-png",
                    "-r",
                    "120",
                    str(path),
                    str(output_dir / f"review-page-{page_number:04d}"),
                ],
                check=True,
            )
        print(f"rendered visual samples to {output_dir.relative_to(ROOT)}")

    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(
        f"PDF validation: {len(reader.pages)} page(s), "
        f"{len(external_uris)} URI link(s), {len(errors)} error(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
