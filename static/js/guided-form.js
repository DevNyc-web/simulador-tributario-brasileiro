// Formulário guiado: só mostra/oculta o campo de ramo conforme o enquadramento escolhido.
// A validação real é feita no servidor.
(() => {
  const form = document.querySelector("[data-guided-form]");
  if (!form) return;
  const radios = [...form.querySelectorAll("input[name=enquadramento]")];
  const panels = [...form.querySelectorAll("[data-show-for]")];

  function update() {
    const picked = radios.find((r) => r.checked);
    panels.forEach((p) => { p.hidden = !picked || p.dataset.showFor !== picked.value; });
  }

  radios.forEach((r) => r.addEventListener("change", update));
  update();
})();
