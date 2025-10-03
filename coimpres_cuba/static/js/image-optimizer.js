/**
 * Optimización de imágenes para Coimpre SRL
 * Este script mejora la carga y renderización de imágenes
 */

document.addEventListener('DOMContentLoaded', function() {
    // Añadir atributo loading="lazy" a todas las imágenes que no lo tengan
    const images = document.querySelectorAll('img:not([loading])');
    images.forEach(img => {
        img.setAttribute('loading', 'lazy');
    });

    // Manejar errores de carga de imágenes
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function() {
            // Mostrar una imagen predeterminada o aplicar una clase de error
            if (!this.classList.contains('error-handled')) {
                this.classList.add('error-handled');
                this.src = '/static/img/no-image.jpg';
                this.alt = 'Imagen no disponible';
            }
        });
    });

    // Optimizar las imágenes del carrusel o galerías si existen
    const carouselImages = document.querySelectorAll('.carousel-item img');
    if (carouselImages.length > 0) {
        // Cargar solo las imágenes visibles inicialmente
        const visibleCarouselImage = document.querySelector('.carousel-item.active img');
        if (visibleCarouselImage) {
            visibleCarouselImage.setAttribute('loading', 'eager');
        }
    }

    // Aplicar clases para animaciones de entrada suaves a imágenes
    const productImages = document.querySelectorAll('.product-card img, .category-card img');
    productImages.forEach(img => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('img-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        observer.observe(img);
    });
});