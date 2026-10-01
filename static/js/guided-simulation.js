// Simulação guiada: apenas animação e progressão visual. Nenhum cálculo tributário aqui:
// os valores chegam prontos do servidor (atributos data-count / data-final).
(() => {
  const root = document.querySelector("[data-guided]");
  if (!root) return;
  const stage = root.querySelector("[data-stage]");
  const scenes = [...root.querySelectorAll("[data-scene]")];
  const summary = root.querySelector("[data-summary]");
  const skip = root.querySelector("[data-skip]");
  const replay = root.querySelector("[data-replay]");
  const stepLabel = root.querySelector("[data-step]");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  const HOLD = 3600; // tempo de cada quadro (ms)
  const COUNT_MS = 1600; // duração dos contadores (ms)

  let index = -1;
  let timer = 0;
  let rafs = new Set();

  function clearTimers() {
    window.clearTimeout(timer);
    rafs.forEach((id) => cancelAnimationFrame(id));
    rafs.clear();
  }

  // contador: só interpola o número mostrado até o valor final vindo do servidor
  function animateCount(el) {
    const target = Number(el.dataset.count);
    if (!Number.isFinite(target) || reduce.matches) { el.textContent = el.dataset.final; return; }
    const formatter = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
    const start = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - start) / COUNT_MS);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = t < 1 ? formatter.format(target * eased) : el.dataset.final;
      if (t < 1) rafs.add(requestAnimationFrame(step));
    };
    el.textContent = formatter.format(0);
    rafs.add(requestAnimationFrame(step));
  }

  function showSummary(focus) {
    clearTimers();
    scenes.forEach((s) => s.classList.remove("is-active", "is-leaving"));
    stage.classList.add("is-done");
    summary.classList.add("is-shown");
    stepLabel.textContent = "";
    skip.hidden = true;
    replay.hidden = false;
    root.querySelectorAll("[data-count]").forEach((el) => { el.textContent = el.dataset.final; });
    if (focus) summary.focus({ preventScroll: true });
  }

  function show(i) {
    if (i >= scenes.length) { showSummary(true); return; }
    const previous = scenes[index];
    if (previous) {
      previous.classList.remove("is-active");
      previous.classList.add("is-leaving");
      window.setTimeout(() => previous.classList.remove("is-leaving"), 650);
    }
    index = i;
    const scene = scenes[i];
    scene.querySelectorAll(".g-checks li").forEach((li, n) => li.style.setProperty("--i", n));
    scene.querySelectorAll(".tick").forEach((t, n) => t.style.setProperty("--i", n));
    scene.classList.add("is-active");
    scene.querySelectorAll("[data-count]").forEach(animateCount);
    stepLabel.textContent = `Quadro ${i + 1} de ${scenes.length}`;
    timer = window.setTimeout(() => show(i + 1), HOLD);
  }

  function start() {
    clearTimers();
    summary.classList.remove("is-shown");
    stage.classList.remove("is-done");
    scenes.forEach((s) => s.classList.remove("is-active", "is-leaving"));
    index = -1;
    skip.hidden = false;
    replay.hidden = true;
    show(0);
  }

  skip.addEventListener("click", () => showSummary(true));
  replay.addEventListener("click", start);

  if (reduce.matches) showSummary(false);
  else start();
})();
