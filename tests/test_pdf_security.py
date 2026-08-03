from __future__ import annotations

import base64
import sys
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_pdf  # noqa: E402
import validate_pdf  # noqa: E402


@pytest.mark.parametrize(
    "font_name",
    [
        "DFCEGX+Noto-Sans-CJK-SC-Bold",
        "TSPJMR+Noto-Sans-CJK-SC",
        "ABCDEF+NotoSansCJKsc-Regular",
    ],
)
def test_pdf_font_validation_accepts_noto_postscript_spellings(
    font_name: str,
) -> None:
    assert validate_pdf.embeds_noto_sans_cjk([font_name])


@pytest.mark.parametrize(
    "font_name",
    [
        "ABCDEF+Source-Han-Sans-SC",
        "ABCDEF+Noto-Sans-SC",
        "ABCDEF+PingFang-SC",
    ],
)
def test_pdf_font_validation_rejects_non_cjk_or_non_noto_fonts(
    font_name: str,
) -> None:
    assert not validate_pdf.embeds_noto_sans_cjk([font_name])


def test_pdf_config_env_is_allowlisted_and_supports_null_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("PLAYBOOK_VERSION_PROVIDER", raising=False)
    config = yaml.load(
        "provider: !ENV [PLAYBOOK_VERSION_PROVIDER, null]\n",
        Loader=build_pdf.MkDocsConfigLoader,
    )
    assert config == {"provider": None}

    monkeypatch.setenv("PLAYBOOK_VERSION_PROVIDER", "mike")
    config = yaml.load(
        "provider: !ENV [PLAYBOOK_VERSION_PROVIDER, null]\n",
        Loader=build_pdf.MkDocsConfigLoader,
    )
    assert config == {"provider": "mike"}


def test_pdf_config_env_rejects_unallowlisted_variable() -> None:
    with pytest.raises(yaml.constructor.ConstructorError):
        yaml.load(
            "value: !ENV [UNREVIEWED_SECRET, null]\n",
            Loader=build_pdf.MkDocsConfigLoader,
        )


def test_release_date_uses_chinese_publication_timezone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("PLAYBOOK_RELEASE_DATE", raising=False)
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1785776400")

    assert build_pdf.release_date() == "2026-08-04"


def _page(site_dir: Path, body: str) -> build_pdf.Page:
    html_path = site_dir / "index.html"
    site_dir.mkdir(parents=True, exist_ok=True)
    html_path.write_text(
        f'<html><body><article class="md-content__inner">{body}</article></body></html>',
        encoding="utf-8",
    )
    return build_pdf.Page(
        index=1,
        title="测试",
        source_path=Path("index.md"),
        html_path=html_path,
        web_path="",
        anchor="section-1",
    )


def test_fetcher_rejects_remote_url_and_redacts_query(tmp_path: Path) -> None:
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    fetch = build_pdf.make_safe_url_fetcher(site_dir)

    query_name = "to" + "ken"
    with pytest.raises(build_pdf.ResourceSecurityError) as caught:
        fetch(f"https://example.invalid/image.png?{query_name}=do-not-disclose")

    message = str(caught.value)
    assert fetch.security_rejections == 1
    assert "do-not-disclose" not in message
    assert f"?{query_name}" not in message


def test_fetcher_rejects_outside_file_and_symlink_escape(tmp_path: Path) -> None:
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"outside")
    fetch = build_pdf.make_safe_url_fetcher(site_dir)

    with pytest.raises(build_pdf.ResourceSecurityError):
        fetch(outside.as_uri())

    link = site_dir / "linked.png"
    link.symlink_to(outside)
    with pytest.raises(build_pdf.ResourceSecurityError):
        fetch(link.as_uri())


def test_fetcher_allows_in_site_file_and_allowlisted_data_uri(tmp_path: Path) -> None:
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    image = site_dir / "safe.png"
    image.write_bytes(b"\x89PNG\r\n\x1a\ntraining")
    fetch = build_pdf.make_safe_url_fetcher(site_dir)

    local = fetch(image.as_uri())
    assert local["string"] == image.read_bytes()
    assert local["mime_type"] == "image/png"

    encoded = base64.b64encode(b"synthetic-image").decode("ascii")
    embedded = fetch(f"data:image/png;base64,{encoded}")
    assert embedded["string"] == b"synthetic-image"
    assert embedded["mime_type"] == "image/png"

    svg = b'<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0h1v1z"/></svg>'
    svg_data = base64.b64encode(svg).decode("ascii")
    assert fetch(f"data:image/svg+xml;base64,{svg_data}")["string"] == svg


