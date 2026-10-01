// Linha do tempo da reforma: apenas alterna o painel do ano. Sem regra fiscal.
(() => {
  const timeline = document.querySelector("[data-reform-timeline]");
  if (!timeline) return;
  const panels = [...document.querySelectorAll("[data-panel]")];

  function select(year) {
    timeline.querySelectorAll("[data-year]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.year === year)));
    panels.forEach((p) => { p.hidden = p.dataset.panel !== year; });
  }

  timeline.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-year]");
    if (btn) select(btn.dataset.year);
  });
  const first = timeline.querySelector("[data-year]");
  if (first) select(first.dataset.year);
})();
