"""Evaluate explicit evidence/decimal checks; never certify semantic correctness."""
import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path


def contained(root, name):
    path = (root / name).resolve()
    if path != root and root not in path.parents:
        raise ValueError("source path escapes source_root")
    return path


def evaluate(case, base):
    if not isinstance(case, dict) or not isinstance(case.get("requirements"), list) or not case["requirements"]:
        raise ValueError("requirements must be a nonempty list")
    ids = [r["id"] for r in case["requirements"]]
    if any(not isinstance(x, str) or not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("unique nonempty requirement IDs required")
    root = (base / case["source_root"]).resolve()
    evidence_path = base / case["evidence"]
    units = json.loads(evidence_path.read_text(encoding="utf-8-sig"))["units"]
    by_id = {u["id"]: u for u in units}
    if len(by_id) != len(units):
        raise ValueError("duplicate evidence IDs")
    results = []
    for req in case["requirements"]:
        checks = req.get("checks", [])
        details = []
        for check in checks:
            kind = check.get("type")
            status, reason = "unverified", "unsupported check type"
            try:
                if kind == "decimal_sum":
                    values = check["values"]
                    if not isinstance(values, list) or not values:
                        raise ValueError("nonempty values required")
                    numbers = [Decimal(str(v)) for v in values]
                    expected = Decimal(str(check["expected"]))
                    if not all(v.is_finite() for v in numbers + [expected]):
                        raise ValueError("finite decimal values required")
                    ok = sum(numbers, Decimal(0)) == expected
                    status, reason = ("pass" if ok else "fail"), "independent decimal calculation (input provenance checked separately)"
                elif kind == "equals":
                    status = "pass" if check["actual"] == check["expected"] else "fail"
                    reason = "literal comparison; not semantic validation"
                elif kind == "source_quote":
                    unit = by_id[check["evidence_id"]]
                    source = contained(root, unit["source"])
                    current = hashlib.sha256(source.read_bytes()).hexdigest()
                    quote = check["quote"]
                    ok = bool(quote.strip()) and quote in unit["text"] and bool(unit.get("location")) and current == unit["source_sha256"]
                    status, reason = ("pass" if ok else "fail"), "source hash/location/extracted quote; visual and semantic review still required"
                elif kind == "manual":
                    reason = check.get("reason", "requires original-source human review")
            except Exception as exc:
                status, reason = "fail", f"{type(exc).__name__}: {exc}"
            details.append({"type": kind, "status": status, "reason": reason})
        status = "fail" if any(c["status"] == "fail" for c in details) else "unverified" if not details or any(c["status"] == "unverified" for c in details) else "pass"
        results.append({"id": req["id"], "status": status, "checks": details})
    overall = "fail" if any(r["status"] == "fail" for r in results) else "unverified" if any(r["status"] == "unverified" for r in results) else "pass"
    return {"schema_version": 1, "scope": "declared checks only; not a correctness certificate", "status": overall, "requirements": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        parser.exit(2, "report already exists; use a new path\n")
    try:
        report = evaluate(json.loads(args.case.read_text(encoding="utf-8-sig")), args.case.resolve().parent)
    except Exception as exc:
        parser.exit(2, f"invalid case: {type(exc).__name__}: {exc}\n")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["status"])
    return {"pass": 0, "fail": 1, "unverified": 2}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
