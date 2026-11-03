"""Independent E9 A-track check: incremental reuse vs a fresh full scan at C0-C3.

The check only reads the teaching lab module; it does not modify the repository.
It answers one question: for the same working tree, does scan(p, previous)
produce the same actual/declared/findings as scan(p)?
"""
import json
import shutil
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "labs" / "e8e10"))
import lab  # noqa: E402

if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)
p = out / "project"
lab.fixture(p)
baseline = lab.scan(p)


def compare(stage, previous):
    incremental = lab.scan(p, previous)
    full = lab.scan(p)
    equal = all(incremental[k] == full[k] for k in ("actual", "declared", "findings"))
    row = {
        "stage": stage,
        "equal": equal,
        "incremental_reused": incremental["reused"],
        "incremental_refreshed": incremental["refreshed"],
        "incremental_added": incremental["added"],
        "incremental_resolved": incremental["resolved"],
        "incremental_actual": incremental["actual"],
        "incremental_declared": incremental["declared"],
        "incremental_findings": incremental["findings"],
        "full_actual": full["actual"],
        "full_declared": full["declared"],
        "full_findings": full["findings"],
    }
    if not equal:
        raise SystemExit("MISMATCH " + stage)
    print("OK", stage, "reused=", incremental["reused"], "refreshed=", incremental["refreshed"])
    return incremental, row


rows = []
(p / "main.c").write_text((p / "main.c").read_text().replace("VALUE+helper()", "VALUE+helper()+0"))
lab.commit(p, "C1 body change")
one, row = compare("C1", baseline)
rows.append(row)
assert set(one["reused"]) == {"main.o", "helper.o"} and not one["refreshed"]

(p / "main.c").write_text('#include "extra.h"\n' + (p / "main.c").read_text())
lab.commit(p, "C2 include change")
two, row = compare("C2", one)
rows.append(row)
assert set(two["refreshed"]) == {"main.o", "helper.o"} and not two["reused"]
assert ["MISSING", "main.o", "extra.h"] in two["added"]

(p / "Makefile").write_text((p / "Makefile").read_text().replace(
    "main.c unused.h", "main.c unused.h config.h extra.h"))
lab.commit(p, "C3 repair declarations")
three, row = compare("C3", two)
rows.append(row)
assert set(three["reused"]) == {"main.o", "helper.o"} and not three["refreshed"]
assert sorted(three["resolved"]) == [["MISSING", "main.o", "config.h"],
                                     ["MISSING", "main.o", "extra.h"]]

summary = {
    "check": "e9-a-incremental-vs-full",
    "method": "same tree, scan(p, prev) vs scan(p), compare actual/declared/findings",
    "baseline": baseline,
    "stages": rows,
    "all_equal": all(r["equal"] for r in rows),
}
(out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print("ALL EQUAL", summary["all_equal"])
