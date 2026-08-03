#!/usr/bin/env python3
"""Build one print-safe Chinese PDF from an already-built MkDocs site."""

from __future__ import annotations

import argparse
import base64
import binascii
import html
import mimetypes
import os
import posixpath
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, unquote_to_bytes, urljoin, urlparse, urlsplit
from urllib.request import url2pathname
from zoneinfo import ZoneInfo

import yaml
from bs4 import BeautifulSoup, Tag
from weasyprint import CSS, HTML

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "output/pdf/flowagentic-playbook.pdf"
DEFAULT_TMP_DIR = PROJECT_ROOT / "tmp/pdfs"
PUBLICATION_TIMEZONE = ZoneInfo("Asia/Shanghai")

ALLOWED_DATA_MIME_TYPES = frozenset(
    {
        "image/gif",
        "image/jpeg",
        "image/png",
        "image/svg+xml",
        "image/webp",
        "font/woff",
        "font/woff2",
    }
)
ALLOWED_FILE_MIME_TYPES = ALLOWED_DATA_MIME_TYPES
MAX_RESOURCE_BYTES = 16 * 1024 * 1024
DANGEROUS_HTML_TAGS = frozenset({"base", "embed", "iframe", "link", "object"})
DANGEROUS_SVG_TAGS = frozenset(
    {
        "animate",
        "animatemotion",
        "animatetransform",
        "base",
        "discard",
        "embed",
        "foreignobject",
        "iframe",
        "link",
        "object",
        "script",
        "set",
    }
)
SVG_URL_ATTRIBUTES = frozenset(
    {"base", "data", "href", "poster", "src"}
)
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE | re.DOTALL)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
CONFIG_ENV_KEY_RE = re.compile(r"^[A-Z][A-Z0-9_]{0,63}$")
ALLOWED_CONFIG_ENV_KEYS = frozenset({"PLAYBOOK_VERSION_PROVIDER"})


class ResourceSecurityError(ValueError):
    """A deliberately redacted error raised for an unsafe PDF resource."""


class MkDocsConfigLoader(yaml.SafeLoader):
    """Safe YAML loader that preserves MkDocs Python-name references as text."""


def construct_python_name(
    loader: MkDocsConfigLoader, suffix: str, node: yaml.Node
) -> str:
    del loader, node
    return suffix


MkDocsConfigLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:",
    construct_python_name,
)


def construct_environment_value(
    loader: MkDocsConfigLoader, node: yaml.Node
) -> str | None:
    """Resolve the small, public-safe subset of MkDocs ``!ENV`` we use.

    PDF generation parses the same configuration as MkDocs, but it must not
    become a generic environment-variable exfiltration primitive. Only the
    release workflow's non-secret version-provider switch is accepted.
    """

    if isinstance(node, yaml.SequenceNode):
        values = loader.construct_sequence(node, deep=True)
    elif isinstance(node, yaml.ScalarNode):
        values = [loader.construct_scalar(node)]
    else:
        raise yaml.constructor.ConstructorError(
            None, None, "!ENV must be a scalar or one/two-item sequence", node.start_mark
        )
    if not 1 <= len(values) <= 2 or not isinstance(values[0], str):
        raise yaml.constructor.ConstructorError(
            None, None, "!ENV must name one environment variable and optional default", node.start_mark
        )
    key = values[0]
    if not CONFIG_ENV_KEY_RE.fullmatch(key) or key not in ALLOWED_CONFIG_ENV_KEYS:
        raise yaml.constructor.ConstructorError(
            None, None, "!ENV variable is not allowlisted for PDF configuration", node.start_mark
        )
    default = values[1] if len(values) == 2 else None
    if default is not None and not isinstance(default, str):
        raise yaml.constructor.ConstructorError(
            None, None, "!ENV default must be a string or null", node.start_mark
        )
    return os.environ.get(key, default)


MkDocsConfigLoader.add_constructor("!ENV", construct_environment_value)


@dataclass(frozen=True)
class Page:
    index: int
    title: str
    source_path: Path
    html_path: Path
    web_path: str
    anchor: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从 MkDocs 构建结果生成 FlowAgentic 中文 PDF。"
    )
    parser.add_argument("--config", type=Path, default=PROJECT_ROOT / "mkdocs.yml")
    parser.add_argument("--site-dir", type=Path, default=PROJECT_ROOT / "site")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--tmp-dir", type=Path, default=DEFAULT_TMP_DIR)
    parser.add_argument("--require-noto", action="store_true")
    return parser.parse_args()


