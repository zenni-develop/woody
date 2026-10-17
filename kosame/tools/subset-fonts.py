#!/usr/bin/env python3
"""Build self-hosted WOFF2 subsets containing only the characters each page uses.

Run after `node build.mjs` whenever text in src/i18n/*.json changes:
    python3 tools/subset-fonts.py && node build.mjs --check

Requires fontTools (+ brotli, or the Node-backed shim in tools/pyshim) and the
OFL fonts Noto Sans CJK, Noto Serif CJK and Inter installed locally.
Font paths can be overridden with the env vars NOTO_SANS_DIR / INTER_DIR.
"""
import html as htmllib
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT = ROOT / "public" / "assets" / "fonts"
NOTO = Path(os.environ.get("NOTO_SANS_DIR", "/usr/share/fonts/opentype/noto"))
INTER = Path(os.environ.get("INTER_DIR", "/usr/share/fonts/opentype/inter"))

# TTC face indices inside the Noto CJK collections
JP, KR = 0, 1
FONTS = {
    #        sans 400                              sans 500                              serif 600
    "ko":   ((NOTO / "NotoSansCJK-Regular.ttc", KR), (NOTO / "NotoSansCJK-Medium.ttc", KR), (NOTO / "NotoSerifCJK-SemiBold.ttc", KR)),
    "ja":   ((NOTO / "NotoSansCJK-Regular.ttc", JP), (NOTO / "NotoSansCJK-Medium.ttc", JP), (NOTO / "NotoSerifCJK-SemiBold.ttc", JP)),
    "en":   ((INTER / "Inter-Regular.otf", None),   (INTER / "Inter-Medium.otf", None),   (NOTO / "NotoSerifCJK-SemiBold.ttc", JP)),
    "root": ((NOTO / "NotoSansCJK-Regular.ttc", KR), (NOTO / "NotoSansCJK-Medium.ttc", KR), (NOTO / "NotoSerifCJK-SemiBold.ttc", JP)),
}
# only the OpenType features the CSS actually relies on
FEATURES = "kern,palt,vert,vrt2,vkna,locl,ccmp,liga,calt,tnum"

# elements set in the serif (headings and display kanji) — the serif subset only needs these
SERIF_PATTERNS = [
    r"<(h1|h2|h3)[^>]*>([\s\S]*?)</\1>",
    r'class="[^"]*(?:kanji|vertical|closing__line|record__score|footer__mark|root__title)[^"]*"[^>]*>([\s\S]*?)</',
]


def serif_text(page: str) -> str:
    body = re.sub(r"<head>[\s\S]*?</head>", "", page)
    found = []
    for pat in SERIF_PATTERNS:
        for m in re.finditer(pat, body):
            found.append(m.group(m.lastindex))
    return htmllib.unescape(re.sub(r"<[^>]+>", " ", " ".join(found)))


# always keep basic Latin, digits and common punctuation so small edits don't break
ALWAYS = "".join(chr(c) for c in range(0x20, 0x7F)) + "–—‘’“”…·₩、。「」（）？！：，"


def visible_text(page: str) -> str:
    page = re.sub(r"<script[\s\S]*?</script>", "", page)
    title = re.search(r"<title>([\s\S]*?)</title>", page)
    page = re.sub(r"<head>[\s\S]*?</head>", title.group(1) if title else "", page)
    page = re.sub(r'(?:alt|aria-label|data-t-[a-z]+)="([^"]*)"', r" \1 ", page)
    page = re.sub(r"<[^>]+>", " ", page)
    return htmllib.unescape(page)


def subset(src, index, chars, dest):
    cmd = [
        "pyftsubset", str(src), f"--text={chars}", "--flavor=woff2",
        f"--output-file={dest}", f"--layout-features={FEATURES}", "--no-hinting", "--desubroutinize",
    ]
    if index is not None:
        cmd.append(f"--font-number={index}")
    env = dict(os.environ)
    shim = ROOT / "tools" / "pyshim"
    env["PYTHONPATH"] = f"{shim}{os.pathsep}{env.get('PYTHONPATH', '')}"
    subprocess.run(cmd, check=True, env=env)


def main():
    if not (DIST / "ko" / "index.html").exists():
        sys.exit("dist/ not found — run `node build.mjs` first")
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, (s400, s500, serif) in FONTS.items():
        page = DIST / ("index.html" if lang == "root" else f"{lang}/index.html")
        chars = "".join(sorted(set(visible_text(page.read_text("utf-8")) + ALWAYS) - {"\n", "\t"}))
        (OUT / f"charset-{lang}.txt").write_text(chars, "utf-8")
        subset(*s400, chars, OUT / f"sans-{lang}-400.woff2")
        subset(*s500, chars, OUT / f"sans-{lang}-500.woff2")
        serif_chars = "".join(sorted(set(serif_text(page.read_text("utf-8")) + ALWAYS) - {"\n", "\t"}))
        subset(*serif, serif_chars, OUT / f"serif-{lang}.woff2")
        sizes = ", ".join(f"{p.name} {p.stat().st_size // 1024}KB" for p in sorted(OUT.glob(f"*-{lang}*.woff2")))
        print(f"{lang}: {len(chars)} chars → {sizes}")


if __name__ == "__main__":
    main()
