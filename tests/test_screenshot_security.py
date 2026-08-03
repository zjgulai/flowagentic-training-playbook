from __future__ import annotations

import hashlib
import copy
import sys
from pathlib import Path

import yaml
from PIL import Image
from PIL.PngImagePlugin import PngInfo


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_public_safety as public_safety  # noqa: E402
import validate_screenshots as screenshots  # noqa: E402


def load(path: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_scan_receipt_template_tracks_current_validator_contract() -> None:
    template = load("data/screenshots/scan-receipt.template.yml")
    manifest = load("data/manifests/screenshots.yml")
    expected_validator = {
        "name": screenshots.VALIDATOR_NAME,
        "version": screenshots.VALIDATOR_VERSION,
    }

    assert template["validator"] == expected_validator
    manifest_validator = manifest["capture_contract"]["validator"]
    assert {
        "name": manifest_validator["name"],
        "version": manifest_validator["version"],
    } == expected_validator


def test_generated_screenshot_plan_satisfies_state_and_semantic_contract() -> None:
    plan = load("data/manifests/screenshot-plan.yml")
    assert screenshots.validate_plan(plan) == []

    states_by_sop: dict[str, set[str]] = {}
    for shot in plan["shots"]:
        states_by_sop.setdefault(shot["sop_id"], set()).add(shot["planned_state"])
        assert shot["doc_path"].startswith("docs/")
        assert (ROOT / shot["doc_path"]).is_file()
    for sop_id in screenshots.CORE_SOPS:
        assert screenshots.CORE_STATES <= states_by_sop[sop_id]

    ext = {
        shot["id"]: (shot["route"], shot["provider"], shot["feature_status"])
        for shot in plan["shots"]
        if shot["id"].startswith("EXT-")
    }
    assert ext == screenshots.EXT_SEMANTICS


def test_ocr_rules_detect_secret_classes_without_returning_values() -> None:
    text = "\n".join(
        [
            "管理员 admin" + "@" + "real-company.test",
            "Authoriza" + "tion: Bearer " + "sk-" + "abcdefghijklmnopqrstuvwxyz123456",
            "内部入口 https://portal.ops" + ".internal",
            "对象 123e4567-e89b-12d3" + "-a456-426614174000",
        ]
    )
    findings = public_safety.scan_ocr_text(text, "docs/assets/screenshots/test.webp")
    kinds = {item["kind"] for item in findings}
    assert "image OCR email" in kinds
    assert "image OCR internal domain" in kinds
    assert "image OCR UUID" in kinds
    assert any("key" in str(kind).lower() or "credential" in str(kind).lower() for kind in kinds)
    assert all("abcdefghijklmnopqrstuvwxyz" not in repr(item) for item in findings)


def test_ocr_rules_allow_synthetic_email_and_masked_value() -> None:
    findings = public_safety.scan_ocr_text(
        "培训账号 learner" + "@example.com\n" + "pass" + "word: " + "*" * 12,
        "docs/assets/screenshots/safe.webp",
    )
    assert findings == []


def test_ocr_rules_detect_space_and_punctuation_split_tokens() -> None:
    text = "\n".join(
        [
            "a , d , m , i , n @ private-corp . test",
            "A P I _ K e y : s k - abcdefghijklmnopqrstuvwxyz123456",
            "A u t h o r i z a t i o n : B e a r e r abcdefghijklmnop.1234567890",
            "123e4567 - e89b - 12d3 - a456 - 426614174000",
        ]
    )
    findings = public_safety.scan_ocr_text(text, "docs/assets/screenshots/split.webp")
    kinds = {str(item["kind"]) for item in findings}
    assert "image OCR email" in kinds
    assert "image OCR UUID" in kinds
    assert "image OCR Bearer token" in kinds
    assert any("key" in kind.lower() or "credential" in kind.lower() for kind in kinds)
    assert all("abcdefghijklmnopqrstuvwxyz" not in repr(item) for item in findings)


def test_png_text_and_webp_xmp_metadata_are_rejected_without_value_leak(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(public_safety, "ROOT", tmp_path)
    png_path = tmp_path / "docs/assets/screenshots/meta.png"
    webp_path = tmp_path / "docs/assets/screenshots/meta.webp"
    clean_webp_path = tmp_path / "docs/assets/screenshots/clean.webp"
    png_path.parent.mkdir(parents=True)
    png_info = PngInfo()
    png_info.add_text("Comment", "owner" + "@" + "private-corp.test")
    Image.new("RGB", (10, 10), "white").save(png_path, format="PNG", pnginfo=png_info)
    Image.new("RGB", (10, 10), "white").save(
        webp_path,
        format="WEBP",
        xmp=b"to" + b"ken: " + b"abcdefghijklmnopqrstuvwxyz123456",
    )
    Image.new("RGB", (10, 10), "white").save(clean_webp_path, format="WEBP")

    png_findings = public_safety.scan_image_metadata(png_path)
    webp_findings = public_safety.scan_image_metadata(webp_path)
    assert any(item["kind"] == "image nonessential metadata" for item in png_findings)
    assert any(item["kind"] == "image metadata email" for item in png_findings)
    assert any(item["kind"] == "image nonessential metadata" for item in webp_findings)
    assert public_safety.scan_image_metadata(clean_webp_path) == []
    assert all("private-corp" not in repr(item) for item in png_findings + webp_findings)


def _make_item_and_receipt(tmp_path: Path) -> tuple[dict, dict, dict]:
    source = tmp_path / "data/screenshots/source/CF-001.png"
    annotated = tmp_path / "docs/assets/screenshots/CF-001.webp"
    receipt = tmp_path / "data/screenshots/receipts/CF-001.yml"
    source.parent.mkdir(parents=True)
    annotated.parent.mkdir(parents=True)
    receipt.parent.mkdir(parents=True)
    Image.new("RGB", (1440, 1000), "white").save(source, format="PNG")
    Image.new("RGB", (1440, 1000), "white").save(annotated, format="WEBP", quality=70)

    safe_text_hash = hashlib.sha256("合成培训页面".encode("utf-8")).hexdigest()
    scan = {
        "engine": "tesseract",
        "engine_version": "tesseract test",
        "languages": ["chi_sim", "eng"],
        "psm": "11",
        "text_sha256": safe_text_hash,
        "character_count": 6,
        "ruleset_sha256": public_safety.image_ruleset_sha256(),
    }
    release_sha = "a" * 40
    item = {
        "id": "CF-001",
        "sop_id": "chatflow",
        "doc_path": "docs/04-chatflow/index.md",
        "step": 1,
        "route": "/chatflows",
        "state": "before",
        "role": "builder",
        "viewport": "1440x1000@100%",
        "locale": "zh-CN",
        "theme": "light",
        "release_sha": release_sha,
        "fixture": "synthetic-enterprise-v1",
        "provider": "none",
        "feature_status": "production-enabled",
        "redaction_status": "passed",
        "alt_text": "对话流程操作前的合成培训页面",
        "source_file": "data/screenshots/source/CF-001.png",
        "source_sha256": file_sha256(source),
        "annotated_file": "docs/assets/screenshots/CF-001.webp",
        "annotated_sha256": file_sha256(annotated),
        "scan_receipt": "data/screenshots/receipts/CF-001.yml",
        "captured_at": "2026-08-01T01:00:00Z",
        "quality_checks": {
            "ocr": "passed",
            "exif": "passed",
            "metadata": "passed",
            "secrets": "passed",
            "dimensions": "passed",
            "file_size": "passed",
        },
    }
    receipt_payload = {
        "schema_version": 1,
        "screenshot_id": item["id"],
        "release_sha": release_sha,
        "validator": {
            "name": screenshots.VALIDATOR_NAME,
            "version": screenshots.VALIDATOR_VERSION,
        },
        "source": {
            "file": item["source_file"],
            "sha256": item["source_sha256"],
            "ocr": scan,
        },
        "annotated": {
            "file": item["annotated_file"],
            "sha256": item["annotated_sha256"],
            "ocr": scan,
        },
        "secret_scan": {
            "ruleset_sha256": public_safety.image_ruleset_sha256(),
            "source_findings": 0,
            "annotated_findings": 0,
        },
        "status": "passed",
        "scanned_at": "2026-08-01T01:05:00Z",
    }
    receipt.write_text(
        yaml.safe_dump(receipt_payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    item["scan_receipt_sha256"] = file_sha256(receipt)
    plan = load("data/manifests/screenshot-plan.yml")
    for shot in plan["shots"]:
        planned_doc = tmp_path / shot["doc_path"]
        planned_doc.parent.mkdir(parents=True, exist_ok=True)
        planned_doc.touch()
    return item, scan, plan


def test_actual_ocr_is_recomputed_and_receipt_cannot_hide_secret(
    tmp_path: Path, monkeypatch
) -> None:
    item, scan, plan = _make_item_and_receipt(tmp_path)
    monkeypatch.setattr(screenshots, "ROOT", tmp_path)
    monkeypatch.setattr(screenshots, "scan_image", lambda _path: (scan, []))
    manifest = {
        "schema_version": 3,
        "release_sha": item["release_sha"],
        "capture_status": "blocked",
        "screenshots": [item],
    }
    assert screenshots.validate_manifest(manifest, plan, release=False) == []

    leaked = [{"file": item["source_file"], "line": 1, "kind": "image OCR email"}]

    def rescan(path: Path):
        return (scan, leaked if path.suffix.lower() == ".png" else [])

    monkeypatch.setattr(screenshots, "scan_image", rescan)
    errors = screenshots.validate_manifest(manifest, plan, release=False)
    assert any("source image safety scan found" in error for error in errors)
    assert any("current OCR rescan contradicts" in error for error in errors)


def test_missing_ocr_fails_closed_for_real_images(tmp_path: Path, monkeypatch) -> None:
    item, _scan, plan = _make_item_and_receipt(tmp_path)
    monkeypatch.setattr(screenshots, "ROOT", tmp_path)

    def unavailable(_path: Path):
        raise public_safety.OCRUnavailable("not installed")

    monkeypatch.setattr(screenshots, "scan_image", unavailable)
    manifest = {
        "schema_version": 3,
        "release_sha": item["release_sha"],
        "capture_status": "passed",
        "screenshots": [item],
    }
    release_plan = copy.deepcopy(plan)
    release_plan["release_sha"] = item["release_sha"]
    for shot in release_plan["shots"]:
        shot["release_sha"] = item["release_sha"]
        shot["capture_status"] = "captured-verified"
    errors = screenshots.validate_manifest(manifest, release_plan, release=True)
    assert any("required OCR engine/languages are unavailable" in error for error in errors)


def test_manifest_schema_requires_dual_hash_and_receipt_binding() -> None:
    schema = load("schemas/screenshot.schema.json")
    required = set(schema["required"])
    assert {
        "source_file",
        "source_sha256",
        "annotated_file",
        "annotated_sha256",
        "scan_receipt",
        "scan_receipt_sha256",
        "captured_at",
        "quality_checks",
        "doc_path",
        "theme",
        "feature_status",
    } <= required


def test_release_manifest_semantics_are_bound_to_plan(tmp_path: Path, monkeypatch) -> None:
    item, scan, plan = _make_item_and_receipt(tmp_path)
    monkeypatch.setattr(screenshots, "ROOT", tmp_path)
    monkeypatch.setattr(screenshots, "scan_image", lambda _path: (scan, []))
    plan["release_sha"] = item["release_sha"]
    for shot in plan["shots"]:
        shot["release_sha"] = item["release_sha"]
        shot["capture_status"] = "captured-verified"
    item["route"] = "/tampered-route"
    manifest = {
        "schema_version": 3,
        "release_sha": item["release_sha"],
        "capture_status": "passed",
        "screenshots": [item],
    }
    errors = screenshots.validate_manifest(manifest, plan, release=True)
    assert any("manifest route does not match plan route" in error for error in errors)


def test_duplicate_image_hashes_require_one_structured_shared_approval() -> None:
    occurrences = [("CF-001", {}), ("CF-002", {})]
    errors = screenshots._validate_hash_reuse_group(
        hash_field="source_sha256", actual_hash="a" * 64, occurrences=occurrences
    )
    assert len(errors) == 2
    approval = {
        "approval_id": "SHR-TRAINING-01",
        "status": "approved",
        "approved_by": "content-security-reviewer",
        "approved_at": "2026-08-01T01:00:00Z",
        "reason": "同一只读空状态在两个连续步骤中具有相同的证据语义。",
        "hash_types": ["source_sha256"],
        "approved_hashes": {"source_sha256": "a" * 64},
        "screenshot_ids": ["CF-001", "CF-002"],
    }
    approved = [("CF-001", {"hash_reuse_approval": approval}), ("CF-002", {"hash_reuse_approval": approval})]
    assert screenshots._validate_hash_reuse_group(
        hash_field="source_sha256", actual_hash="a" * 64, occurrences=approved
    ) == []
    stale = copy.deepcopy(approved)
    stale[0][1]["hash_reuse_approval"] = copy.deepcopy(approval)
    stale[0][1]["hash_reuse_approval"]["approved_hashes"]["source_sha256"] = "b" * 64
    assert any(
        "not bound to current bytes" in error
        for error in screenshots._validate_hash_reuse_group(
            hash_field="source_sha256", actual_hash="a" * 64, occurrences=stale
        )
    )


def test_screenshot_paths_reject_traversal_and_symlinks(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(screenshots, "ROOT", tmp_path)
    outside = tmp_path / "outside.png"
    Image.new("RGB", (10, 10), "white").save(outside, format="PNG")
    resolved, error = screenshots._resolve_confined_path(
        "../outside.png", screenshots.SOURCE_ROOT, {".png"}
    )
    assert resolved is None
    assert "normalized repository-relative" in str(error)

    source_root = tmp_path / screenshots.SOURCE_ROOT
    source_root.mkdir(parents=True)
    link = source_root / "linked.png"
    link.symlink_to(outside)
    resolved, error = screenshots._resolve_confined_path(
        "data/screenshots/source/linked.png", screenshots.SOURCE_ROOT, {".png"}
    )
    assert resolved is None
    assert "symlinked" in str(error)


def test_release_page_must_embed_exact_planned_screenshot(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(screenshots, "ROOT", tmp_path)
    page = tmp_path / "docs/04-chatflow/index.md"
    image = tmp_path / "docs/assets/screenshots/CF-001.webp"
    page.parent.mkdir(parents=True)
    image.parent.mkdir(parents=True)
    image.touch()
    page.write_text(
        "---\nscreenshot_ids:\n  - CF-001\n---\n"
        "# 对话流程\n\n"
        "![对话流程操作前](../assets/screenshots/CF-001.webp)"
        '{ data-screenshot-id="CF-001" }\n',
        encoding="utf-8",
    )
    plan = {
        "shots": [
            {
                "id": "CF-001",
                "doc_path": "docs/04-chatflow/index.md",
                "required_for_release": True,
            }
        ]
    }
    manifest = {
        "screenshots": [
            {
                "id": "CF-001",
                "annotated_file": "docs/assets/screenshots/CF-001.webp",
                "alt_text": "对话流程操作前",
            }
        ]
    }
    assert screenshots.validate_page_bindings(plan, manifest) == []

    manifest["screenshots"][0]["alt_text"] = "不匹配的说明"
    errors = screenshots.validate_page_bindings(plan, manifest)
    assert any("alt text does not match" in error for error in errors)
