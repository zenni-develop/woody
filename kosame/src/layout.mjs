// Single layout for every language. Text comes from src/i18n/<lang>.json,
// shared facts (hours, prices, links, images) from src/data/site.json.

const ESC = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
export const esc = (s = "") => String(s).replace(/[&<>"']/g, (c) => ESC[c]);

const IMG_WIDTHS = [640, 960, 1440, 2000];

/** Unsplash-hosted responsive image (hotlinked, as Unsplash's guidelines ask). */
function img(site, key, alt, { sizes = "100vw", eager = false, cls = "" } = {}) {
  const im = site.images[key];
  const url = (w) => `${im.src}?auto=format&fit=max&q=72&w=${w}`;
  const srcset = IMG_WIDTHS.map((w) => `${url(w)} ${w}w`).join(", ");
  const loading = eager ? 'loading="eager" fetchpriority="high"' : 'loading="lazy"';
  return `<img class="photo photo--${key} ${cls}" src="${url(1440)}" srcset="${srcset}" sizes="${sizes}" width="${im.w}" height="${im.h}" alt="${esc(alt)}" ${loading} decoding="async">`;
}

function price(lang, n) {
  const num = n.toLocaleString("en-US");
  if (lang === "ko") return `${num}원`;
  if (lang === "ja") return `${num}ウォン`;
  return `₩${num}`;
}

function extLink(href, label, t, attrs = "") {
  return `<a href="${esc(href)}" target="_blank" rel="noopener noreferrer" ${attrs}>${label}<span class="visually-hidden"> (${esc(t.ui.external)})</span></a>`;
}

function rail(ch) {
  return `<div class="rail" aria-hidden="true"><span class="rail__kanji">${esc(ch.kanji)}</span><span class="rail__label">${esc(ch.label)}</span></div>`;
}

function langSwitch(t, all, here, label = t.ui.langSwitch) {
  const items = all
    .map((o) => {
      const current = o.lang === here;
      return `<li><a href="../${o.lang}/" hreflang="${o.lang}" lang="${o.lang}"${current ? ' aria-current="page"' : ""}>${esc(o.langName)}</a></li>`;
    })
    .join("");
  return `<nav class="langs" aria-label="${esc(label)}"><ul>${items}</ul></nav>`;
}

function headLinks(site, all, lang) {
  const alt = all
    .map((o) => `<link rel="alternate" hreflang="${o.lang}" href="${site.siteUrl}/${o.lang}/">`)
    .join("\n  ");
  return `${alt}
  <link rel="alternate" hreflang="x-default" href="${site.siteUrl}/">
  <link rel="canonical" href="${site.siteUrl}/${lang}/">`;
}

export const CSP = [
  "default-src 'self'",
  "img-src 'self' https://images.unsplash.com data:",
  "style-src 'self'",
  "font-src 'self'",
  "script-src 'self'",
  "connect-src 'self'",
  "base-uri 'self'",
  "form-action 'none'",
  "object-src 'none'",
].join("; ");

function head({ site, t, all, lang, title, description, ogImage, path }) {
  return `<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta http-equiv="Content-Security-Policy" content="${CSP}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>${esc(title)}</title>
  <meta name="description" content="${esc(description)}">
  <meta name="theme-color" content="#F7F9F4">
  ${lang ? headLinks(site, all, lang) : `<link rel="canonical" href="${site.siteUrl}/">\n  ${all.map((o) => `<link rel="alternate" hreflang="${o.lang}" href="${site.siteUrl}/${o.lang}/">`).join("\n  ")}\n  <link rel="alternate" hreflang="x-default" href="${site.siteUrl}/">`}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Cafe Kosame 小雨">
  <meta property="og:title" content="${esc(title)}">
  <meta property="og:description" content="${esc(description)}">
  <meta property="og:url" content="${site.siteUrl}/${path}">
  <meta property="og:image" content="${ogImage}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  ${t ? `<meta property="og:locale" content="${t.ogLocale}">\n  ${all.filter((o) => o.lang !== lang).map((o) => `<meta property="og:locale:alternate" content="${o.ogLocale}">`).join("\n  ")}` : ""}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(title)}">
  <meta name="twitter:description" content="${esc(description)}">
  <meta name="twitter:image" content="${ogImage}">
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="preload" as="image" href="${site.images.hero.src}?auto=format&amp;fit=max&amp;q=72&amp;w=1440" imagesrcset="${[640, 960, 1440, 2000].map((w) => `${site.images.hero.src}?auto=format&amp;fit=max&amp;q=72&amp;w=${w} ${w}w`).join(", ")}" imagesizes="100vw" fetchpriority="high">
  <link rel="icon" href="${lang ? "../" : ""}assets/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="${lang ? "../" : ""}assets/fonts/serif-${lang || "root"}.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="${lang ? "../" : ""}assets/fonts-${lang || "root"}.css">
  <link rel="stylesheet" href="${lang ? "../" : ""}assets/site.css">
  <link rel="stylesheet" href="${lang ? "../" : ""}assets/photos.css">
  <script src="${lang ? "../" : ""}assets/site.js" defer></script>
</head>`;
}

export function ogImage(site) {
  return `${site.images.hero.src}?auto=format&fit=crop&w=1200&h=630&q=75`;
}

export function renderPage({ site, t, all }) {
  const lang = t.lang;
  const mapKey = site.primaryMap[lang];
  const mapUrl = site.links[mapKey];
  const cta = (extra = "", label = t.ui.cta) =>
    extLink(mapUrl, esc(label), t, `class="button ${extra}" data-track="directions" data-lang="${lang}" data-map="${mapKey}"`);

  const statusData = [
    `data-open="${site.hours.open}"`,
    `data-close="${site.hours.close}"`,
    `data-closed-days="${site.hours.closedWeekdays.join(",")}"`,
    `data-tz="${site.hours.timezone}"`,
    `data-t-open="${esc(t.ui.status.open)}"`,
    `data-t-before="${esc(t.ui.status.before)}"`,
    `data-t-after="${esc(t.ui.status.after)}"`,
    `data-t-closed="${esc(t.ui.status.closed)}"`,
    `data-t-weekdays="${esc(t.ui.weekdays.join("|"))}"`,
    `data-t-tomorrow="${esc(t.ui.tomorrow)}"`,
  ].join(" ");

  // Menu, grouped like a tearoom's お品書き
  const groups = ["dango", "tea", "signature", "coffee"];
  const menu = groups
    .map((g) => {
      const rows = site.menu
        .filter((m) => m.group === g)
        .map((m) => {
          const it = t.sho.items[m.key];
          const season = m.season ? `<span class="menu__season">${esc(t.sho.season[m.season])}</span>` : "";
          const desc = it.desc ? `<p class="menu__desc">${esc(it.desc)}</p>` : "";
          return `<li class="menu__item"><div class="menu__line"><span class="menu__name">${esc(it.name)}${season}</span><span class="menu__dots" aria-hidden="true"></span><span class="menu__price">${price(lang, m.price)}</span></div>${desc}</li>`;
        })
        .join("");
      return `<div class="menu__group"><h3 class="menu__heading">${esc(t.sho.groups[g])}</h3><ul class="menu__list">${rows}</ul></div>`;
    })
    .join("");

  const ratings = site.ratings
    .map(
      (r) =>
        `<li class="record"><span class="record__score">${r.score}</span><span class="record__meta">${extLink(r.url, esc(t.ten.ratingLabels[r.key]), t)}<span class="record__count">${r.count} ${esc(t.ten.reviewsWord)}</span></span></li>`
    )
    .join("");

  const info = t.ketsu.info
    .map((i) => `<div class="info__row"><dt>${esc(i.term)}</dt><dd>${esc(i.desc)}</dd></div>`)
    .join("");

  const maps = ["naverMap", "kakaoMap", "googleMap"]
    .map((k) => `<li>${extLink(site.links[k], esc(t.ketsu.maps[k]), t, `class="maplink" data-track="map-${k}" data-lang="${lang}"`)}</li>`)
    .join("");

  const faq = t.ketsu.faq
    .map((f) => `<details class="faq__item"><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p></details>`)
    .join("");

  const credits = Object.entries(site.images)
    .map(([, im]) => `<li>${extLink(im.page, esc(im.author), t)}</li>`)
    .join("");

  const sources = site.sources.map((s) => `<li>${extLink(s.url, esc(s.label), t)}</li>`).join("");

  return `<!doctype html>
<html lang="${lang}">
${head({ site, t, all, lang, title: t.meta.title, description: t.meta.description, ogImage: ogImage(site), path: `${lang}/` })}
<body>
<a class="skip" href="#top">${esc(t.ui.skip)}</a>

<header class="bar" data-bar>
  <a class="bar__mark" href="#top" aria-label="Cafe Kosame">
    <span class="bar__kanji" lang="ja">小雨</span><span class="bar__word">KOSAME</span>
  </a>
  <nav class="bar__nav" aria-label="${esc(t.ui.navLabel)}">
    <a href="#story">${esc(t.ui.nav.story)}</a>
    <a href="#menu">${esc(t.ui.nav.menu)}</a>
    <a href="#visit">${esc(t.ui.nav.visit)}</a>
  </nav>
  ${langSwitch(t, all, lang)}
  ${extLink(mapUrl, esc(t.ui.ctaShort), t, `class="bar__cta" data-track="directions-bar" data-lang="${lang}" data-map="${mapKey}"`)}
</header>

<main id="top" tabindex="-1">
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero__media">${img(site, "hero", t.hero.imageAlt, { eager: true })}</div>
    <div class="hero__rain" aria-hidden="true"></div>
    <p class="hero__vertical" lang="ja" aria-hidden="true">小雨</p>
    <div class="hero__body">
      <p class="hero__place">${esc(t.hero.place)}</p>
      <h1 id="hero-title" class="hero__title">${t.hero.title.map((l) => `<span>${esc(l)}</span>`).join("")}</h1>
      <p class="hero__lead">${esc(t.hero.lead)}</p>
      <div class="hero__actions">
        ${cta("button--light")}
        <a class="textlink textlink--light" href="#story">${esc(t.ui.readStory)}</a>
      </div>
      <p class="status" data-status ${statusData} aria-live="polite"><span class="status__dot" aria-hidden="true"></span><span class="status__text">${esc(t.ketsu.info[0].desc)}</span> <span class="status__basis">(${esc(t.ui.status.basis)})</span></p>
    </div>
  </section>

  <section class="chapter chapter--ki" id="story" aria-labelledby="ki-title">
    ${rail(t.ki)}
    <div class="chapter__text">
      <h2 id="ki-title" class="chapter__title">${esc(t.ki.heading)}</h2>
      ${t.ki.paras.map((p) => `<p>${esc(p)}</p>`).join("")}
      <figure class="note">
        <blockquote><p>${esc(t.ki.note)}</p></blockquote>
        <figcaption>${extLink(site.links.instagram, esc(t.ki.noteSource), t)}</figcaption>
      </figure>
    </div>
    <figure class="chapter__media chapter__media--tall">${img(site, "room", t.ki.imageAlt, { sizes: "(min-width: 960px) 40vw, 100vw" })}</figure>
  </section>

  <section class="chapter chapter--band chapter--sho" id="menu" aria-labelledby="sho-title">
    ${rail(t.sho)}
    <div class="chapter__text">
      <h2 id="sho-title" class="chapter__title">${esc(t.sho.heading)}</h2>
      <p>${esc(t.sho.intro)}</p>
      <div class="menu">${menu}</div>
      <p class="fineprint">${esc(t.sho.priceNote)}</p>
    </div>
    <div class="chapter__media chapter__media--pair" role="group" aria-label="${esc(t.sho.groups.tea)} / ${esc(t.sho.groups.dango)}" data-swipe>
      <figure>${img(site, "matcha", t.sho.imageAlt.matcha, { sizes: "(min-width: 960px) 36vw, 100vw" })}</figure>
      <figure>${img(site, "dango", t.sho.imageAlt.dango, { sizes: "(min-width: 960px) 30vw, 100vw" })}</figure>
    </div>
    <div class="pairing">
      <figure class="pairing__media">${img(site, "fig", t.sho.imageAlt.fig, { sizes: "(min-width: 960px) 55vw, 100vw" })}</figure>
      <div class="pairing__text">
        <h3>${esc(t.sho.pairingTitle)}</h3>
        <p>${esc(t.sho.pairing)}</p>
        <ul class="notes">${t.sho.notes.map((n) => `<li>${esc(n)}</li>`).join("")}</ul>
      </div>
    </div>
  </section>

  <section class="chapter chapter--band chapter--ten" aria-labelledby="ten-title">
    ${rail(t.ten)}
    <div class="chapter__text">
      <h2 id="ten-title" class="chapter__title chapter__title--quote">${esc(t.ten.heading)}</h2>
      ${t.ten.paras.map((p) => `<p>${esc(p)}</p>`).join("")}
      <p class="fineprint">${extLink(site.links.instagram, esc(t.ten.paraSource), t)}</p>
    </div>
    <figure class="chapter__media chapter__media--small">${img(site, "hojicha", t.sho.imageAlt.hojicha, { sizes: "(min-width: 960px) 26vw, 70vw" })}</figure>
    <div class="voices">
      <h3 class="voices__title">${esc(t.ten.ratingsTitle)}</h3>
      <ul class="records">${ratings}</ul>
      <div class="voices__grid">
        ${t.ten.voices.map((v) => `<div class="voice"><h4>${esc(v.title)}</h4><p>${esc(v.body)}</p></div>`).join("")}
        <div class="voice voice--caveat"><h4>${esc(t.ten.caveatsTitle)}</h4><ul>${t.ten.caveats.map((c) => `<li>${esc(c)}</li>`).join("")}</ul></div>
      </div>
      <p class="fineprint">${esc(t.ten.summaryNote)}</p>
    </div>
  </section>

  <section class="chapter chapter--band chapter--ketsu" id="visit" aria-labelledby="ketsu-title">
    <div class="ketsu__media">${img(site, "window", t.ketsu.imageAlt, { sizes: "100vw" })}</div>
    ${rail(t.ketsu)}
    <div class="chapter__text">
      <h2 id="ketsu-title" class="chapter__title">${esc(t.ketsu.heading)}</h2>
      <p>${esc(t.ketsu.lead)}</p>
      <dl class="info">${info}</dl>
      <h3 class="small-title">${esc(t.ketsu.mapsTitle)}</h3>
      <ul class="maplinks">${maps}</ul>
    </div>
    <div class="faq">
      <h3 class="small-title">${esc(t.ketsu.faqTitle)}</h3>
      ${faq}
    </div>
    <div class="closing">
      <p class="closing__line">${esc(t.ketsu.closing)}</p>
      ${cta("button--light")}
    </div>
  </section>
</main>

<footer class="footer">
  <div class="footer__main">
    <p class="footer__mark"><span lang="ja">小雨</span> Cafe Kosame</p>
    <p>${extLink(site.links.instagram, esc(t.footer.instagram), t, `data-track="instagram" data-lang="${lang}"`)}</p>
    <p class="fineprint">${esc(t.footer.instagramNote)}</p>
  </div>
  <div class="footer__notes">
    <p>${esc(t.footer.photoNote)}</p>
    <p>${esc(t.footer.disclaimer)}</p>
    <p>${esc(t.footer.updated)}: <time datetime="${site.updated}">${site.updated}</time></p>
    <div class="footer__lists">
      <div><h2 class="footer__h">${esc(t.footer.sources)}</h2><ul>${sources}</ul></div>
      <div><h2 class="footer__h">${esc(t.footer.credits)} (Unsplash)</h2><ul>${credits}</ul></div>
    </div>
  </div>
  ${langSwitch(t, all, lang, t.ui.langSwitchFooter)}
</footer>
</body>
</html>
`;
}

export function renderRoot({ site, all }) {
  const ko = all.find((o) => o.lang === "ko");
  const title = "Cafe Kosame 小雨 | 카페 코사메 / カフェ小雨";
  const description = all.map((o) => o.meta.description).join(" ").slice(0, 155);
  const choices = all
    .map(
      (o) =>
        `<li><a class="choice" href="${o.lang}/" hreflang="${o.lang}" lang="${o.lang}" data-lang-choice="${o.lang}"><span class="choice__name">${esc(o.langName)}</span><span class="choice__title">${esc(o.hero.title.join(" "))}</span></a></li>`
    )
    .join("");
  return `<!doctype html>
<html lang="ko">
${head({ site, t: null, all, lang: null, title, description, ogImage: ogImage(site), path: "" })}
<body class="root">
<main class="root__main">
  <div class="hero__media">${img(site, "hero", ko.hero.imageAlt, { eager: true })}</div>
  <div class="hero__rain" aria-hidden="true"></div>
  <div class="root__body">
    <p class="root__kanji" lang="ja">小雨</p>
    <h1 class="root__title">Cafe Kosame</h1>
    <p class="root__place"><span lang="ko">인천 구월동</span><span lang="ja">仁川 九月洞</span><span lang="en">Guwol-dong, Incheon</span></p>
    <ul class="choices">${choices}</ul>
  </div>
</main>
</body>
</html>
`;
}

export function render404({ site, all }) {
  return `<!doctype html>
<html lang="ko">
${head({ site, t: null, all, lang: null, title: "Cafe Kosame 小雨", description: "", ogImage: ogImage(site), path: "" })}
<body class="root">
<main class="root__main root__main--plain">
  <div class="root__body">
    <p class="root__kanji" lang="ja">小雨</p>
    <h1 class="root__title">404</h1>
    <ul class="choices choices--plain">
      ${all.map((o) => `<li><a class="choice" href="${site.siteUrl}/${o.lang}/" lang="${o.lang}"><span class="choice__name">${esc(o.langName)}</span></a></li>`).join("")}
    </ul>
  </div>
</main>
</body>
</html>
`;
}
