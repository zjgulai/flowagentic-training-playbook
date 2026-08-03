#!/usr/bin/env python3
"""Fail closed when the Playbook imports product-repository Git state."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_BASELINE_SHA = "6a5bb28b4590da42c7f1a42c515a8d2d5ba8cd64"
DEFAULT_FORBIDDEN_REMOTES = (
    "github.com/zjgulai/flowise",
    "github.com/flowiseai/flowise",
)
IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "site",
    "output",
    "tmp",
    "artifacts",
}
SENSITIVE_FILENAMES = re.compile(
    r"(^|[-_.])(deploy[-_.]?key|id_rsa|id_ed25519|service[-_.]?account)"
    r"($|[-_.])|(?:\.pem|\.p12|\.pfx|\.key)$",
    re.IGNORECASE,
)
REUSABLE_WORKFLOW = re.compile(
    r"^\s*uses:\s*[^#\s]+/\.github/workflows/[^@\s]+@",
    re.MULTILINE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="验证 Playbook Git 历史、远端和发布配置的独立性。"
    )
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    return parser.parse_args()


def git(root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def visible_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRECTORIES for part in relative.parts):
            continue
        if path.is_file() or path.is_symlink():
            files.append(path)
    return files


def main() -> int:
    root = parse_args().root.resolve()
    issues: list[str] = []

    if not (root / ".git").is_dir():
        issues.append(f"目标目录不是独立 Git 仓库：{root}")
    top_level = git(root, "rev-parse", "--show-toplevel")
    if top_level.returncode != 0 or Path(top_level.stdout.strip()).resolve() != root:
        issues.append("Git 顶层目录与 Playbook 根目录不一致")

    if (root / ".gitmodules").exists():
        issues.append("发现 .gitmodules；公开 Playbook 禁止使用 submodule")
    if (root / ".git/modules").exists():
        issues.append("发现 .git/modules；仓库包含 submodule 状态")

    for candidate in root.rglob(".git"):
        if candidate.resolve() == (root / ".git").resolve():
            continue
        relative = candidate.relative_to(root)
        if any(part in IGNORED_DIRECTORIES for part in relative.parts[:-1]):
            continue
        issues.append(f"发现嵌套 Git 历史：{relative}")

    staged = git(root, "ls-files", "--stage")
    if staged.returncode != 0:
        issues.append(f"无法读取 Git 索引：{staged.stderr.strip()}")
    else:
        for line in staged.stdout.splitlines():
            if line.startswith("160000 "):
                path = line.split("\t", 1)[-1]
                issues.append(f"发现 gitlink：{path}")

    source_object = git(root, "cat-file", "-e", f"{SOURCE_BASELINE_SHA}^{{commit}}")
    if source_object.returncode == 0:
        issues.append(
            "独立仓库包含产品源码基线提交对象；不得复制或嫁接产品仓库 Git 历史"
        )

    history = git(root, "log", "--format=%B")
    if history.returncode == 0 and re.search(
        r"^git-subtree-(?:dir|split|mainline):", history.stdout, re.MULTILINE
    ):
        issues.append("提交历史包含 git subtree 元数据")

    extra_forbidden = tuple(
        item.strip().casefold()
        for item in os.environ.get("FORBIDDEN_GIT_REMOTES", "").split(",")
        if item.strip()
    )
    forbidden = DEFAULT_FORBIDDEN_REMOTES + extra_forbidden
    remotes = git(root, "remote", "-v")
    if remotes.returncode == 0:
        for line in remotes.stdout.splitlines():
            folded = line.casefold()
            if any(pattern in folded for pattern in forbidden):
                issues.append(f"发现产品源码仓库远端：{line}")

    for path in visible_files(root):
        relative = path.relative_to(root)
        if SENSITIVE_FILENAMES.search(path.name):
            issues.append(f"发现疑似部署密钥文件：{relative}")
        if relative.parts[:2] == (".github", "workflows"):
            try:
                body = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                issues.append(f"工作流不是 UTF-8 文本：{relative}")
                continue
            if REUSABLE_WORKFLOW.search(body):
                issues.append(f"工作流引用了其他仓库的可复用发布流程：{relative}")

    if issues:
        print("独立性检查失败：", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print("独立性检查通过：无 submodule、gitlink、源仓库历史或部署密钥依赖。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
