#!/usr/bin/env node
// Zero-dependency static build: one layout × three language data files.
// Usage: node build.mjs            → writes dist/
//        node build.mjs --check    → also fails if a font subset is missing glyphs
import { readFileSync, writeFileSync, mkdirSync, rmSync, cpSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { renderPage, renderRoot, render404 } from "./src/layout.mjs";

const ROOT = dirname(fileURLToPath(import.meta.url));
const DIST = join(ROOT, "dist");
const read = (p) => JSON.parse(readFileSync(join(ROOT, p), "utf8"));

const site = read("src/data/site.json");
const all = site.languages.map((l) => read(`src/i18n/${l}.json`));

// --- sanity checks: every language must define the same keys ----------------
function keys(obj, prefix = "") {
  return Object.entries(obj).flatMap(([k, v]) =>
    v && typeof v === "object" && !Array.isArray(v) ? keys(v, `${prefix}${k}.`) : [`${prefix}${k}`]
  );
}
const base = new Set(keys(all[0]));
let problems = 0;
for (const t of all.slice(1)) {
  const mine = new Set(keys(t));
  for (const k of base) if (!mine.has(k)) { console.error(`✗ ${t.lang}: missing ${k}`); problems++; }
  for (const k of mine) if (!base.has(k)) { console.error(`✗ ${t.lang}: extra ${k}`); problems++; }
}
for (const t of all) {
  for (const m of site.menu) if (!t.sho.items[m.key]) { console.error(`✗ ${t.lang}: no menu text for ${m.key}`); problems++; }
  if (t.meta.title.length > 60) console.warn(`! ${t.lang}: title is ${t.meta.title.length} chars (guideline ≤ 60)`);
}
if (problems) process.exit(1);

// --- write pages --------------------------------------------------------------
rmSync(DIST, { recursive: true, force: true });
mkdirSync(DIST, { recursive: true });
cpSync(join(ROOT, "public"), DIST, { recursive: true });

const out = (p, s) => { mkdirSync(dirname(join(DIST, p)), { recursive: true }); writeFileSync(join(DIST, p), s); };

for (const t of all) out(`${t.lang}/index.html`, renderPage({ site, t, all }));
out("index.html", renderRoot({ site, all }));
out("404.html", render404({ site, all }));

// photo focal points (kept out of inline styles so the CSP can stay strict)
out(
  "assets/photos.css",
  Object.entries(site.images).map(([k, im]) => `.photo--${k}{object-position:${im.focus}}`).join("\n") + "\n"
);

// per-language font faces (self-hosted subsets, see tools/subset-fonts.py)
const face = (family, file, weight) =>
  `@font-face{font-family:"${family}";src:url("fonts/${file}.woff2") format("woff2");font-weight:${weight};font-style:normal;font-display:swap}`;
for (const l of [...site.languages, "root"]) {
  out(
    `assets/fonts-${l}.css`,
    [face("Kosame Sans", `sans-${l}-400`, 400), face("Kosame Sans", `sans-${l}-500`, 500), face("Kosame Serif", `serif-${l}`, 600)].join("\n") + "\n"
  );
}

// sitemap + robots
const urls = ["", ...site.languages.map((l) => `${l}/`)];
out(
  "sitemap.xml",
  `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${urls
  .map(
    (u) => `  <url>
    <loc>${site.siteUrl}/${u}</loc>
    <lastmod>${site.updated}</lastmod>
${site.languages.map((l) => `    <xhtml:link rel="alternate" hreflang="${l}" href="${site.siteUrl}/${l}/"/>`).join("\n")}
    <xhtml:link rel="alternate" hreflang="x-default" href="${site.siteUrl}/"/>
  </url>`
  )
  .join("\n")}
</urlset>
`
);
out("robots.txt", `User-agent: *\nAllow: /\nSitemap: ${site.siteUrl}/sitemap.xml\n`);

// --- font coverage check --------------------------------------------------------
const strict = process.argv.includes("--check");
let missingTotal = 0;
for (const l of [...site.languages, "root"]) {
  const file = join(ROOT, "public/assets/fonts", `charset-${l}.txt`);
  if (!existsSync(file)) { console.warn(`! fonts for ${l} not generated yet (run: python3 tools/subset-fonts.py)`); missingTotal++; continue; }
  const have = new Set([...readFileSync(file, "utf8")]);
  const html = readFileSync(join(DIST, l === "root" ? "index.html" : `${l}/index.html`), "utf8");
  const need = new Set([...visibleText(html)]);
  const missing = [...need].filter((c) => !have.has(c) && c.trim());
  if (missing.length) { console.warn(`! ${l}: font subset lacks ${missing.join("")} — rerun tools/subset-fonts.py`); missingTotal++; }
}
if (strict && missingTotal) process.exit(1);

console.log(`✓ built ${all.length} languages → dist/`);

export function visibleText(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/g, "")
    .replace(/<head>[\s\S]*?<\/head>/, (h) => (h.match(/<title>([\s\S]*?)<\/title>/) || ["", ""])[1])
    .replace(/(?:alt|aria-label|data-t-[a-z]+)="([^"]*)"/g, " $1 ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
}
