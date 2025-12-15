(function () {
  const root = document.documentElement;

  function applyTheme(theme) {
    root.dataset.theme = theme;
    localStorage.setItem("theme", theme);

    const btn = document.getElementById("themeToggle");
    if (btn) btn.textContent = (theme === "light") ? "Dark mode" : "Light mode";
  }

  // Load saved theme or follow system preference
  const saved = localStorage.getItem("theme");
  const prefersLight = window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches;
  applyTheme(saved || (prefersLight ? "light" : "dark"));

  document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("themeToggle");
    if (!btn) return;

    btn.addEventListener("click", () => {
      const current = root.dataset.theme || "dark";
      applyTheme(current === "dark" ? "light" : "dark");
    });
  });
})();

