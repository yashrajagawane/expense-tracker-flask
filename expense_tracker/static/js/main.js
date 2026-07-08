// Ledger — small UI helpers (theme toggle, flash auto-dismiss)
(function () {
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');

  function setIcon() {
    if (!toggle) return;
    const dark = root.getAttribute('data-theme') === 'dark';
    toggle.innerHTML = dark
      ? '<i class="fa-solid fa-sun"></i><span class="tt-label">Light</span>'
      : '<i class="fa-solid fa-moon"></i><span class="tt-label">Dark</span>';
  }
  setIcon();

  if (toggle) {
    toggle.addEventListener('click', () => {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      setIcon();
    });
  }

  // Auto dismiss flash messages after 4s
  document.querySelectorAll('.flash').forEach((el) => {
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transform = 'translateX(20px)';
      el.style.transition = 'all .3s ease';
      setTimeout(() => el.remove(), 300);
    }, 4000);
  });
})();
