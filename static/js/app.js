// Apenas comportamento visual. Nenhuma regra fiscal aqui.
const toggle = document.querySelector(".menu-toggle");
const nav = document.getElementById("nav");
toggle?.addEventListener("click", () => {
  const open = nav.classList.toggle("open");
  toggle.setAttribute("aria-expanded", open);
});
