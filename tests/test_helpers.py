import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path
from test_core import load, ROOT

ocr = load("ocr", ".agents/skills/extract-ocr/scripts/ocr.py")
media = load("media", ".agents/skills/analyze-media/scripts/segments.py")

class HelperTests(unittest.TestCase):
    def test_synthetic_tesseract_tsv_parser_not_real_ocr(self):
        # Simulated engine output only: no OCR quality claim.
        tsv = "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n"
        tsv += "5\t1\t1\t1\t1\t1\t10\t20\t30\t40\t60\t2026-10-29\n"
        tsv += "5\t1\t1\t1\t1\t2\t50\t20\t30\t40\t95\t\"Name\n"
        result = ocr.parse_tsv(tsv)
        self.assertEqual(result[0]["bbox"], [10, 20, 30, 40])
        self.assertIn("low_engine_confidence", result[0]["review_flags"])
        self.assertIn("sensitive_number_or_symbol", result[0]["review_flags"])
        self.assertEqual(result[1]["text"], '"Name')

    def test_segments_coverage_overlap_and_boundaries(self):
        for duration in ("0.1", "300", "300.1", "601", "3600"):
            plan = media.segments(duration, "300", "5")
            self.assertEqual(Decimal(plan[0]["start_seconds"]), 0)
            self.assertEqual(Decimal(plan[-1]["end_seconds"]), Decimal(duration))
            for a, b in zip(plan, plan[1:]):
                self.assertEqual(Decimal(a["end_seconds"]) - Decimal(b["start_seconds"]), 5)
        self.assertEqual(len(media.segments(600, 300, 0)), 2)

    def test_segments_reject_invalid_inputs(self):
        for values in ((0, 300, 5), (10, 0, 0), (10, 5, 5), (10, 5, -1), ("NaN", 300, 5), ("Infinity", 300, 5)):
            with self.assertRaises(ValueError):
                media.segments(*values)

    def test_verification_cli_exit_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "evidence.json").write_text('{"units": []}', encoding="utf-8")
            for expected, checks in ((0, [{"type": "equals", "actual": 1, "expected": 1}]),
                                     (1, [{"type": "equals", "actual": 1, "expected": 2}]),
                                     (2, [{"type": "manual", "reason": "not run"}])):
                case = {"source_root": ".", "evidence": "evidence.json", "requirements": [{"id": "R", "checks": checks}]}
                (base / "case.json").write_text(json.dumps(case), encoding="utf-8")
                result = subprocess.run([sys.executable, str(ROOT / ".agents/skills/verify-results/scripts/verify.py"),
                                         str(base / "case.json"), "--report", str(base / f"report{expected}.json")], capture_output=True)
                self.assertEqual(result.returncode, expected, result.stderr)

if __name__ == "__main__":
    unittest.main()
