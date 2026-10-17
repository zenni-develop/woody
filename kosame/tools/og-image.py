#!/usr/bin/env python3
"""Render the 1200×630 share image (OG/Twitter) from the hero illustration.
Needs Playwright with Chromium:  python3 tools/og-image.py"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
import base64
svg = "data:image/svg+xml;base64," + base64.b64encode((ROOT / "public/images/hero.svg").read_bytes()).decode()
out = ROOT / "public/og/og-image.jpg"
tmp = ROOT / "public/og/.og-render.png"
out.parent.mkdir(parents=True, exist_ok=True)
html = f"""<body style="margin:0"><img src="{svg}" style="width:1200px;height:630px;object-fit:cover;object-position:62% 52%;display:block"></body>"""
with sync_playwright() as p:
    exe = os.environ.get("CHROMIUM_PATH")
    b = p.chromium.launch(**({"executable_path": exe} if exe else {}))
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(html); pg.wait_for_load_state("load"); pg.wait_for_timeout(600)
    pg.screenshot(path=str(tmp))
    b.close()
from PIL import Image  # JPEG keeps the grain texture small enough for chat previews
Image.open(tmp).convert("RGB").save(out, "JPEG", quality=84, optimize=True, progressive=True)
tmp.unlink()
print(out, out.stat().st_size // 1024, "KB")
