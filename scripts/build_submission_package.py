#!/usr/bin/env python3
"""Build the local A09 E8-E12 submission ZIP (source + docs + evidence)."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT.parent / f"A09_E11-E12_提交包_{datetime.now():%Y%m%d}.zip"
INCLUDE = [
    "README.md", "B组交接材料.md", "Makefile", "compose.yaml",
    "requirements-dev.in", "requirements-dev.lock", "run_lab.py", "run_e11e12.py",
    "ci", "docs", "evidence", "labs", "services", "scripts", "tests", "templates",
    "fixtures", ".github",
]
EXCLUDE_PARTS = {".git", "__pycache__", "work", "data", "node_modules", ".venv",
                 ".idea", ".pytest_cache", ".mypy_cache", "*.pyc"}


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def excluded(path):
    return any(part in EXCLUDE_PARTS or part.endswith(".pyc") for part in path.parts)


def collect():
    files = []
    for name in INCLUDE:
        path = ROOT / name
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
        else:
            files.extend(item for item in path.rglob("*")
                         if item.is_file() and not excluded(item.relative_to(ROOT)))
    extra = ROOT.parent / "PR_241880089.md"
    if extra.is_file():
        files.append(extra)
    unique = {}
    for path in files:
        arc = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.name
        unique[arc] = path
    return dict(sorted(unique.items()))


def git_value(*args):
    proc = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    out = Path(args.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise SystemExit(f"Refusing to overwrite existing package: {out}")

    files = collect()
    entries = []
    manifest_lines = []
    for arc, path in files.items():
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        entries.append((arc, data))
        manifest_lines.append(f"{digest}  {arc}")

    audit_path = ROOT / "docs/reports/A09-E11-E12-audit.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8")) if audit_path.is_file() else None
    dirty = [line for line in git_value("status", "--porcelain").splitlines() if line.strip()]
    info = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "scope": "A09 E8-E12 source, documents, evidence and audit",
        "branch": git_value("rev-parse", "--abbrev-ref", "HEAD"),
        "head": git_value("rev-parse", "HEAD"),
        "worktree_dirty": bool(dirty),
        "uncommitted_entries": len(dirty),
        "file_count": len(entries) + 3,
        "source_bytes": sum(len(data) for _, data in entries),
        "audit_summary": audit.get("summary") if audit else None,
        "note": "241880374 evidence directory is absent; see docs/reports/A09-E11-E12-audit.md",
    }
    info_data = (json.dumps(info, ensure_ascii=False, indent=2) + "\n").encode()
    manifest_data = ("\n".join(manifest_lines) + "\n").encode()

    groups = {}
    for arc, data in entries:
        top = arc.split("/", 1)[0] if "/" in arc else "(root)"
        groups.setdefault(top, {"count": 0, "bytes": 0})
        groups[top]["count"] += 1
        groups[top]["bytes"] += len(data)
    checklist = [
        "# A09 E11–E12 提交包清单",
        "",
        f"- 生成时间：{info['generated_at']}",
        f"- 分支：`{info['branch']}`",
        f"- HEAD：`{info['head']}`",
        f"- 文件数：{info['file_count']}（含本清单、`ARCHIVE-INFO.json`、`MANIFEST.sha256`）",
        f"- 源文件字节数：{info['source_bytes']}",
        f"- 工作区未提交改动：{info['uncommitted_entries']} 项" if info["worktree_dirty"] else "- 工作区：干净",
        "",
        "## 包含范围",
        "",
        "| 顶层路径 | 文件数 | 字节数 |",
        "|---|---:|---:|",
    ]
    for top, stat in sorted(groups.items()):
        checklist.append(f"| `{top}` | {stat['count']} | {stat['bytes']} |")
    checklist += [
        "",
        "## 归档检查结论",
        "",
    ]
    if audit:
        summary = audit["summary"]
        checklist.append(f"- `docs/reports/A09-E11-E12-audit.md`：{summary['pass']} PASS / "
                         f"{summary['warn']} WARN / {summary['fail']} FAIL（共 {summary['checks']} 项）。")
        checklist.append("- WARN：马海川 241880374 的 `evidence/students/241880374/e11-e12/` 缺失；"
                         "报告已归档但无法按 SHA256 复核，本次未代造证据。")
    checklist += [
        "- 所有证据的逐文件哈希见 `MANIFEST.sha256`；原始证据目录内另有各自的 `SHA256SUMS`。",
        "",
        "## 复核方式",
        "",
        "```bash",
        "python3 scripts/audit_e11_e12.py",
        "sha256sum -c MANIFEST.sha256   # 解压后于包根执行",
        "```",
        "",
    ]
    checklist_data = ("\n".join(checklist)).encode()

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for arc, data in entries:
            archive.writestr(arc, data)
        archive.writestr("ARCHIVE-INFO.json", info_data)
        archive.writestr("MANIFEST.sha256", manifest_data)
        archive.writestr("提交包清单.md", checklist_data)

    zip_sha = sha256_file(out)
    sidecar = out.with_suffix(out.suffix + ".sha256")
    sidecar.write_text(f"{zip_sha}  {out.name}\n", encoding="utf-8")
    with zipfile.ZipFile(out) as archive:
        bad = archive.testzip()
    print(json.dumps({
        "package": str(out),
        "bytes": out.stat().st_size,
        "sha256": zip_sha,
        "sidecar": str(sidecar),
        "entries": len(entries) + 3,
        "testzip": bad,
        "audit_summary": info["audit_summary"],
    }, ensure_ascii=False, indent=2))
    return 0 if bad is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
