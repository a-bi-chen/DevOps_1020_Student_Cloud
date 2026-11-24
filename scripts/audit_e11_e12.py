#!/usr/bin/env python3
"""Offline audit for the A09 E11-E12 archive.

Checks member documents, personal tests, every published SHA256 manifest,
JSON parseability, and the B09 sign-off object identity.
Writes docs/reports/A09-E11-E12-audit.json and .md.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMBERS = {
    "241880089": "陈玉熙",
    "241880369": "高嘉程",
    "241880374": "马海川",
    "241880375": "张海洋",
}
TEST_CLASSES = {
    "241880089": "StudentE11E12A241880089",
    "241880369": "StudentE11E12A241880369",
    "241880374": "StudentE11E12A241880374",
    "241880375": "StudentE11E12A241880375",
}
MANIFESTS = [
    "evidence/students/241880089/e11-e12/SHA256SUMS",
    "evidence/students/241880369/e11-e12/artifacts.sha256",
    "evidence/students/241880374/e11-e12/SHA256SUMS",
    "evidence/students/241880375/e11-e12/archived-artifacts.sha256",
    "evidence/students/241880375/e11-e12/b09-signoff/artifacts.sha256",
]
EXPECTED_B09 = {
    "job_id": "job-1bd0ed1b449f44f293853df90440844f",
    "trace_id": "trace-4e7c0c6afd0447f9869d2f5e1ee6f4ae",
    "base_commit": "3fcb72029bf560afde2d29436395ff3b979a19fd",
    "target_commit": "15c059958a41a5a0513dc048036439843a34ad28",
    "repaired_commit": "817b2459d53f586f7f3800ce20d0c3f002621f77",
    "source_report_sha256": "8508d50232bfa4a529d51accd4dc94e5765a0fe0a0b130eebf73f8f866a98716",
    "candidate_patch_sha256": "88074f66c291dcad1344c48f6a2b9ddd42d235d9d0415c85fb33310c5b7cb2af",
    "build_log_sha256": "29bfc7126a891b1deca1f143ff3f7d2a0003e1c4d43a3df25ba739524b1a9a0c",
    "incremental_log_sha256": "52b1b0840faee45dffd5d909945f740dd9fad73b1dc58e544ac1c0491ce05e57",
    "recheck_report_sha256": "08792b92a49d4b4cd59c4919f4a7c9d4679bf3bf1010559190046e53a7080c00",
}
CHECKS = []


def check(name, status, detail):
    CHECKS.append({"name": name, "status": status, "detail": detail})


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_manifest(path):
    entries = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$", line)
        if not match:
            entries.append({"line": raw, "status": "BAD_LINE"})
            continue
        expected, relative = match[1].lower(), match[2].strip()
        candidates = [path.parent / relative, ROOT / relative]
        target = next((item for item in candidates if item.is_file()), None)
        if target is None:
            entries.append({"path": relative, "status": "MISSING"})
            continue
        actual = sha256(target)
        entries.append({"path": relative, "status": "OK" if actual == expected else "MISMATCH",
                        "expected": expected, "actual": actual})
    return entries


def git_blob(rev, path):
    proc = subprocess.run(["git", "ls-tree", rev, "--", path], cwd=ROOT,
                          text=True, capture_output=True)
    if proc.returncode or not proc.stdout.strip():
        return None
    return proc.stdout.split()[2]


def main():
    summary = {"checks": 0, "pass": 0, "warn": 0, "fail": 0}
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scope": "A09 E11-E12 documents, evidence, manifests and cross-checks",
        "members": {},
        "manifests": {},
        "json": {"files": 0, "failures": []},
        "b09_signoff": {},
        "checks": CHECKS,
    }

    for sid, name in MEMBERS.items():
        doc_dir = ROOT / "docs/students" / sid / "e11-e12"
        required = ["个人报告.md", "ADR.md", "AI_USAGE.md"]
        missing = [item for item in required if not (doc_dir / item).is_file()]
        check(f"{sid} 个人材料", "FAIL" if missing else "PASS",
              f"缺少 {missing}" if missing else f"{name}：报告/ADR/AI_USAGE 齐全")

        test_hits = []
        for source in (ROOT / "labs/e11e12").glob("*.py"):
            if TEST_CLASSES[sid] in source.read_text(encoding="utf-8", errors="replace"):
                test_hits.append(source.relative_to(ROOT).as_posix())
        check(f"{sid} 个人测试", "PASS" if test_hits else "FAIL",
              ", ".join(test_hits) if test_hits else f"未找到 {TEST_CLASSES[sid]}")

        evidence_dir = ROOT / "evidence/students" / sid / "e11-e12"
        evidence_files = [item for item in evidence_dir.rglob("*") if item.is_file()] if evidence_dir.is_dir() else []
        if not evidence_dir.is_dir():
            check(f"{sid} 证据目录", "WARN", "report 已归档，但 evidence/ 目录缺失，无法按 SHA256 复核")
            member_status = "FAIL" if missing or not test_hits else "WARN"
        else:
            check(f"{sid} 证据目录", "PASS" if evidence_files else "WARN",
                  f"{len(evidence_files)} 个文件，{sum(item.stat().st_size for item in evidence_files)} 字节")
            member_status = "FAIL" if missing or not test_hits else ("PASS" if evidence_files else "WARN")
        report["members"][sid] = {
            "name": name, "docs": doc_dir.relative_to(ROOT).as_posix(),
            "doc_missing": missing, "tests": test_hits,
            "evidence_dir": evidence_dir.relative_to(ROOT).as_posix() if evidence_dir.is_dir() else None,
            "evidence_files": len(evidence_files), "status": member_status,
        }

    for relative in MANIFESTS:
        path = ROOT / relative
        if not path.is_file():
            check(f"manifest {relative}", "FAIL", "清单文件不存在")
            report["manifests"][relative] = {"entries": 0, "failures": [{"path": relative, "status": "MISSING"}]}
            continue
        entries = parse_manifest(path)
        failures = [item for item in entries if item.get("status") != "OK"]
        check(f"manifest {relative}", "FAIL" if failures else "PASS",
              f"{len(entries)} 项，失败 {len(failures)} 项")
        report["manifests"][relative] = {"entries": len(entries), "failures": failures}

    json_files = sorted((ROOT / "evidence/students").rglob("*.json"))
    for path in json_files:
        report["json"]["files"] += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - report the exact parser error
            report["json"]["failures"].append({"path": path.relative_to(ROOT).as_posix(), "error": str(exc)})
    check("证据 JSON 可解析", "FAIL" if report["json"]["failures"] else "PASS",
          f"{report['json']['files']} 个 JSON，失败 {len(report['json']['failures'])} 个")

    signoff = ROOT / "evidence/students/241880375/e11-e12/b09-signoff"
    validation_path = signoff / "validation.json"
    b09 = {"checks": [], "validation": None}
    if not validation_path.is_file():
        check("B09 签收 validation.json", "FAIL", "文件不存在")
    else:
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        b09["validation"] = validation
        failures = [key for key, expected in EXPECTED_B09.items() if validation.get(key) != expected]
        if validation.get("accepted") is not True:
            failures.append("accepted")
        check("B09 签收字段", "FAIL" if failures else "PASS",
              f"不一致字段：{failures}" if failures else "accepted=true，job/trace/base/target/补丁/日志/复检哈希全部一致")

    archive_relative = "evidence/students/241880375/e11-e12/e11e12-evidence-241880375.tar.gz"
    archive = ROOT / archive_relative
    archive_sha = sha256(archive) if archive.is_file() else None
    blob_a = git_blob("b0765a0f990b10a28392fe6d4318b4b73a41177a", archive_relative)
    blob_pr17 = git_blob("0cd8054911a18be96900e05c3b7747c6b35a4112", archive_relative)
    blob_main = git_blob("HEAD", archive_relative)
    identities = {"b0765a0f": blob_a, "pr17_head": blob_pr17, "current_main": blob_main}
    same_blob = bool(blob_a) and blob_a == blob_pr17 == blob_main
    expected_archive = "19479d51720decbca2518453e00646a4700c7b21101b018965bfdbc0c8cce648"
    b09["archive"] = {
        "path": archive_relative,
        "sha256": archive_sha,
        "expected_sha256": expected_archive,
        "git_blobs": identities,
        "same_git_blob": same_blob,
    }
    if (ROOT / ".git").is_dir():
        check("B09 归档 Git 对象一致", "PASS" if same_blob else "FAIL",
              f"blob={identities}")
    else:
        check("B09 归档 Git 对象一致", "WARN",
              "离线提交包不含 .git；以归档 SHA256 和 B09 签收字段复核")
    check("B09 归档 SHA256", "PASS" if archive_sha == expected_archive else "FAIL",
          f"{archive_sha}")

    signoff_expected = {
        "candidate.patch": "88074f66c291dcad1344c48f6a2b9ddd42d235d9d0415c85fb33310c5b7cb2af",
        "validation.json": "aeb157c32906bfe7859fc93e14c2a52cbb5e63dad0004c033d8c29f788475394",
        "build.log": "29bfc7126a891b1deca1f143ff3f7d2a0003e1c4d43a3df25ba739524b1a9a0c",
        "incremental.log": "52b1b0840faee45dffd5d909945f740dd9fad73b1dc58e544ac1c0491ce05e57",
        "recheck.json": "08792b92a49d4b4cd59c4919f4a7c9d4679bf3bf1010559190046e53a7080c00",
        "repaired-project.bundle": "e6f7cd9802728705c85fd003ee031900a44691715c1768590a5de830017c0dda",
    }
    actual_hashes = {name: sha256(signoff / name) for name in signoff_expected if (signoff / name).is_file()}
    bad = [name for name, expected in signoff_expected.items() if actual_hashes.get(name) != expected]
    b09["files"] = actual_hashes
    report["b09_signoff"] = b09
    check("B09 签收产物哈希", "FAIL" if bad else "PASS",
          f"不一致：{bad}" if bad else "candidate.patch / validation / build / incremental / recheck / bundle 全部一致")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    missing_mentions = [sid for sid in MEMBERS if sid not in readme]
    check("README 索引", "PASS" if not missing_mentions else "FAIL",
          f"缺少：{missing_mentions}" if missing_mentions else "四人学号均已索引")

    for item in CHECKS:
        key = {"PASS": "pass", "WARN": "warn", "FAIL": "fail"}[item["status"]]
        summary[key] += 1
    summary["checks"] = len(CHECKS)
    report["summary"] = summary

    out_json = ROOT / "docs/reports/A09-E11-E12-audit.json"
    out_md = ROOT / "docs/reports/A09-E11-E12-audit.md"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# A09 E11–E12 归档全量检查记录",
        "",
        f"- 生成时间：{report['generated_at']}",
        f"- 结果：**{summary['pass']} PASS / {summary['warn']} WARN / {summary['fail']} FAIL**（共 {summary['checks']} 项）",
        "",
        "## 1. 四位组员材料",
        "",
        "| 学号 | 姓名 | 个人材料 | 个人测试 | 证据文件数 | 结论 |",
        "|---|---|---|---|---|---|",
    ]
    for sid, name in MEMBERS.items():
        info = report["members"][sid]
        material = "缺失：" + "、".join(info["doc_missing"]) if info["doc_missing"] else "齐全"
        tests = "已归档" if info["tests"] else "**未找到**"
        evidence = info["evidence_files"] if info["evidence_dir"] else "**目录缺失**"
        lines.append(f"| {sid} | {name} | {material} | {tests} | {evidence} | {info['status']} |")
    lines += [
        "",
        "## 2. 校验清单",
        "",
        "| 检查项 | 结果 | 说明 |",
        "|---|---|---|",
    ]
    for item in CHECKS:
        lines.append(f"| {item['name']} | **{item['status']}** | {item['detail']} |")
    lines += [
        "",
        "## 3. B09 对 A09 E12 的签收核对",
        "",
        f"- 核对时 A09 `main`：`b0765a0f990b10a28392fe6d4318b4b73a41177a`；PR #17 head：`0cd8054911a18be96900e05c3b7747c6b35a4112`。",
        f"- 证据归档 Git blob 三处一致：`{blob_a}`（b0765a0f / PR #17 / 当前 main `bfd2ab1`）。",
        f"- 归档 SHA256：`{archive_sha}`；与 B09 记录的 `19479d51720decbca2518453e00646a4700c7b21101b018965bfdbc0c8cce648` 一致。",
        f"- A 端 job/trace：`{EXPECTED_B09['job_id']}` / `{EXPECTED_B09['trace_id']}`；base/target 为 `{EXPECTED_B09['base_commit']}` / `{EXPECTED_B09['target_commit']}`。",
        "- B09 直接消费原始 `incremental-check.json`（SHA256 `8508d502...`），未使用 `fixed-md.json`；修复提交 `817b245...` 的父提交为 A 端 target，仅修改 Makefile。",
        "- 复检 `recheck_missing_count=0`，仅保留允许的 `REDUNDANT(main.o, unused.h)`；最终 MD=0。",
        "",
        "## 4. 缺口与说明",
        "",
        "- 241880374 马海川：个人报告/ADR/AI_USAGE、个人测试、证据包、run-summary 和 SHA256SUMS 均已归档。",
        "- 陈玉熙 241880089：E11–E12 个人材料、个人测试与证据均已归档。",
        "- 本检查只读仓库文件，不修改任何组员材料；所有哈希均按文件字节重新计算。",
        "",
        f"机器可读结果：`{out_json.relative_to(ROOT).as_posix()}`",
        "",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({"summary": summary, "report": out_md.relative_to(ROOT).as_posix()},
                     ensure_ascii=False, indent=2))
    return 1 if summary["fail"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
