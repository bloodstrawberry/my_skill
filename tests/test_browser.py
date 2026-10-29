"""Opt-in real Chromium test on local synthetic HTML; no external site."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from test_core import ROOT

@unittest.skipUnless(os.environ.get("RUN_BROWSER_TESTS") == "1", "set RUN_BROWSER_TESTS=1 for real browser")
class BrowserTests(unittest.TestCase):
    def test_dynamic_loading_click_and_capture(self):
        from playwright.sync_api import sync_playwright, expect
        url = (ROOT / "examples/browser.html").as_uri()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                page = browser.new_page()
                page.goto(url)
                page.locator('body[data-ready="yes"]').wait_for()
                expect(page.locator("#result")).to_have_text("Waiting")
                page.get_by_role("button", name="Calculate").click()
                expect(page.locator("#result")).to_have_text("2000 KRW")
                self.assertNotEqual(page.locator("#result").inner_text(), "1900 KRW")
            finally:
                browser.close()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "capture"
            result = subprocess.run([sys.executable, str(ROOT / ".agents/skills/inspect-browser/scripts/capture.py"),
                                     url, str(out), "--wait-selector", 'body[data-ready="yes"]'], capture_output=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((out / "screen.png").is_file())
            self.assertIn("Waiting", (out / "text.txt").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