def test_fetcher_rejects_file_query_without_leaking_value(tmp_path: Path) -> None:
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    image = site_dir / "safe.png"
    image.write_bytes(b"png")
    fetch = build_pdf.make_safe_url_fetcher(site_dir)

    with pytest.raises(build_pdf.ResourceSecurityError) as caught:
        fetch(f"{image.as_uri()}?credential=hidden-value")

    assert "hidden-value" not in str(caught.value)
    assert "credential" not in str(caught.value)


def test_fetcher_rejects_non_resource_data_uri(tmp_path: Path) -> None:
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    fetch = build_pdf.make_safe_url_fetcher(site_dir)

    with pytest.raises(build_pdf.ResourceSecurityError):
        fetch("data:text/html,%3Cscript%3Ealert(1)%3C/script%3E")

    with pytest.raises(build_pdf.ResourceSecurityError) as caught:
        fetch("https://[malformed.invalid/path?secret=still-hidden")
    assert "still-hidden" not in str(caught.value)


@pytest.mark.parametrize("tag_name", sorted(build_pdf.DANGEROUS_HTML_TAGS))
def test_extract_articles_rejects_dangerous_embedding_tags(
    tmp_path: Path, tag_name: str
) -> None:
    site_dir = tmp_path / "site"
    page = _page(site_dir, f'<{tag_name} src="https://example.invalid/x"></{tag_name}>')

    with pytest.raises(build_pdf.ResourceSecurityError) as caught:
        build_pdf.extract_articles([page], site_dir)

    assert tag_name in str(caught.value)


def test_extract_articles_rejects_remote_resource_and_redacts_query(
    tmp_path: Path,
) -> None:
    site_dir = tmp_path / "site"
    query_name = "api" + "_key"
    page = _page(
        site_dir,
        f'<img src="https://example.invalid/x.png?{query_name}=never-print-this">',
    )

    with pytest.raises(build_pdf.ResourceSecurityError) as caught:
        build_pdf.extract_articles([page], site_dir)

    message = str(caught.value)
    assert "never-print-this" not in message
    assert query_name not in message


@pytest.mark.parametrize(
    "style",
    [
        "background-image:url(https://example.invalid/pixel)",
        r"background-image:u\72l(https://example.invalid/pixel)",
        "background-image:image('https://example.invalid/pixel')",
    ],
)
def test_extract_articles_rejects_inline_css_resource_bypasses(
    tmp_path: Path, style: str
) -> None:
    site_dir = tmp_path / "site"
    page = _page(site_dir, f'<p style="{style}">text</p>')

    with pytest.raises(build_pdf.ResourceSecurityError):
        build_pdf.extract_articles([page], site_dir)


def test_svg_allows_internal_fragment_and_rejects_external_reference(
    tmp_path: Path,
) -> None:
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    safe_svg = site_dir / "safe.svg"
    safe_svg.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<defs><path id="shape" d="M0 0h1v1z"/></defs>'
        '<use href="#shape"/></svg>',
        encoding="utf-8",
    )
    fetch = build_pdf.make_safe_url_fetcher(site_dir)
    assert fetch(safe_svg.as_uri())["mime_type"] == "image/svg+xml"

    unsafe_svg = site_dir / "unsafe.svg"
    unsafe_svg.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<image href="https://example.invalid/pixel?secret=not-for-errors"/>'
        "</svg>",
        encoding="utf-8",
    )
    with pytest.raises(build_pdf.ResourceSecurityError) as caught:
        fetch(unsafe_svg.as_uri())
    assert "not-for-errors" not in str(caught.value)


def test_extract_articles_rejects_inline_svg_external_reference(
    tmp_path: Path,
) -> None:
    site_dir = tmp_path / "site"
    page = _page(
        site_dir,
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<use href="https://example.invalid/icons.svg#shape"/>'
        "</svg>",
    )

    with pytest.raises(build_pdf.ResourceSecurityError):
        build_pdf.extract_articles([page], site_dir)


@pytest.mark.parametrize(
    "svg",
    [
        '<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>',
        '<svg xmlns="http://www.w3.org/2000/svg"><animate attributeName="x"/></svg>',
        '<?xml-stylesheet href="https://example.invalid/x.css"?>'
        '<svg xmlns="http://www.w3.org/2000/svg"/>',
    ],
)
def test_fetcher_rejects_active_svg(tmp_path: Path, svg: str) -> None:
    site_dir = tmp_path / "site"
    site_dir.mkdir()
    candidate = site_dir / "active.svg"
    candidate.write_text(svg, encoding="utf-8")

    with pytest.raises(build_pdf.ResourceSecurityError):
        build_pdf.make_safe_url_fetcher(site_dir)(candidate.as_uri())
