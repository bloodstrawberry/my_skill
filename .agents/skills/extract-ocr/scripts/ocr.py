"""Single-image Tesseract TSV extraction with original pixel coordinates."""
import argparse
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
from pathlib import Path


def parse_tsv(text):
    tokens = []
    for row in csv.DictReader(io.StringIO(text), delimiter="\t", quoting=csv.QUOTE_NONE):
        if not row.get("text", "").strip():
            continue
        confidence = float(row["conf"])
        flags = []
        if confidence < 80:
            flags.append("low_engine_confidence")
        if re.search(r"[0-9@_{}<>/=+\\-]", row["text"]):
            flags.append("sensitive_number_or_symbol")
        tokens.append({"text": row["text"], "bbox": [int(row[k]) for k in ("left", "top", "width", "height")],
                       "block": int(row["block_num"]), "paragraph": int(row["par_num"]), "line": int(row["line_num"]),
                       "confidence": confidence, "review_flags": flags})
    return tokens


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--lang", default="eng")
    parser.add_argument("--psm", type=int, choices=range(14), default=3)
    parser.add_argument("--timeout", type=float, default=120)
    args = parser.parse_args()
    if args.output.exists() or args.timeout <= 0:
        parser.exit(2, "output exists or invalid timeout\n")
    binary = shutil.which("tesseract")
    if binary is None:
        parser.exit(2, "tesseract missing; see docs/setup.md; OCR not performed\n")
    try:
        run = subprocess.run([binary, str(args.image.resolve()), "stdout", "-l", args.lang, "--psm", str(args.psm), "tsv"],
                             capture_output=True, text=True, encoding="utf-8", timeout=args.timeout, check=True)
        version = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=10, check=True).stdout.splitlines()[0]
        data = {"source": str(args.image.resolve()), "source_sha256": hashlib.sha256(args.image.read_bytes()).hexdigest(),
                "tool": version, "lang": args.lang, "psm": args.psm, "coordinate_system": "original image pixels, top-left, bbox=x/y/width/height",
                "tokens": parse_tsv(run.stdout), "warnings": ["review all names, dates and symbols; no table structure or translation inferred", run.stderr.strip()]}
        if not data["tokens"]:
            data["warnings"].append("empty OCR; inspect source")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 0 if data["tokens"] else 1
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        parser.exit(2, f"OCR failed: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
