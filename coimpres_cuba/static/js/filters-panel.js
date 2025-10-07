// Gestión del panel de filtros usando Bootstrap Collapse
document.addEventListener('DOMContentLoaded', () => {
    const filterBody = document.getElementById('filterBody');
    if (!filterBody) return;

    const toggleBtn = document.querySelector('.btn-toggle-filters');
    if (!toggleBtn) return;

    const span = toggleBtn.querySelector('span');
    if (!span) return;

    // Actualizar el texto del botón cuando el collapse cambia
    filterBody.addEventListener('show.bs.collapse', () => {
        span.textContent = 'Ocultar';
        toggleBtn.setAttribute('aria-expanded', 'true');
    });

    filterBody.addEventListener('hide.bs.collapse', () => {
        span.textContent = 'Mostrar';
        toggleBtn.setAttribute('aria-expanded', 'false');
    });

    // Si hay un filtro activo, mostrar el panel automáticamente en móvil
    const hasActiveFilters = document.querySelector('.alert-info');
    if (hasActiveFilters && window.innerWidth < 992) {
        const bsCollapse = new bootstrap.Collapse(filterBody, {
            show: true
        });
    }
});