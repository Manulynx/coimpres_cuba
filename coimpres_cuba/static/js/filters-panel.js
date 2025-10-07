// Toggle de panel de filtros (extraído de product_list.html)
// Soporta múltiples botones con clase .btn-toggle-filters
(function(){
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-toggle-filters').forEach(btn => {
      const targetSel = btn.getAttribute('data-target');
      if (!targetSel) return;
      const target = document.querySelector(targetSel);
      if (!target) return;

      // Estado inicial
      const span = btn.querySelector('span');
      const sync = () => {
        const open = target.classList.contains('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        if (span) span.textContent = open ? 'Ocultar' : 'Mostrar';
      };
      sync();

      btn.addEventListener('click', e => {
        e.preventDefault();
        target.classList.toggle('open');
        sync();
      });
    });
  });
})();
