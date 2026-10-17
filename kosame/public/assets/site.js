// Cafe Kosame — small progressive enhancements. The page is fully readable without this file.
(() => {
  "use strict";
  const doc = document.documentElement;
  doc.classList.add("js");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- open / closed status (Asia/Seoul) ---------- */
  function seoulNow(tz) {
    const parts = new Intl.DateTimeFormat("en-US", {
      timeZone: tz, weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23",
    }).formatToParts(new Date());
    const get = (t) => parts.find((p) => p.type === t)?.value;
    const day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(get("weekday"));
    return { day, minutes: Number(get("hour")) * 60 + Number(get("minute")) };
  }
  const toMin = (hhmm) => { const [h, m] = hhmm.split(":").map(Number); return h * 60 + m; };

  function renderStatus(el) {
    const d = el.dataset;
    const closed = (d.closedDays || "").split(",").filter(Boolean).map(Number);
    const weekdays = (d.tWeekdays || "").split("|");
    const { day, minutes } = seoulNow(d.tz || "Asia/Seoul");
    const open = toMin(d.open), close = toMin(d.close);
    const nextOpenDay = () => {
      for (let i = 1; i <= 7; i++) {
        const n = (day + i) % 7;
        if (!closed.includes(n)) return i === 1 ? d.tTomorrow : weekdays[n];
      }
      return "";
    };
    let state, text;
    if (closed.includes(day)) { state = "closed"; text = d.tClosed; }
    else if (minutes < open) { state = "before"; text = d.tBefore; }
    else if (minutes < close) { state = "open"; text = d.tOpen; }
    else { state = "after"; text = d.tAfter; }
    text = text.replace("{open}", d.open).replace("{close}", d.close).replace("{next}", nextOpenDay());
    el.dataset.state = state;
    const label = el.querySelector(".status__text");
    if (label && label.textContent !== text) label.textContent = text;
  }
  const statusEls = document.querySelectorAll("[data-status]");
  if (statusEls.length && "Intl" in window) {
    try {
      statusEls.forEach(renderStatus);
      setInterval(() => statusEls.forEach(renderStatus), 60_000);
    } catch { /* keep the static hours text */ }
  }

  /* ---------- top bar turns solid after the hero ---------- */
  const bar = document.querySelector("[data-bar]");
  const hero = document.querySelector(".hero");
  if (bar && hero && "IntersectionObserver" in window) {
    new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) bar.removeAttribute("data-solid");
      else bar.setAttribute("data-solid", "");
    }, { rootMargin: "-64px 0px 0px 0px" }).observe(hero);
  } else if (bar) {
    bar.setAttribute("data-solid", "");
  }

  /* ---------- chapter kanji ink-in ---------- */
  const rails = document.querySelectorAll(".rail");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    rails.forEach((r) => r.setAttribute("data-seen", ""));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.setAttribute("data-seen", ""); io.unobserve(e.target); }
      });
    }, { threshold: 0.4 });
    rails.forEach((r) => io.observe(r));
  }

  /* ---------- swipe row: focusable only while it scrolls (keyboard users can arrow through) ---------- */
  const swipes = document.querySelectorAll("[data-swipe]");
  const syncSwipe = () => swipes.forEach((el) => {
    if (el.scrollWidth > el.clientWidth + 1) el.setAttribute("tabindex", "0");
    else el.removeAttribute("tabindex");
  });
  if (swipes.length) { syncSwipe(); window.addEventListener("resize", syncSwipe, { passive: true }); }

  /* ---------- CTA tracking hook (GA4 / GTM read window.dataLayer if installed) ---------- */
  document.addEventListener("click", (ev) => {
    const a = ev.target.closest("[data-track]");
    if (!a) return;
    const payload = { event: "cta_click", cta: a.dataset.track, lang: a.dataset.lang || doc.lang, map: a.dataset.map || "" };
    if (Array.isArray(window.dataLayer)) window.dataLayer.push(payload);
    if (typeof window.plausible === "function") window.plausible("CTA", { props: payload });
  });

  /* ---------- language landing: suggest, never redirect ---------- */
  const choices = document.querySelectorAll("[data-lang-choice]");
  if (choices.length) {
    const prefs = (navigator.languages || [navigator.language || ""]).map((l) => l.slice(0, 2).toLowerCase());
    const match = prefs.find((p) => [...choices].some((c) => c.dataset.langChoice === p));
    if (match) {
      const el = [...choices].find((c) => c.dataset.langChoice === match);
      el.setAttribute("data-suggested", "");
      el.parentElement.parentElement.prepend(el.parentElement);
    }
  }
})();
