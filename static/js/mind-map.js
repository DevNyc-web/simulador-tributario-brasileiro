// Mapa mental: câmera guiada por scroll. Apenas lógica visual; nenhum cálculo tributário aqui.
(() => {
  const root = document.documentElement;
  if (!root.classList.contains("js")) return;

  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  const world = document.getElementById("world");
  const svg = document.getElementById("links");
  const hint = document.getElementById("hint");
  const indNum = document.getElementById("ind-num");
  const indTotal = document.getElementById("ind-total");
  const indBar = document.getElementById("ind-bar");
  const NS = "http://www.w3.org/2000/svg";

  // Paradas do percurso, em ordem; posição do centro vem dos atributos data-x / data-y.
  const stops = [...document.querySelectorAll("[data-stop]")]
    .sort((a, b) => Number(a.dataset.stop) - Number(b.dataset.stop))
    .map((el) => ({ el, x: Number(el.dataset.x), y: Number(el.dataset.y), fit: 1 }));
  const N = stops.length;
  const SEGMENTS = N - 1;
  const FUTURE_FROM = 14; // trechos que levam ao roadmap e de volta ao núcleo são pontilhados
  const HUB = N - 1;
  const BRANCHES = [5, 6, 7, 8, 9];
  const DIP = 0.3; // quanto a câmera se afasta no meio do trecho para mostrar o mapa maior

  let vw = 0;
  let vh = 0;
  let cur = 0;
  let target = 0;
  let raf = 0;
  let last = 0;
  let activeIdx = -1;
  const segs = []; // { base, done, len }
  let traveler = null;

  // ---------- conexões (SVG) ----------
  function curve(a, b, back) {
    const dx = b.x - a.x;
    const dy = b.y - a.y;
    let c1;
    let c2;
    if (back) {
      c1 = [a.x, a.y - (a.y - b.y) * 0.6];
      c2 = [b.x + (a.x - b.x) * 0.5, b.y];
    } else if (Math.abs(dx) >= Math.abs(dy)) {
      c1 = [a.x + dx * 0.5, a.y];
      c2 = [b.x - dx * 0.5, b.y];
    } else {
      c1 = [a.x, a.y + dy * 0.5];
      c2 = [b.x, b.y - dy * 0.5];
    }
    return `M${a.x},${a.y} C${c1[0]},${c1[1]} ${c2[0]},${c2[1]} ${b.x},${b.y}`;
  }

  function path(d, cls) {
    const p = document.createElementNS(NS, "path");
    p.setAttribute("d", d);
    p.setAttribute("class", cls);
    svg.appendChild(p);
    return p;
  }

  function buildLinks() {
    BRANCHES.forEach((i) => path(curve(stops[HUB], stops[i], false), "branch"));
    for (let i = 0; i < SEGMENTS; i += 1) {
      const future = i >= FUTURE_FROM ? " future" : "";
      const d = curve(stops[i], stops[i + 1], i === SEGMENTS - 1);
      const base = path(d, `base${future}`);
      const done = path(d, `done${future}`);
      const len = base.getTotalLength();
      done.style.strokeDasharray = `${len}`;
      done.style.strokeDashoffset = `${len}`;
      segs.push({ base, done, len });
    }
    traveler = document.createElementNS(NS, "circle");
    traveler.setAttribute("r", "16");
    svg.appendChild(traveler);
  }

  // ---------- câmera ----------
  function measure() {
    vw = window.innerWidth;
    vh = window.innerHeight;
    const maxScale = vw < 700 ? 1.5 : 1.15;
    stops.forEach((s) => {
      const fit = Math.min((vw * 0.9) / s.el.offsetWidth, (vh * 0.8) / s.el.offsetHeight);
      s.fit = Math.max(0.18, Math.min(maxScale, fit));
    });
  }

  // plateau perto de cada parada: a câmera "descansa" e só se move no miolo do trecho
  function ease(t) {
    const u = Math.max(0, Math.min(1, (t - 0.22) / 0.56));
    return u * u * (3 - 2 * u);
  }

  function render(p) {
    const s = p * SEGMENTS;
    const i = Math.min(SEGMENTS - 1, Math.floor(s));
    const t = s - i;
    const e = ease(t);
    const a = stops[i];
    const b = stops[i + 1];

    const x = a.x + (b.x - a.x) * e;
    const y = a.y + (b.y - a.y) * e;
    let scale = Math.exp(Math.log(a.fit) + (Math.log(b.fit) - Math.log(a.fit)) * e);
    if (!reduce.matches) scale *= 1 - DIP * Math.sin(Math.PI * e);
    world.style.transform = `translate3d(${vw / 2 - x * scale}px, ${vh / 2 - y * scale}px, 0) scale(${scale})`;

    // trilha percorrida e ponto viajante
    segs.forEach((sg, k) => {
      const shown = k < i ? 1 : k === i ? e : 0;
      sg.done.style.strokeDashoffset = `${sg.len * (1 - shown)}`;
    });
    const pt = segs[i].base.getPointAtLength(segs[i].len * e);
    traveler.setAttribute("cx", pt.x);
    traveler.setAttribute("cy", pt.y);

    // destaque do núcleo atual
    const idx = Math.round(s);
    if (idx !== activeIdx) {
      activeIdx = idx;
      stops.forEach((st, k) => st.el.classList.toggle("is-active", k === idx));
      indNum.textContent = String(idx).padStart(2, "0");
    }
    indBar.style.transform = `scaleY(${p})`;
    hint.classList.toggle("is-hidden", p > 0.02);
  }

  // ---------- progresso por scroll (scroll nativo; sem captura de roda, arrasto ou zoom) ----------
  function readTarget() {
    const max = root.scrollHeight - window.innerHeight;
    target = max > 0 ? Math.max(0, Math.min(1, window.scrollY / max)) : 0;
  }

  function tick(now) {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    if (reduce.matches) cur = target;
    else cur += (target - cur) * (1 - Math.exp(-dt * 7));
    if (Math.abs(target - cur) < 0.00005) cur = target;
    render(cur);
    raf = cur === target ? 0 : requestAnimationFrame(tick);
  }

  function request() {
    if (raf) return;
    last = performance.now();
    raf = requestAnimationFrame(tick);
  }

  function relayout() {
    measure();
    readTarget();
    cur = target;
    render(cur);
  }

  indTotal.textContent = String(N - 1).padStart(2, "0");
  buildLinks();
  relayout();
  window.addEventListener("scroll", () => { readTarget(); request(); }, { passive: true });
  window.addEventListener("resize", relayout);
  window.addEventListener("orientationchange", relayout);
  window.addEventListener("load", relayout);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(relayout);
})();
