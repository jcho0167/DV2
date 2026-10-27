// Embeds every Vega-Lite spec in /specs and adds light, purposeful motion.
// Shared styling lives in one config object so the individual specs stay readable,
// and so every chart uses the same fonts, neutrals and colour roles as the page CSS.

document.documentElement.classList.add("js");

const INK = "#17221b";
const MUTED = "#5e675f";
const RULE = "#dcd9cd";
const AXIS = "#aaa79b";

const sharedConfig = {
  background: null,
  font: "Archivo, 'Helvetica Neue', Arial, sans-serif",
  padding: { left: 0, right: 4, top: 4, bottom: 4 },   // left edge flush with the text column
  view: { stroke: null },
  axis: {
    labelColor: MUTED,
    titleColor: INK,
    labelFontSize: 11.5,
    titleFontSize: 12,
    titleFontWeight: 600,
    domainColor: AXIS,
    tickColor: AXIS,
    gridColor: RULE,
    gridDash: [2, 3]
  },
  legend: {
    labelColor: INK,
    titleColor: INK,
    labelFontSize: 12,
    titleFontSize: 12,
    titleFontWeight: 600,
    labelFont: "Archivo, sans-serif",
    titleFont: "Archivo, sans-serif"
  },
  header: { labelFont: "Archivo, sans-serif" },
  title: { color: INK, subtitleColor: MUTED, font: "Archivo, sans-serif" },
  text: { font: "Archivo, sans-serif" }
};

// [container, spec, how its marks enter]
//   fade     – the whole chart fades in
//   stagger  – marks appear one after another in data order (e.g. chronologically)
//   draw     – line paths draw from start to end, then the other marks fade in
//   waffle   – each facet "counts up" its 100 squares at the same time
const charts = [
  ["#vis-origins", "charts_new/01_origins_map.json", "stagger"],
  ["#vis-choropleth", "charts_new/02_state_choropleth.json", "fade"],
  ["#vis-radial", "charts_new/03_radial_states.json", "stagger"],
  ["#vis-dumbbell", "charts_new/04_aria_dumbbell.json", "stagger"],
  ["#vis-halloffame", "charts_new/05_hall_of_fame_timeline.json", "stagger"],
  ["#vis-hottest-line", "charts_new/06_hottest100_aussie_share.json", "draw"],
  ["#vis-waffle", "charts_new/07_hottest100_waffle.json", "waffle"],
  ["#vis-votes", "charts_new/08_number_ones_votes.json", "stagger"],
  ["#vis-world", "charts_new/09_world_peaks_map.json", "fade"],
  ["#vis-heatmap", "charts_new/10_peaks_heatmap.json", "stagger"],
  ["#vis-flows", "charts_new/11_number_one_flow_map.json", "draw"]
];

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const embedOptions = { actions: false, renderer: "svg", config: sharedConfig, tooltip: { theme: "custom" } };

// ---------- Mark entrance animations (run once per chart) ----------
const MARKS = ".role-mark path, .role-mark line, .role-mark text";

function clearAfter(el, ms) {
  setTimeout(() => {
    el.classList.remove("pre-anim");
    el.querySelectorAll(MARKS).forEach((m) => {
      m.style.animation = "";
      m.style.strokeDasharray = "";
      m.style.strokeDashoffset = "";
      m.style.transition = "";
      m.style.opacity = "";
    });
  }, ms);
}

function fadeIn(marks, delayFn, duration = 450) {
  marks.forEach((m, i) => {
    m.style.animation = `markIn ${duration}ms ease-out ${delayFn(i)}ms backwards`;
  });
}