def fail(message: str) -> int:
    print(f"PDF 构建失败：{message}", file=sys.stderr)
    return 1


def _rejected(reason: str) -> ResourceSecurityError:
    """Return a security error that never includes attacker-controlled URL text."""

    return ResourceSecurityError(f"PDF 资源安全校验拒绝：{reason}")


def _check_resource_size(payload: bytes) -> None:
    if len(payload) > MAX_RESOURCE_BYTES:
        raise _rejected("资源超过尺寸上限")


def _validate_embedded_reference(value: str, *, svg_depth: int) -> None:
    reference = value.strip()
    if not reference or reference.startswith("#"):
        return
    if reference.casefold().startswith("data:"):
        _decode_data_uri(reference, svg_depth=svg_depth + 1)
        return
    raise _rejected("SVG 包含外部资源引用")


def _validate_css_references(value: str, *, svg_depth: int) -> None:
    normalized = CSS_COMMENT_RE.sub("", value).casefold()
    if "\\" in normalized:
        raise _rejected("CSS 包含转义资源语法")
    if "@" in normalized:
        raise _rejected("CSS 包含禁止的 at-rule")
    matches = list(CSS_URL_RE.finditer(normalized))
    for match in matches:
        _validate_embedded_reference(match.group(2), svg_depth=svg_depth)
    residual = CSS_URL_RE.sub("", normalized)
    if any(
        marker in residual
        for marker in (
            "expression(",
            "ftp:",
            "gopher:",
            "http:",
            "https:",
            "javascript:",
            "file:",
        )
    ):
        raise _rejected("CSS 包含禁止的协议或表达式")


def _validate_svg(payload: bytes, *, svg_depth: int = 0) -> None:
    """Reject active SVG content and every non-inline resource reference."""

    if svg_depth > 2:
        raise _rejected("SVG data URI 嵌套过深")
    _check_resource_size(payload)
    try:
        svg_text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _rejected("SVG 必须使用 UTF-8 编码") from exc
    lowered = svg_text.casefold()
    if "<!doctype" in lowered or "<!entity" in lowered:
        raise _rejected("SVG 包含 DTD 或实体声明")
    if "<?xml-stylesheet" in lowered:
        raise _rejected("SVG 包含外部样式处理指令")
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        raise _rejected("SVG 不是有效 XML") from exc

    for element_count, element in enumerate(root.iter(), start=1):
        if element_count > 50_000:
            raise _rejected("SVG 元素数量超过上限")
        tag_name = str(element.tag).rsplit("}", 1)[-1].casefold()
        if tag_name in DANGEROUS_SVG_TAGS:
            raise _rejected(f"SVG 包含危险元素 {tag_name}")
        if tag_name == "style" and element.text:
            _validate_css_references(element.text, svg_depth=svg_depth)
        for raw_name, raw_value in element.attrib.items():
            name = str(raw_name).rsplit("}", 1)[-1].casefold()
            value = str(raw_value)
            if name.startswith("on"):
                raise _rejected("SVG 包含事件处理属性")
            if name in SVG_URL_ATTRIBUTES:
                _validate_embedded_reference(value, svg_depth=svg_depth)
            if name == "style" or "url(" in value.casefold():
                _validate_css_references(value, svg_depth=svg_depth)


def _decode_data_uri(url: str, *, svg_depth: int = 0) -> tuple[bytes, str]:
    """Decode a small allowlisted data URI without delegating to network code."""

    if len(url) > (MAX_RESOURCE_BYTES * 2):
        raise _rejected("data URI 超过尺寸上限")
    header, separator, encoded = url.partition(",")
    if not separator or not header.casefold().startswith("data:"):
        raise _rejected("data URI 格式无效")
    metadata = header[5:].split(";")
    mime_type = (metadata[0] or "text/plain").casefold()
    if mime_type not in ALLOWED_DATA_MIME_TYPES:
        raise _rejected("data URI 媒体类型不在允许清单")

    is_base64 = False
    for parameter in metadata[1:]:
        normalized = parameter.strip().casefold()
        if normalized == "base64" and not is_base64:
            is_base64 = True
        elif normalized in {"charset=utf-8", "charset=us-ascii"}:
            continue
        else:
            raise _rejected("data URI 参数不在允许清单")
    try:
        encoded_bytes = unquote_to_bytes(encoded)
        payload = (
            base64.b64decode(encoded_bytes, validate=True)
            if is_base64
            else encoded_bytes
        )
    except (binascii.Error, ValueError) as exc:
        raise _rejected("data URI 编码无效") from exc
    _check_resource_size(payload)
    if mime_type == "image/svg+xml":
        _validate_svg(payload, svg_depth=svg_depth)
    return payload, mime_type


