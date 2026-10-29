"""Create gap-free overlapping media intervals; does not decode media."""
import argparse
import json
from decimal import Decimal
from pathlib import Path


def segments(duration, chunk, overlap):
    duration, chunk, overlap = map(lambda x: Decimal(str(x)), (duration, chunk, overlap))
    if not all(x.is_finite() for x in (duration, chunk, overlap)) or duration <= 0 or chunk <= 0 or not 0 <= overlap < chunk:
        raise ValueError("finite duration/chunk > 0 and 0 <= overlap < chunk required")
    start, output = Decimal(0), []
    while start < duration:
        end = min(start + chunk, duration)
        output.append({"id": len(output), "start_seconds": str(start), "end_seconds": str(end), "offset_seconds": str(start)})
        if len(output) > 100000:
            raise ValueError("plan too large; increase chunk size")
        if end == duration:
            break
        start = end - overlap
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("duration")
    parser.add_argument("--chunk", default="300")
    parser.add_argument("--overlap", default="5")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.exit(2, "output exists\n")
    try:
        data = {"schema_version": 1, "units": "seconds, relative to original start", "chunks": segments(args.duration, args.chunk, args.overlap)}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except (ValueError, ArithmeticError) as exc:
        parser.exit(2, f"invalid interval: {exc}\n")
    print(len(data["chunks"]))


if __name__ == "__main__":
    main()