function animateChart(el, mode) {
  const all = [...el.querySelectorAll(MARKS)];
  if (mode === "fade") {
    fadeIn(all, () => 0, 700);
    el.classList.remove("pre-anim");
    clearAfter(el, 800);
    return;
  }
  if (mode === "stagger") {
    const step = Math.max(4, Math.min(30, 900 / all.length));
    fadeIn(all, (i) => i * step);
    el.classList.remove("pre-anim");
    clearAfter(el, all.length * step + 500);
    return;
  }
  if (mode === "waffle") {
    const squares = all.filter((m) => m.closest(".mark-symbol"));
    fadeIn(squares, (i) => (i % 100) * 9, 300);
    fadeIn(all.filter((m) => !squares.includes(m)), () => 0);
    el.classList.remove("pre-anim");
    clearAfter(el, 100 * 9 + 400);
    return;
  }
  if (mode === "draw") {
    const lines = all.filter((m) => m.closest(".mark-line"));
    const others = all.filter((m) => !lines.includes(m));
    const drawTime = 1200;
    lines.forEach((p, i) => {
      const len = p.getTotalLength ? p.getTotalLength() : 0;
      const delay = Math.min(i * 25, 900);
      p.style.strokeDasharray = `${len} ${len}`;
      p.style.strokeDashoffset = `${len}`;
      p.style.opacity = "1";
      p.getBoundingClientRect(); // commit the start state before transitioning
      p.style.transition = `stroke-dashoffset ${drawTime}ms ease-in-out ${delay}ms`;
      p.style.strokeDashoffset = "0";
    });
    // base map and areas fade in at once; points/labels follow once the line has drawn
    fadeIn(others, (i) => (others[i].closest(".mark-shape, .mark-area") ? 0 : drawTime * 0.8), 500);
    el.classList.remove("pre-anim");
    clearAfter(el, drawTime + 1000 + 600);
  }
}

// ---------- Embed every chart, animate when it scrolls into view ----------
const chartObserver = !reduceMotion && "IntersectionObserver" in window
  ? new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        chartObserver.unobserve(el);
        el._ready.then(() => requestAnimationFrame(() => animateChart(el, el.dataset.anim)));
      });
    }, { threshold: 0.3 })
  : null;

for (const [selector, spec, mode] of charts) {
  const el = document.querySelector(selector);
  el.dataset.anim = mode;
  if (chartObserver) el.classList.add("pre-anim");
  el._ready = vegaEmbed(el, spec, embedOptions).catch((err) => {
    el.classList.remove("pre-anim");
    el.innerHTML = `<p class="vis-error">This chart could not load (${err.message}).</p>`;
    console.error(spec, err);
  });
  if (chartObserver) chartObserver.observe(el);
}

// ---------- Text reveal ----------
const revealObserver = !reduceMotion && "IntersectionObserver" in window
  ? new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("in"); revealObserver.unobserve(e.target); }
      });
    }, { threshold: 0.1 })
  : null;
document.querySelectorAll(".reveal").forEach((el) => {
  if (revealObserver) revealObserver.observe(el);
  else el.classList.add("in");
});

// ---------- Stats count up once ----------
function countUp(el) {
  const target = Number(el.dataset.count);
  const suffix = el.dataset.suffix || "";
  const start = performance.now();
  const dur = 1100;
  const tick = (now) => {
    const t = Math.min(1, (now - start) / dur);
    const eased = 1 - Math.pow(1 - t, 3);
    el.textContent = Math.round(target * eased) + suffix;
    if (t < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
if (!reduceMotion && "IntersectionObserver" in window) {
  const statObserver = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { countUp(e.target); statObserver.unobserve(e.target); }
    });
  }, { threshold: 0.6 });
  document.querySelectorAll("[data-count]").forEach((el) => statObserver.observe(el));
}

// ---------- Equaliser strip in the masthead ----------
const eq = document.querySelector(".eq");
if (eq) {
  const bars = Math.ceil(window.innerWidth / 18);
  for (let i = 0; i < bars; i++) {
    const s = document.createElement("span");
    s.style.animationDelay = `${-(Math.sin(i * 1.7) + 1) * 0.8}s`;
    s.style.animationDuration = `${1.2 + ((i * 7) % 5) * 0.15}s`;
    eq.appendChild(s);
  }
}