def _read_site_resource(site_dir: Path, url: str) -> tuple[bytes, str]:
    """Read one regular file whose fully-resolved target remains in site_dir."""

    parsed = urlsplit(url)
    if parsed.scheme.casefold() != "file" or parsed.netloc:
        raise _rejected("只允许无主机名的 file URL")
    if parsed.query:
        raise _rejected("file URL 不允许查询参数")
    try:
        root = site_dir.resolve(strict=True)
        path_text = url2pathname(unquote(parsed.path))
        if "\x00" in path_text:
            raise _rejected("file URL 包含非法字符")
        candidate = Path(path_text).resolve(strict=True)
        candidate.relative_to(root)
    except ResourceSecurityError:
        raise
    except (FileNotFoundError, OSError, ValueError) as exc:
        raise _rejected("file 资源不存在或越过站点根目录") from exc
    if not candidate.is_file():
        raise _rejected("file 资源不是普通文件")
    try:
        size = candidate.stat().st_size
    except OSError as exc:
        raise _rejected("无法读取 file 资源") from exc
    if size > MAX_RESOURCE_BYTES:
        raise _rejected("资源超过尺寸上限")

    mime_type = (mimetypes.guess_type(candidate.name)[0] or "").casefold()
    if mime_type not in ALLOWED_FILE_MIME_TYPES:
        raise _rejected("file 资源类型不在允许清单")
    try:
        payload = candidate.read_bytes()
    except OSError as exc:
        raise _rejected("无法读取 file 资源") from exc
    _check_resource_size(payload)
    if mime_type == "image/svg+xml":
        _validate_svg(payload)
    return payload, mime_type


