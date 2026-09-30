// Apenas comportamento visual e validação estrutural. Nenhuma regra fiscal aqui.

// Menu mobile
const toggle = document.querySelector(".menu-toggle");
const nav = document.getElementById("nav");
toggle?.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", open);
});

// "1.234,56" | "1234.56" | "R$ 10" -> número, ou NaN se o formato for inválido
function parseMoney(text) {
  let s = text.replace(/R\$|\s/g, "");
  if (s.includes(",")) s = s.replace(/\./g, "").replace(",", ".");
  return /^\d+(\.\d{1,2})?$/.test(s) ? Number(s) : NaN;
}

const formatMoney = (n) =>
  n.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function validateField(el) {
  const msg = document.getElementById(`${el.id}-msg`);
  let error = "";
  if (el.dataset.kind === "year") {
    if (!el.value) error = "Selecione um ano entre 2026 e 2033.";
  } else if (el.dataset.kind === "money" && "required" in el.dataset) {
    const n = parseMoney(el.value);
    if (!el.value.trim()) error = "Campo obrigatório.";
    else if (Number.isNaN(n)) error = "Informe um valor válido (ex.: 5000,00).";
    else if (n <= 0 && !("allowZero" in el.dataset)) error = "Informe um valor maior que zero.";
  }
  el.setAttribute("aria-invalid", error ? "true" : "false");
  msg.textContent = error;
  return !error;
}

// Formulários de simulação: valida estrutura e NÃO calcula
document.querySelectorAll("form[data-sim]").forEach((form) => {
  const inputs = [...form.querySelectorAll("[data-kind]")].filter((el) => !el.readOnly);
  const status = document.querySelector("[data-status]");

  inputs.forEach((el) => {
    el.addEventListener("blur", () => {
      validateField(el);
      if (el.dataset.kind === "money") {
        const n = parseMoney(el.value);
        if (!Number.isNaN(n)) el.value = formatMoney(n);
      }
    });
  });

  // Campos anuais espelham o mensal (exibição apenas; não é regra tributária)
  form.querySelectorAll("input[id$='_mensal']").forEach((monthly) => {
    const annual = form.querySelector(`#${monthly.id.replace("_mensal", "_anual")}`);
    monthly.addEventListener("input", () => {
      const n = parseMoney(monthly.value);
      annual.value = Number.isNaN(n) ? "" : formatMoney(n * 12);
    });
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const results = inputs.map(validateField);
    if (status) status.hidden = results.includes(false);
    const firstBad = inputs.find((el) => el.getAttribute("aria-invalid") === "true");
    firstBad?.focus();
  });

  form.addEventListener("reset", () => {
    inputs.forEach((el) => {
      el.removeAttribute("aria-invalid");
      document.getElementById(`${el.id}-msg`).textContent = "";
    });
    if (status) status.hidden = true;
  });
});

// Escolha de simulação
const choice = document.querySelector("form[data-choice]");
choice?.addEventListener("submit", (e) => {
  e.preventDefault();
  const picked = choice.querySelector("input[name=perfil]:checked");
  if (picked) window.location.href = picked.value;
  else choice.querySelector("[data-choice-msg]").textContent = "Escolha um perfil para continuar.";
});

// Timeline da reforma
const timeline = document.querySelector("[data-timeline]");
timeline?.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-year]");
  if (!btn) return;
  timeline.querySelectorAll("[data-year]").forEach((b) => b.setAttribute("aria-pressed", b === btn));
  document.querySelector("[data-year-title]").textContent = btn.dataset.year;
});
