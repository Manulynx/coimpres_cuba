// Toggle de panel de filtros (extraído de product_list.html)
// Soporta múltiples botones con clase .btn-toggle-filters
(function(){
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-toggle-filters').forEach(btn => {
      const targetSelector = btn.getAttribute('data-target');
      if(!targetSelector) return;
      const target = document.querySelector(targetSelector);
      if(!target) return;
      // Estado inicial accesible
      btn.setAttribute('aria-expanded', target.classList.contains('open') ? 'true' : 'false');
      btn.setAttribute('aria-controls', target.id || '');
      btn.addEventListener('click', () => {
        target.classList.toggle('open');
        const isOpen = target.classList.contains('open');
        const span = btn.querySelector('span');
        if(span) span.textContent = isOpen ? 'Ocultar' : 'Mostrar';
        btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      });
    });
  });
})();
