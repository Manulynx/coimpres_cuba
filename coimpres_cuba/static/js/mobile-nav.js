/**
 * Mobile Navigation Enhancement
 * Mejora la experiencia de navegación móvil con animaciones y transiciones
 */

document.addEventListener('DOMContentLoaded', function() {
    // Mejorar la experiencia del botón hamburguesa
    enhanceMobileNavToggle();
    
    // Añadir comportamiento de cierre al hacer clic fuera del menú
    setupClickOutsideClose();
});

/**
 * Mejora el comportamiento del botón hamburguesa
 */
function enhanceMobileNavToggle() {
    const navToggle = document.querySelector('.navbar-toggler');
    const navCollapse = document.querySelector('.navbar-collapse');
    
    if (!navToggle || !navCollapse) return;
    
    // Añadir clase con efecto de rebote al mostrar/ocultar
    navToggle.addEventListener('click', function() {
        // Pequeña vibración táctil en dispositivos que la soportan
        if (window.navigator && window.navigator.vibrate) {
            window.navigator.vibrate(50);
        }
        
        // Añadir clase de animación cuando se expande
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        
        // Si el menú está expandiéndose
        if (!isExpanded) {
            navToggle.classList.add('pulse-animation');
            
            // Remover la clase después de que termine la animación
            setTimeout(() => {
                navToggle.classList.remove('pulse-animation');
            }, 400);
        }
    });
}

/**
 * Configura el cierre del menú al hacer clic fuera de él
 */
function setupClickOutsideClose() {
    document.addEventListener('click', function(event) {
        const navToggle = document.querySelector('.navbar-toggler');
        const navCollapse = document.querySelector('.navbar-collapse');
        
        if (!navToggle || !navCollapse) return;
        
        // Si el menú está abierto y el clic fue fuera del menú y no en el botón hamburguesa
        const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
        const clickedInsideMenu = navCollapse.contains(event.target);
        const clickedOnToggle = navToggle.contains(event.target);
        
        if (isExpanded && !clickedInsideMenu && !clickedOnToggle) {
            // Activar el botón hamburguesa programáticamente para cerrar el menú
            navToggle.click();
        }
    });
}