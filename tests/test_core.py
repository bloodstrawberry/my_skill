import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

prepare = load("prepare", ".agents/skills/prepare-evidence/scripts/prepare.py")
verify = load("verify", ".agents/skills/verify-results/scripts/verify.py")

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.source = self.base / "input"
        self.source.mkdir()
        (self.source / "notes.txt").write_text("Price: 0.1\nPrice: 0.2\nTotal: 0.3\n", encoding="utf-8")
        self.out = self.base / "output"

    def tearDown(self):
        self.tmp.cleanup()

    def case(self):
        return {"source_root": "input", "evidence": "output/evidence.json", "requirements": [
            {"id": "R1", "checks": [{"type": "source_quote", "evidence_id": "notes.txt#3", "quote": "0.3"},
                                    {"type": "decimal_sum", "values": ["0.1", "0.2"], "expected": "0.3"}]}]}

    def test_normal_locations_and_decimal(self):
        manifest = prepare.prepare(self.source, self.out, ["notes.txt"])
        self.assertEqual(manifest["missing"], [])
        data = json.loads((self.out / "evidence.json").read_text(encoding="utf-8"))
        self.assertEqual(data["units"][2]["location"], {"line": 3})
        self.assertEqual(verify.evaluate(self.case(), self.base)["status"], "pass")

    def test_duplicate_missing_corrupt_and_unsupported(self):
        (self.source / "copy.txt").write_bytes((self.source / "notes.txt").read_bytes())
        (self.source / "bad.json").write_text("{broken", encoding="utf-8")
        (self.source / "scan.png").write_bytes(b"synthetic-not-a-real-image")
        manifest = prepare.prepare(self.source, self.out, ["absent.txt"])
        self.assertEqual(manifest["missing"], ["absent.txt"])
        by_path = {x["path"]: x for x in manifest["files"]}
        self.assertTrue(any("duplicate_of" in x for x in manifest["files"]))
        self.assertEqual(by_path["bad.json"]["status"], "error")
        self.assertEqual(by_path["scan.png"]["status"], "needs_extraction")

    def test_source_tamper_and_wrong_sum(self):
        prepare.prepare(self.source, self.out)
        (self.source / "notes.txt").write_text("changed", encoding="utf-8")
        case = self.case()
        case["requirements"][0]["checks"][1]["expected"] = "0.4"
        result = verify.evaluate(case, self.base)
        self.assertEqual(result["status"], "fail")
        self.assertTrue(all(x["status"] == "fail" for x in result["requirements"][0]["checks"]))

    def test_missing_evidence_empty_unknown_manual(self):
        prepare.prepare(self.source, self.out)
        case = self.case()
        case["requirements"][0]["checks"][0]["evidence_id"] = "missing#1"
        self.assertEqual(verify.evaluate(case, self.base)["status"], "fail")
        for checks in ([], [{"type": "unknown"}], [{"type": "manual", "reason": "API not called"}]):
            case["requirements"][0]["checks"] = checks
            self.assertEqual(verify.evaluate(case, self.base)["status"], "unverified")

    def test_output_protection_and_expected_traversal(self):
        for output in (self.source, self.source / "child", self.base):
            with self.assertRaises(ValueError):
                prepare.prepare(self.source, output)
        with self.assertRaises(ValueError):
            prepare.prepare(self.source, self.out, ["../secret"])
        prepare.prepare(self.source, self.out)
        with self.assertRaises(ValueError):
            prepare.prepare(self.source, self.out)

    def test_duplicate_requirement_ids(self):
        prepare.prepare(self.source, self.out)
        case = self.case()
        case["requirements"].append(case["requirements"][0])
        with self.assertRaises(ValueError):
            verify.evaluate(case, self.base)

    def test_csv_multiline_and_empty_file(self):
        (self.source / "table.csv").write_text('name,value\n"A\nB",10\n', encoding="utf-8")
        (self.source / "empty.txt").write_text("", encoding="utf-8")
        result = prepare.prepare(self.source, self.out)
        self.assertEqual(next(x for x in result["files"] if x["path"] == "empty.txt")["status"], "review_required")
        units = json.loads((self.out / "evidence.json").read_text(encoding="utf-8"))["units"]
        self.assertEqual([u["location"]["row"] for u in units if u["source"] == "table.csv"], [1, 2])

    def test_nonfinite_decimal_is_not_a_valid_total(self):
        prepare.prepare(self.source, self.out)
        case = self.case()
        case["requirements"][0]["checks"] = [{"type": "decimal_sum", "values": ["Infinity"], "expected": "Infinity"}]
        self.assertEqual(verify.evaluate(case, self.base)["status"], "fail")

    def test_evidence_source_path_escape(self):
        prepare.prepare(self.source, self.out)
        evidence_path = self.out / "evidence.json"
        data = json.loads(evidence_path.read_text(encoding="utf-8"))
        data["units"][2]["source"] = "../outside.txt"
        evidence_path.write_text(json.dumps(data), encoding="utf-8")
        result = verify.evaluate(self.case(), self.base)
        self.assertEqual(result["status"], "fail")
        self.assertIn("escapes", result["requirements"][0]["checks"][0]["reason"])

    @unittest.skipUnless(importlib.util.find_spec("pypdf"), "pypdf unavailable")
    def test_real_pdf_text_and_page_locator(self):
        from pypdf import PdfWriter
        from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
        writer = PdfWriter()
        page = writer.add_blank_page(width=300, height=200)
        font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})
        page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)})})
        stream = DecodedStreamObject()
        stream.set_data(b"BT /F1 12 Tf 10 100 Td (Total 2000 KRW) Tj ET")
        page[NameObject("/Contents")] = writer._add_object(stream)
        writer.write(self.source / "text.pdf")
        prepare.prepare(self.source, self.out)
        data = json.loads((self.out / "evidence.json").read_text(encoding="utf-8"))
        unit = next(u for u in data["units"] if u["source"] == "text.pdf")
        self.assertEqual(unit["location"], {"page": 1})
        self.assertIn("Total 2000 KRW", unit["text"])

    @unittest.skipUnless(importlib.util.find_spec("pypdf"), "pypdf unavailable")
    def test_real_blank_pdf_needs_review(self):
        from pypdf import PdfWriter
        writer = PdfWriter()
        writer.add_blank_page(width=100, height=100)
        writer.write(self.source / "blank.pdf")
        result = prepare.prepare(self.source, self.out)
        item = next(x for x in result["files"] if x["path"] == "blank.pdf")
        self.assertEqual(item["status"], "review_required")
        self.assertIn("page 1", item["issues"][0])

    @unittest.skipUnless(importlib.util.find_spec("openpyxl"), "openpyxl unavailable")
    def test_real_xlsx_formula_and_hidden_sheet(self):
        from openpyxl import Workbook
        book = Workbook()
        book.active["A1"] = "=1+2"
        hidden = book.create_sheet("hidden")
        hidden.sheet_state = "hidden"
        hidden["B2"] = 3
        book.save(self.source / "book.xlsx")
        book.close()
        prepare.prepare(self.source, self.out)
        units = json.loads((self.out / "evidence.json").read_text(encoding="utf-8"))["units"]
        self.assertTrue(any(u["text"] == "=1+2" for u in units))
        self.assertTrue(any(u["location"] == {"sheet": "hidden", "cell": "B2"} for u in units))

if __name__ == "__main__":
    unittest.main()
