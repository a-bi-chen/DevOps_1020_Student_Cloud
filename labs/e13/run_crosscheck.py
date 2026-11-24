#!/usr/bin/env python3
"""E13 cross-project check adapter (A09 BuildChecker/EChecker -> B09 fixture).

The stock E11-E12 entry snapshots the repository root and the EChecker scan
profile only accepts -O0/-O1.  B09's project lives in a subdirectory and uses
-std=c11 -Wall -Wextra -Werror, so this adapter:

* checks out the two original B09 commit hashes unchanged;
* treats fixtures/e11e12-b1-real as the project root;
* keeps BuildChecker's full_check unchanged;
* applies the same EChecker scan algorithm with a documented E13 flag profile;
* records the stock entry's actual failure modes instead of hiding them.

Run on Linux with git/make/gcc/strace available.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "labs/e8e10"), str(ROOT / "services/buildchecker")]
import lab  # noqa: E402
from buildchecker.fullcheck import full_check  # noqa: E402

SCHEMA = "e13-1"
PROFILE = "GCC_LOCAL_HEADERS_EXPLICIT_MAKE_E13_B09"
ALLOWED_FLAGS = {"-std=c11 -Wall -Wextra -Werror"}
TARGETS = (("main.o", "main.c"), ("helper.o", "helper.c"))


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(argv, cwd, log, timeout=120, env=None):
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    try:
        proc = subprocess.run(
            [str(x) for x in argv],
            cwd=str(cwd),
            text=True,
            capture_output=True,
            timeout=timeout,
            env=env,
        )
        record = {
            "argv": [str(x) for x in argv],
            "cwd": str(cwd),
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "elapsed_s": round(time.monotonic() - started, 3),
        }
    except subprocess.TimeoutExpired as exc:
        record = {
            "argv": [str(x) for x in argv],
            "cwd": str(cwd),
            "exit_code": None,
            "stdout": (exc.stdout or "").decode() if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
            "stderr": ((exc.stderr or "").decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")) + "\nTIMEOUT",
            "elapsed_s": round(time.monotonic() - started, 3),
        }
    lines = ["$ " + " ".join(record["argv"]), f"cwd={record['cwd']}", f"exit={record['exit_code']}"]
    if record["stdout"]:
        lines += ["[stdout]", record["stdout"].rstrip("\n")]
    if record["stderr"]:
        lines += ["[stderr]", record["stderr"].rstrip("\n")]
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return record


def git(argv, cwd):
    proc = subprocess.run(["git", *argv], cwd=str(cwd), text=True, capture_output=True)
    if proc.returncode:
        raise RuntimeError(f"git {' '.join(argv)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def snapshot(repo, commit, dest, subdir, out):
    dest = Path(dest)
    if dest.exists():
        raise RuntimeError(f"snapshot destination already exists: {dest}")
    cloned = run(["git", "clone", "--no-hardlinks", "--no-checkout", str(repo), str(dest)],
                 ROOT, out / f"{dest.name}-clone.log", timeout=300)
    if cloned["exit_code"] != 0:
        raise RuntimeError(f"clone failed: {cloned['stderr'].strip()}")
    checked = run(["git", "checkout", "--detach", commit], dest, out / f"{dest.name}-checkout.log", timeout=120)
    if checked["exit_code"] != 0:
        raise RuntimeError(f"checkout failed: {checked['stderr'].strip()}")
    actual = git(["rev-parse", "HEAD"], dest)
    if actual != commit:
        raise RuntimeError(f"commit mismatch: requested {commit}, checked out {actual}")
    project = dest / subdir
    names = {item.name for item in project.glob("*.c")}
    if names != {"main.c", "helper.c"} or not (project / "config.h").is_file():
        raise RuntimeError("project does not match the E8-E10/E13 profile layout")
    log = git(["log", "-1", "--format=%H%x20%ci%x20%s"], dest)
    return project, actual, log


def run_project_commands(project, outdir, expected_output):
    outdir.mkdir(parents=True, exist_ok=True)
    result = {}
    steps = [
        ("make_clean", ["make", "clean"], 120),
        ("make", ["make"], 120),
        ("make_test", ["make", "test"], 120),
        ("app", ["./app"], 30),
    ]
    for name, argv, timeout in steps:
        result[name] = run(argv, project, outdir / f"{name}.log", timeout=timeout)
    result["make_clean_and_make_ok"] = (
        result["make_clean"]["exit_code"] == 0 and result["make"]["exit_code"] == 0
    )
    result["make_test_ok"] = result["make_test"]["exit_code"] == 0
    result["app_ok"] = result["app"]["exit_code"] == 0
    result["expected_output"] = expected_output
    result["app_stdout"] = result["app"]["stdout"]
    result["output_matches"] = result["app"]["stdout"].strip() == expected_output
    result["app_stdout_sha256"] = hashlib.sha256(result["app"]["stdout"].encode()).hexdigest()
    save(outdir / "commands.json", result)
    return result


def declarations_e13(project):
    """lab.declarations() only accepts '='; B09 uses '?=' and ':='."""
    text = (project / "Makefile").read_text()
    variables = {}
    for match in re.finditer(r"^(\w+)\s*(?:\?=|:=|=)\s*(.*)$", text, re.M):
        variables[match[1]] = match[2]
    graph = {}
    for target, _source in TARGETS:
        match = re.search(r"^" + re.escape(target) + r": ([^\n]*)$", text, re.M)
        if not match:
            raise ValueError(f"UNSUPPORTED_RULE {target}")
        deps = match[1]
        for _ in range(8):
            deps = re.sub(r"\$\((\w+)\)", lambda item: variables.get(item[1], item[0]), deps)
        if "$" in deps or "%" in deps or "|" in deps:
            raise ValueError("UNSUPPORTED_DECLARATION")
        graph[target] = sorted(set(deps.split()))
    return graph, variables.get("CFLAGS", "")


def scan_e13(project, old=None):
    """Same algorithm as labs/e8e10/lab.py scan, with the E13 flag profile."""
    started = time.perf_counter()
    declared, flags = declarations_e13(project)
    if flags not in ALLOWED_FLAGS:
        raise ValueError(f"UNSUPPORTED_FLAGS {flags}")
    files = {x.name: x.read_text() for x in sorted(project.glob("*")) if x.suffix in [".c", ".h"]}
    key = {
        "directives": {name: [line for line in text.splitlines() if line.lstrip().startswith("#")]
                       for name, text in files.items()},
        "recipes": [line for line in (project / "Makefile").read_text().splitlines() if line.startswith("\t")],
        "flags": flags,
        "compiler": lab.run(["gcc", "--version"], project).splitlines()[0],
    }
    actual, refreshed, reused = {}, [], []
    for target, source in TARGETS:
        if old and old.get("key") == key and target in old.get("actual", {}):
            actual[target] = old["actual"][target]
            reused.append(target)
        else:
            output = lab.run(["gcc", *flags.split(), "-MM", "-MT", target, source], project)
            actual[target] = sorted(set(output.replace("\\\n", " ").split(":", 1)[1].split()))
            refreshed.append(target)
    findings = []
    for target in actual:
        for kind, edges in [
            ("MISSING", set(actual[target]) - set(declared[target])),
            ("REDUNDANT", set(declared[target]) - set(actual[target])),
        ]:
            findings.extend({"type": kind, "target": target, "dependency": dep} for dep in sorted(edges))
    current = {(f["type"], f["target"], f["dependency"]) for f in findings}
    previous = {(f["type"], f["target"], f["dependency"]) for f in old["findings"]} if old else set()
    return {
        "schema_version": SCHEMA,
        "profile": PROFILE,
        "commit": git(["rev-parse", "HEAD"], project),
        "key": key,
        "actual": actual,
        "declared": declared,
        "findings": findings,
        "added": [list(item) for item in sorted(current - previous)],
        "resolved": [list(item) for item in sorted(previous - current)],
        "refreshed": refreshed,
        "reused": reused,
        "elapsed_s": round(time.perf_counter() - started, 4),
    }


def normalized(findings):
    return sorted((f["type"], f["target"], f["dependency"])
                  for f in findings if f["target"] in ("main.o", "helper.o"))


def probe_stock_entry(repo, subdir, base, target, out):
    probes = {}
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([
        str(ROOT / "services/buildchecker"), str(ROOT / "labs/e8e10"),
        str(ROOT / "labs/e11e12"), env.get("PYTHONPATH", ""),
    ])
    for label, repo_arg in (("subdir", str((repo / subdir).resolve())), ("root", str(repo.resolve()))):
        request = {"mode": "e11-a", "repo": repo_arg, "base": base, "target": target}
        request_path = out / f"official-entry-{label}-request.json"
        save(request_path, request)
        result = run(
            [sys.executable, str(ROOT / "labs/e11e12/pipeline.py"),
             "--request", str(request_path), "--out", str(out / f"official-entry-{label}")],
            ROOT, out / f"official-entry-{label}.log", timeout=300, env=env,
        )
        stderr_lines = [line for line in result["stderr"].strip().splitlines() if line.strip()]
        error = {}
        try:
            error = json.loads(result["stdout"]).get("error", {})
        except json.JSONDecodeError:
            pass
        probes[label] = {
            "repo": repo_arg,
            "exit_code": result["exit_code"],
            "error_code": error.get("code", ""),
            "error_message": error.get("message", ""),
            "last_error_line": stderr_lines[-1] if stderr_lines else "",
            "log": f"official-entry-{label}.log",
        }
    try:
        lab.scan(out / "target-project" / subdir)
        probes["stock_scan"] = {"status": "ACCEPTED", "error": ""}
    except Exception as exc:  # noqa: BLE001 - the exact rejection text is the evidence
        probes["stock_scan"] = {"status": "REJECTED", "error": f"{type(exc).__name__}: {exc}"}
    save(out / "entry-probes.json", probes)
    return probes


def artifact_hashes(out, names):
    return {name: sha256(out / name) for name in names if (out / name).is_file()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="B09 repository root")
    parser.add_argument("--subdir", default="fixtures/e11e12-b1-real")
    parser.add_argument("--base", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--expected-output", default="hello E3")
    parser.add_argument("--skip-probe", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    subdir = Path(args.subdir)
    out = Path(args.out).resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"Output must be a fresh empty directory: {out}")
    out.mkdir(parents=True, exist_ok=True)
    save(out / "request.json", {
        "schema_version": SCHEMA,
        "requestor": "B09",
        "repo": str(repo),
        "subdir": subdir.as_posix(),
        "base": args.base,
        "target": args.target,
        "expected_output": args.expected_output,
        "expected": {"base_findings": [], "target_findings": [["MISSING", "main.o", "extra.h"]]},
        "started_at": now(),
    })

    base_project, base_commit, base_log = snapshot(repo, args.base, out / "base-project", subdir, out)
    target_project, target_commit, target_log = snapshot(repo, args.target, out / "target-project", subdir, out)
    repo_head = git(["rev-parse", "HEAD"], repo)

    base_commands = run_project_commands(base_project, out / "commands-base", args.expected_output)
    target_commands = run_project_commands(target_project, out / "commands-target", args.expected_output)

    base_full = full_check(base_project, out / "baseline-full",
                           clean_command="make clean", build_command="make app", timeout=120)
    target_full = full_check(target_project, out / "target-full",
                             clean_command="make clean", build_command="make app", timeout=120)
    save(out / "buildchecker-base.json", {
        "schema_version": SCHEMA, "commit": base_commit, "status": base_full.get("status"),
        "findings": base_full.get("findings", []), "report": base_full,
    })
    save(out / "buildchecker-target.json", {
        "schema_version": SCHEMA, "commit": target_commit, "status": target_full.get("status"),
        "findings": target_full.get("findings", []), "report": target_full,
    })

    baseline = scan_e13(base_project)
    save(out / "baseline-cache.json", baseline)
    incremental = scan_e13(target_project, baseline)
    save(out / "incremental-check.json", incremental)

    incremental_findings = normalized(incremental["findings"])
    target_full_findings = normalized(target_full.get("findings", []))
    base_full_findings = normalized(base_full.get("findings", []))
    expected_base = []
    expected_target = [("MISSING", "main.o", "extra.h")]
    consistency = incremental_findings == target_full_findings
    expectations = {
        "base_no_findings": base_full_findings == expected_base,
        "target_expected_findings": target_full_findings == expected_target,
        "incremental_matches_target_full": consistency,
        "incremental_only_expected_addition": incremental["added"] == [["MISSING", "main.o", "extra.h"]],
        "base_commands_ok": all(base_commands[k] for k in ("make_clean_and_make_ok", "make_test_ok", "app_ok", "output_matches")),
        "target_commands_ok": all(target_commands[k] for k in ("make_clean_and_make_ok", "make_test_ok", "app_ok", "output_matches")),
        "commits_unchanged": base_commit == args.base and target_commit == args.target,
    }

    probes = {} if args.skip_probe else probe_stock_entry(repo, subdir, args.base, args.target, out)
    status = "SUCCEEDED" if all(expectations.values()) and all(
        item.get("status") == "SUCCEEDED" for item in (base_full, target_full)
    ) else "FAILED"

    report = {
        "schema_version": SCHEMA,
        "kind": "crosscheck",
        "generated_at": now(),
        "responder": "A09",
        "requestor": "B09 (https://github.com/llxxy-cn/devops-b09)",
        "status": status,
        "project": {
            "repo": str(repo),
            "repo_head": repo_head,
            "subdir": subdir.as_posix(),
            "base_commit": base_commit,
            "base_commit_log": base_log,
            "target_commit": target_commit,
            "target_commit_log": target_log,
        },
        "environment": {
            "python": sys.version.split()[0],
            "gcc": lab.run(["gcc", "--version"], ROOT).splitlines()[0],
            "make": lab.run(["make", "--version"], ROOT).splitlines()[0],
            "strace": lab.run(["strace", "--version"], ROOT).splitlines()[0],
            "detector": base_full.get("detector"),
            "detector_version": base_full.get("detector_version"),
        },
        "entry_compatibility": {
            "official_pipeline_subdir": probes.get("subdir"),
            "official_pipeline_root": probes.get("root"),
            "official_echecker_scan": probes.get("stock_scan"),
            "adapter": f"labs/e13/run_crosscheck.py ({PROFILE}); original commit hashes preserved",
        },
        "commands": {"base": base_commands, "target": target_commands},
        "buildchecker": {
            "base": {"status": base_full.get("status"), "findings": base_full_findings},
            "target": {"status": target_full.get("status"), "findings": target_full_findings},
        },
        "echecker": {
            "profile": PROFILE,
            "baseline_findings": normalized(baseline["findings"]),
            "incremental_findings": incremental_findings,
            "added": incremental["added"],
            "resolved": incremental["resolved"],
            "refreshed": incremental["refreshed"],
            "reused": incremental["reused"],
            "target_full_reference": target_full_findings,
            "consistent": consistency,
        },
        "expectations": expectations,
        "expected": {
            "base_findings": [],
            "target_findings": [list(item) for item in expected_target],
            "program_output": args.expected_output,
        },
        "artifacts": artifact_hashes(out, [
            "baseline-cache.json", "incremental-check.json", "buildchecker-base.json",
            "buildchecker-target.json", "entry-probes.json", "commands-base/commands.json",
            "commands-target/commands.json", "baseline-full/findings.json", "target-full/findings.json",
        ]),
    }
    save(out / "detection-report.json", report)

    lines = [
        "# E13 B09 交叉检测报告（A09 BuildChecker / EChecker）",
        "",
        f"- 生成时间：{report['generated_at']}",
        f"- 结论：**{status}**",
        "- 请求方：B09，仓库 <https://github.com/llxxy-cn/devops-b09>",
        f"- 项目子目录：`{subdir.as_posix()}`",
        f"- Base（原始提交，未改写）：`{base_commit}`",
        f"- Target（原始提交，未改写）：`{target_commit}`",
        f"- B09 仓库当前 HEAD：`{repo_head}`",
        "",
        "## 1. 检测入口兼容性",
        "",
        "| 入口 | 结果 | 证据 |",
        "|---|---|---|",
    ]
    for key, label in (("subdir", "官方 pipeline，repo 指向子目录"),
                       ("root", "官方 pipeline，repo 指向仓库根"),
                       ("stock_scan", "官方 EChecker scan，直接扫子目录")):
        item = probes.get(key, {})
        if key == "stock_scan":
            lines.append(f"| {label} | `{item.get('status', 'NOT_RUN')}`：{item.get('error', '')} | `entry-probes.json` |")
        else:
            detail = item.get("error_code", "") or item.get("last_error_line", "")
            if item.get("error_message"):
                detail = f"{detail}: {item['error_message']}"
            lines.append(f"| {label} | 退出码 `{item.get('exit_code')}`：`{detail}` | `{item.get('log', '')}` |")
    lines += [
        "",
        "官方入口不能直接以该子目录运行：E11-E12 `snapshot()` 以仓库根为项目根，"
        "EChecker `scan()` 的 flags 白名单也不含 B09 的 `-std=c11 -Wall -Wextra -Werror`。"
        f"本报告使用 `{PROFILE}` 适配配置：保留 BuildChecker `full_check` 原实现，"
        "按同一 EChecker 算法（Makefile 声明 vs `gcc -MM` 实际依赖、保守缓存失效、added/resolved）执行增量检测。",
        "",
        "## 2. 原始项目命令与输出",
        "",
        "| 项目 | make clean && make | make test | ./app | 输出 | 期望输出匹配 |",
        "|---|---|---|---|---|---|",
    ]
    for label, commands in (("Base", base_commands), ("Target", target_commands)):
        lines.append(
            f"| {label} | {'PASS' if commands['make_clean_and_make_ok'] else 'FAIL'} "
            f"| {'PASS' if commands['make_test_ok'] else 'FAIL'} "
            f"| {'PASS' if commands['app_ok'] else 'FAIL'} "
            f"| `{commands['app_stdout'].strip()}` | {commands['output_matches']} |"
        )
    lines += [
        "",
        "## 3. BuildChecker 全量检测",
        "",
        "| 项目 | 状态 | 依赖缺陷（main.o/helper.o） |",
        "|---|---|---|",
        f"| Base | `{base_full.get('status')}` | `{base_full_findings}` |",
        f"| Target | `{target_full.get('status')}` | `{target_full_findings}` |",
        "",
        "## 4. EChecker 增量检测",
        "",
        f"- 基线缓存：`baseline-cache.json`；目标增量：`incremental-check.json`",
        f"- 增量 findings：`{incremental_findings}`",
        f"- 新增：`{incremental['added']}`；解决：`{incremental['resolved']}`",
        f"- 刷新目标：`{incremental['refreshed']}`；复用目标：`{incremental['reused']}`",
        f"- 与目标全量结果一致：**{consistency}**",
        "",
        "## 5. 预期核对",
        "",
        "| 检查项 | 结果 |",
        "|---|---|",
    ]
    for key, value in expectations.items():
        lines.append(f"| `{key}` | {value} |")
    lines += [
        "",
        "## 6. 交付说明",
        "",
        "- 两个原始提交号均已通过 `git checkout --detach <sha>` 与 `git rev-parse HEAD` 双重核对；未对 B09 仓库做任何提交或改写。",
        "- BuildChecker 的全量报告、实际依赖图、声明依赖图、make 数据库和原始 trace 保存在 `baseline-full/`、`target-full/`。",
        "- 命令日志保存在 `commands-base/`、`commands-target/`；入口兼容性原始日志保存在 `official-entry-*.log`。",
        "- 文件校验见 `SHA256SUMS`。",
        "",
    ]
    (out / "detection-report.md").write_text("\n".join(lines), encoding="utf-8")

    files = sorted(path for path in out.rglob("*") if path.is_file()
                   and not any(part in {"base-project", "target-project"} for part in path.parts))
    checksum_lines = [f"{sha256(path)}  {path.relative_to(out).as_posix()}" for path in files]
    (out / "SHA256SUMS").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "out": str(out), "expectations": expectations,
                      "findings": incremental_findings}, ensure_ascii=False, indent=2))
    return 0 if status == "SUCCEEDED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