class SafeURLFetcher:
    """Fail-closed WeasyPrint fetcher with an explicit rejection counter."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.security_rejections = 0

    def __call__(self, url: str) -> dict[str, object]:
        try:
            scheme = urlsplit(url).scheme.casefold()
            if scheme == "data":
                payload, mime_type = _decode_data_uri(url)
            elif scheme == "file":
                payload, mime_type = _read_site_resource(self.root, url)
            else:
                raise _rejected("资源协议不在允许清单")
            return {
                "string": payload,
                "mime_type": mime_type,
            }
        except ResourceSecurityError:
            self.security_rejections += 1
            raise
        except Exception as exc:
            self.security_rejections += 1
            raise _rejected("资源 URL 无法安全解析") from exc


def make_safe_url_fetcher(site_dir: Path) -> SafeURLFetcher:
    """Create a fail-closed WeasyPrint fetcher bound to one built site root."""

    try:
        root = site_dir.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        raise _rejected("站点根目录不存在") from exc
    if not root.is_dir():
        raise _rejected("站点根路径不是目录")
    return SafeURLFetcher(root)


def flatten_nav(nodes: object) -> list[tuple[str, str]]:
    pages: list[tuple[str, str]] = []
    if isinstance(nodes, list):
        for item in nodes:
            pages.extend(flatten_nav(item))
    elif isinstance(nodes, dict):
        for title, target in nodes.items():
            if isinstance(target, str) and target.endswith(".md"):
                pages.append((str(title), target))
            else:
                pages.extend(flatten_nav(target))
    return pages


def output_html_path(site_dir: Path, markdown_path: Path) -> Path:
    if markdown_path.name == "index.md":
        return site_dir / markdown_path.parent / "index.html"
    return site_dir / markdown_path.with_suffix("") / "index.html"


def web_path_for(markdown_path: Path) -> str:
    if markdown_path.name == "index.md":
        parent = markdown_path.parent.as_posix().strip("/")
        return f"{parent}/" if parent else ""
    return f"{markdown_path.with_suffix('').as_posix().strip('/')}/"


def build_pages(config: dict[str, object], site_dir: Path) -> list[Page]:
    nav_entries = flatten_nav(config.get("nav", []))
    pages: list[Page] = []
    for index, (title, source) in enumerate(nav_entries, start=1):
        source_path = Path(source)
        pages.append(
            Page(
                index=index,
                title=title,
                source_path=source_path,
                html_path=output_html_path(site_dir, source_path),
                web_path=web_path_for(source_path),
                anchor=f"section-{index}",
            )
        )
    return pages


def release_date() -> str:
    explicit = os.environ.get("PLAYBOOK_RELEASE_DATE")
    if explicit:
        return explicit
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.fromtimestamp(
            int(epoch), tz=PUBLICATION_TIMEZONE
        ).date().isoformat()
    return datetime.now(tz=PUBLICATION_TIMEZONE).date().isoformat()


def ensure_noto_font(required: bool) -> bool:
    if not required:
        return True
    executable = shutil.which("fc-match")
    if not executable:
        print("未找到 fc-match，无法验证 Noto Sans CJK。", file=sys.stderr)
        return False
    result = subprocess.run(
        [executable, "-f", "%{family}", "Noto Sans CJK SC"],
        check=False,
        capture_output=True,
        text=True,
    )
    families = result.stdout.casefold()
    if result.returncode != 0 or "noto sans cjk" not in families:
        print(
            f"Noto Sans CJK 验证失败，fc-match 返回：{result.stdout.strip()}",
            file=sys.stderr,
        )
        return False
    return True


def normalize_internal_web_path(page: Page, href: str) -> tuple[str, str] | None:
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        return None
    base = f"https://playbook.invalid/{page.web_path}"
    resolved = urlparse(urljoin(base, href))
    normalized = posixpath.normpath(unquote(resolved.path)).lstrip("/")
    if normalized == ".":
        normalized = ""
    if normalized.endswith("index.html"):
        normalized = normalized[: -len("index.html")]
    elif normalized.endswith(".html"):
        normalized = normalized[: -len(".html")] + "/"
    if normalized and not normalized.endswith("/") and "." not in Path(normalized).name:
        normalized += "/"
    return normalized, resolved.fragment


def local_asset_uri(page: Page, site_dir: Path, raw_url: str) -> str:
    parsed = urlparse(raw_url)
    if parsed.scheme.casefold() == "data":
        _decode_data_uri(raw_url)
        return raw_url
    if parsed.scheme or parsed.netloc:
        raise _rejected("页面资源使用了非本地协议")
    if parsed.query:
        raise _rejected("本地资源 URL 不允许查询参数")
    if parsed.path.startswith("/"):
        target = site_dir / unquote(parsed.path.lstrip("/"))
    else:
        target = page.html_path.parent / unquote(parsed.path)
    try:
        root = site_dir.resolve(strict=True)
        resolved = target.resolve(strict=True)
        resolved.relative_to(root)
    except (FileNotFoundError, OSError, ValueError) as exc:
        raise _rejected("页面资源不存在或越过站点根目录") from exc
    if not resolved.is_file():
        raise _rejected("页面资源不是普通文件")
    uri = resolved.as_uri()
    if parsed.fragment:
        uri += f"#{parsed.fragment}"
    return uri


def rewrite_srcset(
    page: Page,
    site_dir: Path,
    value: str,
    resource_fetcher,
) -> str:
    rewritten: list[str] = []
    for candidate in value.split(","):
        pieces = candidate.strip().split(maxsplit=1)
        if not pieces:
            continue
        source = local_asset_uri(page, site_dir, pieces[0])
        resource_fetcher(source)
        rewritten.append(" ".join([source, *pieces[1:]]))
    return ", ".join(rewritten)


def validate_html_resource_surface(content: Tag) -> None:
    """Reject elements and inline references that could bypass URL rewriting."""

    for tag_name in DANGEROUS_HTML_TAGS:
        if content.find(tag_name) is not None:
            raise _rejected(f"页面正文包含危险元素 {tag_name}")
    for element in content.select("[style]"):
        if isinstance(element, Tag):
            _validate_css_references(str(element.get("style", "")), svg_depth=0)
    for svg in content.find_all("svg"):
        if isinstance(svg, Tag):
            _validate_svg(str(svg).encode("utf-8"))


def extract_articles(pages: list[Page], site_dir: Path) -> list[str]:
    articles: list[str] = []
    page_lookup: dict[str, str] = {}
    id_maps: dict[int, dict[str, str]] = {}
    resource_fetcher = make_safe_url_fetcher(site_dir)

    for page in pages:
        page_lookup[page.web_path] = page.anchor
        page_lookup[f"{page.web_path}index.html"] = page.anchor

    soups: dict[int, BeautifulSoup] = {}
    for page in pages:
        if not page.html_path.is_file():
            raise FileNotFoundError(
                f"导航页面未生成：{page.source_path} -> {page.html_path}"
            )
        soup = BeautifulSoup(page.html_path.read_text(encoding="utf-8"), "html.parser")
        content = soup.select_one(".md-content__inner")
        if content is None:
            raise ValueError(f"页面缺少 Material 正文容器：{page.html_path}")

        for removable in content.select(
            "script, style, .md-content__button, .headerlink, .md-source-file"
        ):
            removable.decompose()
        for self_download in content.select(
            'a[href$="flowagentic-playbook.pdf"]'
        ):
            self_download.decompose()

        validate_html_resource_surface(content)

        id_map: dict[str, str] = {}
        for element in content.select("[id]"):
            if not isinstance(element, Tag):
                continue
            original = str(element.get("id", ""))
            if not original:
                continue
            replacement = f"p{page.index}-{original}"
            element["id"] = replacement
            id_map[original] = replacement
        id_maps[page.index] = id_map
        soups[page.index] = soup

    pages_by_anchor = {page.anchor: page for page in pages}
    for page in pages:
        soup = soups[page.index]
        content = soup.select_one(".md-content__inner")
        assert content is not None

        for element in content.select("[src]"):
            if isinstance(element, Tag):
                source = local_asset_uri(
                    page, site_dir, str(element.get("src", ""))
                )
                resource_fetcher(source)
                element["src"] = source
        for element in content.select("[poster]"):
            if isinstance(element, Tag):
                poster = local_asset_uri(
                    page, site_dir, str(element.get("poster", ""))
                )
                resource_fetcher(poster)
                element["poster"] = poster
        for element in content.select("[background]"):
            if isinstance(element, Tag):
                background = local_asset_uri(
                    page, site_dir, str(element.get("background", ""))
                )
                resource_fetcher(background)
                element["background"] = background
        for element in content.select("[srcset]"):
            if isinstance(element, Tag):
                element["srcset"] = rewrite_srcset(
                    page,
                    site_dir,
                    str(element.get("srcset", "")),
                    resource_fetcher,
                )

        for link in content.select("a[href]"):
            if not isinstance(link, Tag):
                continue
            href = str(link.get("href", ""))
            if href.startswith(("#", "mailto:", "tel:")):
                if href.startswith("#") and len(href) > 1:
                    original = href[1:]
                    link["href"] = f"#{id_maps[page.index].get(original, original)}"
                continue
            parsed_href = urlsplit(href)
            if parsed_href.scheme.casefold() in {"http", "https"}:
                continue
            if parsed_href.scheme or parsed_href.netloc:
                raise _rejected("超链接协议不在允许清单")
            normalized = normalize_internal_web_path(page, href)
            if normalized is None:
                continue
            target_path, fragment = normalized
            target_anchor = page_lookup.get(target_path)
            if target_anchor is not None:
                target_page = pages_by_anchor[target_anchor]
                if fragment:
                    destination = id_maps[target_page.index].get(
                        fragment, target_page.anchor
                    )
                else:
                    destination = target_page.anchor
                link["href"] = f"#{destination}"
            else:
                link["href"] = local_asset_uri(page, site_dir, href)

        articles.append(
            f'<section class="pdf-page" id="{page.anchor}" '
            f'data-source="{html.escape(page.source_path.as_posix())}">'
            f"{content.decode_contents()}</section>"
        )

    return articles


def pdf_stylesheet() -> str:
    return """
    @page {
      size: A4;
      margin: 18mm 16mm 18mm;
      @top-left {
        color: #667085;
        content: "FlowAgentic 培训与操作 Playbook";
        font-size: 8pt;
      }
      @top-right {
        color: #667085;
        content: string(chapter);
        font-size: 8pt;
      }
      @bottom-center {
        color: #667085;
        content: counter(page) " / " counter(pages);
        font-size: 8pt;
      }
    }
    @page:first {
      @top-left { content: none; }
      @top-right { content: none; }
      @bottom-center { content: none; }
    }
    * { box-sizing: border-box; }
    html {
      color: #101828;
      font-family: "Noto Sans CJK SC", "Noto Sans SC", "Source Han Sans SC",
        "PingFang SC", "Microsoft YaHei", sans-serif;
      font-size: 10pt;
      line-height: 1.65;
    }
    body { margin: 0; }
    .pdf-cover {
      align-items: flex-start;
      break-after: page;
      display: flex;
      flex-direction: column;
      min-height: 245mm;
      padding-top: 36mm;
    }
    .pdf-cover h1 {
      color: #1d2939;
      font-size: 30pt;
      line-height: 1.2;
      margin: 0 0 12mm;
    }
    .pdf-cover .subtitle {
      color: #475467;
      font-size: 14pt;
      margin-bottom: 30mm;
    }
    .pdf-cover .classification {
      border: 1px solid #667085;
      border-radius: 3mm;
      color: #344054;
      font-weight: 700;
      margin-bottom: 8mm;
      padding: 2mm 4mm;
    }
    .pdf-cover dl {
      display: grid;
      gap: 2mm 5mm;
      grid-template-columns: 30mm 1fr;
      margin: auto 0 0;
    }
    .pdf-cover dt { color: #667085; }
    .pdf-cover dd { margin: 0; overflow-wrap: anywhere; }
    .pdf-toc { break-after: page; }
    .pdf-toc h1 { font-size: 22pt; margin: 0 0 8mm; }
    .pdf-toc ol { columns: 2; column-gap: 12mm; padding-left: 7mm; }
    .pdf-toc li { break-inside: avoid; margin: 0 0 3mm; }
    .pdf-toc a { color: #344054; text-decoration: none; }
    .pdf-toc a::after {
      color: #667085;
      content: leader(".") target-counter(attr(href), page);
      margin-left: 2mm;
    }
    .pdf-page { break-before: page; }
    .pdf-page h1 {
      color: #1d2939;
      font-size: 21pt;
      line-height: 1.3;
      margin: 0 0 8mm;
      string-set: chapter content();
    }
    h2 {
      border-bottom: 0.25mm solid #d0d5dd;
      color: #1d2939;
      font-size: 15pt;
      line-height: 1.35;
      margin: 10mm 0 4mm;
      padding-bottom: 1.5mm;
    }
    h3 { color: #344054; font-size: 12pt; margin: 7mm 0 3mm; }
    h1, h2, h3, h4 { break-after: avoid; }
    p, li { orphans: 3; widows: 3; }
    a { color: #175cd3; overflow-wrap: anywhere; }
    img, svg {
      display: block;
      height: auto;
      margin: 4mm auto;
      max-width: 100%;
    }
    figure, table, pre, blockquote, .admonition, .tabbed-set {
      break-inside: avoid;
    }
    figcaption {
      color: #667085;
      font-size: 8.5pt;
      text-align: center;
    }
    table {
      border-collapse: collapse;
      font-size: 8.5pt;
      margin: 4mm 0;
      width: 100%;
    }
    th, td {
      border: 0.2mm solid #d0d5dd;
      padding: 1.5mm 2mm;
      text-align: left;
      vertical-align: top;
    }
    th { background: #f2f4f7; }
    code {
      background: #f2f4f7;
      border-radius: 1mm;
      font-family: "Noto Sans Mono CJK SC", "SFMono-Regular", Consolas, monospace;
      font-size: 8.5pt;
      padding: 0.2mm 0.8mm;
    }
    pre {
      background: #101828;
      border-radius: 2mm;
      color: #f9fafb;
      font-size: 8pt;
      line-height: 1.45;
      overflow-wrap: anywhere;
      padding: 3mm;
      white-space: pre-wrap;
    }
    pre code { background: transparent; color: inherit; padding: 0; }
    blockquote {
      border-left: 1mm solid #98a2b3;
      color: #475467;
      margin-left: 0;
      padding-left: 4mm;
    }
    .admonition {
      border: 0.25mm solid #98a2b3;
      border-radius: 2mm;
      margin: 4mm 0;
      padding: 3mm 4mm;
    }
    .admonition-title { font-weight: 700; margin-top: 0; }
    .headerlink, .md-content__button, button { display: none !important; }
    """


def compose_html(
    title: str,
    pages: list[Page],
    articles: list[str],
    release_version: str,
    release_sha: str,
) -> str:
    toc_items = "".join(
        f'<li><a href="#{page.anchor}">{html.escape(page.title)}</a></li>'
        for page in pages
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
</head>
<body>
  <section class="pdf-cover">
    <div class="classification">公开脱敏培训版</div>
    <h1>{html.escape(title)}</h1>
    <p class="subtitle">使用者、流程搭建者、二次开发者、管理员／运维人员</p>
    <dl>
      <dt>Playbook 版本</dt><dd>{html.escape(release_version)}</dd>
      <dt>产品提交</dt><dd>{html.escape(release_sha)}</dd>
      <dt>发布日期</dt><dd>{html.escape(release_date())}</dd>
      <dt>内容许可</dt><dd>正文 CC BY-NC-SA 4.0；代码 MIT</dd>
    </dl>
  </section>
  <nav class="pdf-toc">
    <h1>目录</h1>
    <ol>{toc_items}</ol>
  </nav>
  {''.join(articles)}
</body>
</html>
"""


def main() -> int:
    args = parse_args()
    config_path = args.config.resolve()
    site_dir = args.site_dir.resolve()
    output = args.output.resolve()
    tmp_dir = args.tmp_dir.resolve()

    if not config_path.is_file():
        return fail(f"未找到 MkDocs 配置：{config_path}")
    if not site_dir.is_dir():
        return fail(f"未找到站点构建目录：{site_dir}；请先运行 mkdocs build --strict")
    if not ensure_noto_font(args.require_noto):
        return 1

    config = yaml.load(
        config_path.read_text(encoding="utf-8"),
        Loader=MkDocsConfigLoader,
    )
    if not isinstance(config, dict):
        return fail("mkdocs.yml 顶层结构无效")
    pages = build_pages(config, site_dir)
    if not pages:
        return fail("mkdocs.yml 的 nav 中没有 Markdown 页面")

    missing = [str(page.html_path) for page in pages if not page.html_path.is_file()]
    if missing:
        return fail("以下导航页面未生成：\n- " + "\n- ".join(missing))

    try:
        articles = extract_articles(pages, site_dir)
    except (FileNotFoundError, ValueError) as exc:
        return fail(str(exc))

    title = str(config.get("site_name", "FlowAgentic 培训与操作 Playbook"))
    baseline = config.get("extra", {})
    baseline = baseline.get("baseline", {}) if isinstance(baseline, dict) else {}
    fallback_sha = (
        str(baseline.get("release_sha", "未绑定"))
        if isinstance(baseline, dict)
        else "未绑定"
    )
    release_version = os.environ.get("PLAYBOOK_RELEASE_VERSION", "draft")
    release_sha = os.environ.get("PLAYBOOK_RELEASE_SHA", fallback_sha)
    document = compose_html(title, pages, articles, release_version, release_sha)
    try:
        resource_fetcher = make_safe_url_fetcher(site_dir)
    except ResourceSecurityError as exc:
        return fail(str(exc))

    tmp_dir.mkdir(parents=True, exist_ok=True)
    combined_html = tmp_dir / "flowagentic-playbook.html"
    combined_html.write_text(document, encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        HTML(
            string=document,
            base_url=site_dir.as_uri(),
            url_fetcher=resource_fetcher,
        ).write_pdf(
            output,
            stylesheets=[
                CSS(
                    string=pdf_stylesheet(),
                    base_url=site_dir.as_uri(),
                    url_fetcher=resource_fetcher,
                )
            ],
            presentational_hints=True,
        )
    except ResourceSecurityError as exc:
        output.unlink(missing_ok=True)
        return fail(str(exc))
    except Exception as exc:  # pragma: no cover - WeasyPrint reports backend detail.
        del exc
        output.unlink(missing_ok=True)
        return fail("WeasyPrint 渲染失败（资源与路径细节已隐藏）")

    if resource_fetcher.security_rejections:
        output.unlink(missing_ok=True)
        return fail("WeasyPrint 尝试读取被拒绝的资源；未保留本次输出")

    if not output.is_file() or output.stat().st_size < 1024:
        output.unlink(missing_ok=True)
        return fail(f"PDF 未生成或尺寸异常：{output}")
    if output.read_bytes()[:5] != b"%PDF-":
        output.unlink(missing_ok=True)
        return fail(f"输出不是 PDF：{output}")

    site_download = site_dir / "assets" / "downloads" / "flowagentic-playbook.pdf"
    site_download.parent.mkdir(parents=True, exist_ok=True)
    if output != site_download:
        shutil.copy2(output, site_download)

    print(f"PDF 已生成：{output} ({output.stat().st_size:,} bytes)")
    print(f"站点下载副本：{site_download}")
    print(f"中间 HTML：{combined_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
