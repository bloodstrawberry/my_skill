"""Capture one anonymous Chromium page. No stored credentials or cookies."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("output", type=Path)
    parser.add_argument("--wait-selector")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    args = parser.parse_args()
    if urlparse(args.url).scheme not in {"http", "https", "file"} or args.timeout_ms <= 0:
        parser.exit(2, "http/https/file URL and positive timeout required\n")
    if args.output.exists() and any(args.output.iterdir()):
        parser.exit(2, "output must be new or empty\n")
    try:
        from playwright.sync_api import sync_playwright
        args.output.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            try:
                context = browser.new_context(viewport={"width": 1280, "height": 720}, locale="en-US", timezone_id="UTC")
                page = context.new_page()
                page.set_default_timeout(args.timeout_ms)
                response = page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout_ms)
                if args.wait_selector:
                    page.locator(args.wait_selector).wait_for(state="visible")
                (args.output / "text.txt").write_text(page.locator("body").inner_text(), encoding="utf-8")
                page.screenshot(path=str(args.output / "screen.png"), full_page=True)
                data = {"status": "captured", "url": args.url, "final_url": page.url, "http_status": response.status if response else None,
                        "captured_at": datetime.now(timezone.utc).isoformat(), "browser": browser.version,
                        "viewport": {"width": 1280, "height": 720}, "locale": "en-US", "timezone": "UTC", "login": "anonymous",
                        "cookie_consent": "unknown; no automatic interaction", "wait_selector": args.wait_selector,
                        "scope": "single page; no bug reproduction or login verification"}
                (args.output / "capture.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
                return 1 if response and response.status >= 400 else 0
            finally:
                browser.close()
    except Exception as exc:
        parser.exit(2, f"capture not completed: {type(exc).__name__}: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
