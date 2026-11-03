"""Compare A-track semantic outputs from two independent CI runs on one commit."""
import csv
import json
import sys
from pathlib import Path

run1 = Path(sys.argv[1]).resolve()
run2 = Path(sys.argv[2]).resolve()
out = Path(sys.argv[3]).resolve()
out.mkdir(parents=True, exist_ok=True)

VOLATILE = {"commit", "elapsed_s", "elapsed_ms", "trace_id", "pid", "line"}


def norm(value):
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items() if k not in VOLATILE}
    if isinstance(value, list):
        return [norm(v) for v in value]
    return value


def semantic_findings(findings):
    return sorted((f["type"], f["target"], f["dependency"]) for f in findings)


def semantic_graph(edges):
    return sorted((e["target"], e["dependency"], e.get("kind"))
                  for e in edges if e["target"] in ("main.o", "helper.o"))


def load(path):
    return json.loads(path.read_text())


def diff(name, a, b, errors):
    if a != b:
        errors.append({"item": name, "run1": a, "run2": b})
        print("DIFF", name)
    else:
        print("SAME", name)


errors = []
for stage in ("A-e8", "A-e9"):
    files = sorted(p.name for p in (run1 / stage).glob("*.json"))
    for name in files:
        if name.startswith("buildchecker"):
            continue
        diff(f"{stage}/{name}", norm(load(run1 / stage / name)),
             norm(load(run2 / stage / name)), errors)

# E8 BuildChecker semantic comparison.
for base in (run1, run2):
    pass
e8a = load(run1 / "A-e8/buildchecker/findings.json")
e8b = load(run2 / "A-e8/buildchecker/findings.json")
diff("A-e8/buildchecker/findings", semantic_findings(e8a["findings"]),
     semantic_findings(e8b["findings"]), errors)
diff("A-e8/buildchecker/actual-graph",
     semantic_graph(load(run1 / "A-e8/buildchecker/actual-graph.json")),
     semantic_graph(load(run2 / "A-e8/buildchecker/actual-graph.json")), errors)

# E10 case JSONs.
for name in ("baseline", "unchanged", "body", "include", "declaration", "flags", "header"):
    diff(f"A-e10/{name}.json", norm(load(run1 / "A-e10" / f"{name}.json")),
         norm(load(run2 / "A-e10" / f"{name}.json")), errors)

# E10 final BuildChecker semantics.
e10a = load(run1 / "A-e10/final-buildchecker/findings.json")
e10b = load(run2 / "A-e10/final-buildchecker/findings.json")
diff("A-e10/final-buildchecker/findings", semantic_findings(e10a["findings"]),
     semantic_findings(e10b["findings"]), errors)
diff("A-e10/final-buildchecker/actual-graph",
     semantic_graph(load(run1 / "A-e10/final-buildchecker/actual-graph.json")),
     semantic_graph(load(run2 / "A-e10/final-buildchecker/actual-graph.json")), errors)

# E10 30-row gate: compare structure and equality, not timings.
def rows(path):
    with (path / "A-e10/results.csv").open() as f:
        return list(csv.DictReader(f))


r1, r2 = rows(run1), rows(run2)
diff("A-e10/results rows", len(r1), len(r2), errors)
diff("A-e10/results cases", sorted({r["case"] for r in r1}), sorted({r["case"] for r in r2}), errors)
diff("A-e10/results equal", [r["equal"] for r in r1], [r["equal"] for r in r2], errors)
diff("A-e10/results cache behaviour",
     sorted((r["case"], r["repeat"], r["reused"], r["refreshed"]) for r in r1),
     sorted((r["case"], r["repeat"], r["reused"], r["refreshed"]) for r in r2), errors)
diff("A-e10/gate.json", load(run1 / "A-e10/gate.json"), load(run2 / "A-e10/gate.json"), errors)

summary = {"passed": not errors, "differences": errors}
(out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print("PASSED", summary["passed"])
raise SystemExit(0 if summary["passed"] else 1)
