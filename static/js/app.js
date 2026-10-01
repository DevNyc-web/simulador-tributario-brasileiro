// Apenas comportamento visual e validação estrutural de formato. Nenhuma regra fiscal aqui:
// todo cálculo, limite, alíquota e escolha de anexo acontece no servidor (Python).

// Menu mobile
const toggle = document.querySelector(".menu-toggle");
const nav = document.getElementById("nav");
toggle?.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", open);
});

// "1.234,56" | "1234.56" | "R$ 10" -> true se o FORMATO for válido (o servidor converte e valida de novo)
function validMoneyFormat(text) {
  const s = text.replace(/R\$|\s/g, "");
  return /^(\d{1,3}(\.\d{3})*|\d+),\d{1,2}$/.test(s) || /^\d+(\.\d{1,2})?$/.test(s) || /^\d{1,3}(\.\d{3})+$/.test(s);
}

function setError(el, error) {
  const msg = document.getElementById(`${el.id}-msg`);
  el.setAttribute("aria-invalid", error ? "true" : "false");
  if (msg) msg.textContent = error;
  return !error;
}

function validateField(el) {
  if (el.closest("[hidden]")) return true;
  // modo estável: campos avançados em branco são preenchidos pelo servidor
  const stable = el.form && el.form.querySelector("#hist_modo");
  if (stable && stable.checked && el.closest("[data-advanced]") && !el.value.trim()) return setError(el, "");
  const value = el.value.trim();
  const required = "required" in el.dataset;
  if (el.dataset.kind === "money") {
    if (!value) return setError(el, required ? "Campo obrigatório." : "");
    return setError(el, validMoneyFormat(value) ? "" : "Informe um valor válido (ex.: 8.000,50).");
  }
  if (el.dataset.kind === "integer") {
    if (!value) return setError(el, "Campo obrigatório.");
    const n = Number(value);
    const min = el.min === "" ? -Infinity : Number(el.min);
    const max = el.max === "" ? Infinity : Number(el.max);
    return setError(el, Number.isInteger(n) && n >= min && n <= max ? "" : "Informe um número inteiro válido.");
  }
  if (el.tagName === "SELECT") return setError(el, value ? "" : "Selecione uma opção.");
  return true;
}

// Histórico mensal: mostra/oculta linhas conforme os meses desde a abertura (só interface)
function updateHistory(form) {
  const meses = form.querySelector("#meses_desde_abertura");
  if (!meses) return;
  const n = parseInt(meses.value, 10);
  const needed = Number.isNaN(n) || n < 1 ? 0 : n < 13 ? n - 1 : 12;
  const stable = form.querySelector("#hist_modo");
  const isStable = Boolean(stable && stable.checked);
  form.querySelectorAll("[data-history-row]").forEach((row) => {
    const visible = !isStable && Number(row.dataset.historyRow) <= needed;
    row.hidden = !visible;
    row.querySelectorAll("[data-kind=money]").forEach((el) => {
      if (visible) el.setAttribute("data-required", "");
      else el.removeAttribute("data-required");
    });
  });
  const box = form.querySelector("[data-history]");
  if (box) box.hidden = isStable || needed === 0;
}

// Campo de lucro contábil só aparece com escrituração (validação real fica no servidor)
function updateLucro(form) {
  const modo = form.querySelector("#modo_apuracao");
  const wrap = form.querySelector("[data-lucro-field]");
  if (!modo || !wrap) return;
  const show = modo.value === "COM_ESCRITURACAO";
  wrap.hidden = !show;
  const input = wrap.querySelector("[data-kind=money]");
  if (show) input.setAttribute("data-required", "");
  else input.removeAttribute("data-required");
}

document.querySelectorAll("form[data-sim]").forEach((form) => {
  const inputs = () => [...form.querySelectorAll("[data-kind], select")];

  inputs().forEach((el) => el.addEventListener("blur", () => validateField(el)));
  form.querySelector("#meses_desde_abertura")?.addEventListener("input", () => updateHistory(form));
  form.querySelector("#hist_modo")?.addEventListener("change", () => updateHistory(form));
  form.querySelector("#modo_apuracao")?.addEventListener("change", () => updateLucro(form));
  updateHistory(form);
  updateLucro(form);

  // Envia ao servidor; só bloqueia se o formato estiver claramente inválido
  form.addEventListener("submit", (e) => {
    const results = inputs().map(validateField);
    if (results.includes(false)) {
      e.preventDefault();
      inputs().find((el) => el.getAttribute("aria-invalid") === "true")?.focus();
    }
  });
});

// Foco no resumo de erros devolvido pelo servidor
document.querySelector("[data-error-summary]")?.focus();

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
