"""Independent E8/E10 A-track checks on the archived CI artifact.

E8:  BuildChecker actual graph vs GCC -MM full scan on the same C0 tree.
E10: all 30 incremental/full rows equal; final BuildChecker graph/findings vs
     a fresh GCC -MM scan of the final tree.
"""
import csv
import json
import shutil
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
artifact = Path(sys.argv[2]).resolve()
out = Path(sys.argv[3]).resolve()
sys.path.insert(0, str(repo / "labs" / "e8e10"))
import lab  # noqa: E402

if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)


def normalize_findings(findings):
    return sorted((f["type"], f["target"], f["dependency"]) for f in findings)


def project_graph(edges):
    return {
        target: sorted({e["dependency"] for e in edges if e["target"] == target})
        for target in ("main.o", "helper.o")
    }


def fresh_scan(source, name):
    target = out / name
    shutil.copytree(source, target)
    lab.run(["git", "init", "-b", "main"], target)
    lab.run(["git", "config", "user.name", "IndependentCheck"], target)
    lab.run(["git", "config", "user.email", "check@localhost"], target)
    (target / ".gitignore").write_text("*.o\napp\n")
    lab.commit(target, "independent scan input")
    return lab.scan(target)


report = {}

# E8: real BuildChecker graph vs fresh GCC projection.
e8 = artifact / "A-e8"
e8_baseline = json.loads((e8 / "baseline.json").read_text())
e8_edges = json.loads((e8 / "buildchecker" / "actual-graph.json").read_text())
e8_findings = json.loads((e8 / "buildchecker" / "findings.json").read_text())["findings"]
e8_scan = fresh_scan(e8 / "project", "e8-fresh")
e8_projected = project_graph(e8_edges)
report["e8"] = {
    "buildchecker_actual": e8_projected,
    "baseline_actual": e8_baseline["actual"],
    "fresh_gcc_actual": e8_scan["actual"],
    "buildchecker_findings": normalize_findings(e8_findings),
    "baseline_findings": normalize_findings(e8_baseline["findings"]),
    "fresh_gcc_findings": normalize_findings(e8_scan["findings"]),
    "graph_equal": e8_projected == e8_baseline["actual"] == e8_scan["actual"],
    "findings_equal": (normalize_findings(e8_findings)
                       == normalize_findings(e8_baseline["findings"])
                       == normalize_findings(e8_scan["findings"])),
}

# E10: 30-row equality gate and final graph cross-check.
e10 = artifact / "A-e10"
rows = list(csv.DictReader((e10 / "results.csv").open()))
gate = json.loads((e10 / "gate.json").read_text())
e10_edges = json.loads((e10 / "final-buildchecker" / "actual-graph.json").read_text())
e10_findings = json.loads((e10 / "final-buildchecker" / "findings.json").read_text())["findings"]
e10_scan = fresh_scan(e10 / "project", "e10-fresh")
e10_projected = project_graph(e10_edges)
report["e10"] = {
    "rows": len(rows),
    "all_equal": all(r["equal"] == "True" for r in rows),
    "gate": gate,
    "cases": sorted({r["case"] for r in rows}),
    "per_case": {
        case: {
            "reused": next(int(r["reused"]) for r in rows if r["case"] == case),
            "refreshed": next(int(r["refreshed"]) for r in rows if r["case"] == case),
        }
        for case in sorted({r["case"] for r in rows})
    },
    "buildchecker_actual": e10_projected,
    "fresh_gcc_actual": e10_scan["actual"],
    "buildchecker_findings": normalize_findings(e10_findings),
    "fresh_gcc_findings": normalize_findings(e10_scan["findings"]),
    "graph_equal": e10_projected == e10_scan["actual"],
    "findings_equal": normalize_findings(e10_findings) == normalize_findings(e10_scan["findings"]),
}

report["passed"] = (
    report["e8"]["graph_equal"]
    and report["e8"]["findings_equal"]
    and report["e10"]["rows"] == 30
    and report["e10"]["all_equal"]
    and report["e10"]["gate"].get("passed") is True
    and report["e10"]["graph_equal"]
    and report["e10"]["findings_equal"]
)
(out / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(0 if report["passed"] else 1)
