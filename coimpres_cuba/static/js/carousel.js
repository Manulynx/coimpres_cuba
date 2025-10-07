// Carrusel automático infinito - Desplazamiento circular continuo
document.addEventListener('DOMContentLoaded', function() {
    const track = document.getElementById('carouselTrack');
    if (!track) {
        console.log('Carrusel no encontrado');
        return;
    }
    
    const originalProducts = Array.from(track.children);
    const totalProducts = originalProducts.length;
    console.log('Total productos originales:', totalProducts);
    
    if (totalProducts === 0) {
        console.log('No hay productos para mostrar');
        return;
    }
    
    let currentIndex = 0;
    let autoSlideInterval;
    let isTransitioning = false;
    
    // Función para obtener productos visibles según el tamaño de pantalla
    function getVisibleProducts() {
        if (window.innerWidth <= 768) return 1;
        if (window.innerWidth <= 992) return 2;
        return 3;
    }
    
    // Crear productos duplicados para efecto infinito
    function setupInfiniteCarousel() {
        const visibleProducts = getVisibleProducts();
        
        // Limpiar productos duplicados existentes
        track.innerHTML = '';
        
        // Agregar productos originales
        originalProducts.forEach(product => {
            track.appendChild(product.cloneNode(true));
        });
        
        // Duplicar algunos productos al final para efecto infinito
        for (let i = 0; i < visibleProducts; i++) {
            const clonedProduct = originalProducts[i].cloneNode(true);
            clonedProduct.classList.add('cloned');
            track.appendChild(clonedProduct);
        }
        
        console.log('Carrusel infinito configurado. Total elementos:', track.children.length);
    }
    
    // Función para mover el carrusel a un índice específico
    function moveToIndex(index, immediate = false) {
        const visibleProducts = getVisibleProducts();
        const slideWidth = 100 / visibleProducts;
        const translateX = -(index * slideWidth);
        
        if (immediate) {
            track.style.transition = 'none';
        } else {
            track.style.transition = 'transform 0.8s ease-in-out';
        }
        
        track.style.transform = `translateX(${translateX}%)`;
        currentIndex = index;
        
        console.log(`Moviendo a índice ${index}, translateX: ${translateX}%`);
        
        if (immediate) {
            // Restaurar transición después de un frame
            requestAnimationFrame(() => {
                track.style.transition = 'transform 0.8s ease-in-out';
            });
        }
    }
    
    // Función para avanzar automáticamente con efecto infinito
    function autoSlide() {
        const visibleProducts = getVisibleProducts();
        
        if (totalProducts <= visibleProducts) {
            console.log('No hay suficientes productos para hacer carrusel');
            return;
        }
        
        if (isTransitioning) return;
        
        isTransitioning = true;
        currentIndex++;
        
        // Si hemos llegado al final (productos duplicados), resetear sin animación
        if (currentIndex >= totalProducts) {
            moveToIndex(currentIndex);
            
            // Después de la transición, saltar al principio sin animación
            setTimeout(() => {
                currentIndex = 0;
                moveToIndex(currentIndex, true);
                isTransitioning = false;
            }, 800); // Duración de la transición
        } else {
            moveToIndex(currentIndex);
            setTimeout(() => {
                isTransitioning = false;
            }, 800);
        }
    }
    
    // Función para mover manualmente
    window.moveCarousel = function(direction) {
        if (isTransitioning) return;
        
        const visibleProducts = getVisibleProducts();
        
        if (totalProducts <= visibleProducts) return;
        
        isTransitioning = true;
        clearInterval(autoSlideInterval);
        
        if (direction > 0) {
            // Avanzar
            currentIndex++;
            if (currentIndex >= totalProducts) {
                moveToIndex(currentIndex);
                setTimeout(() => {
                    currentIndex = 0;
                    moveToIndex(currentIndex, true);
                    isTransitioning = false;
                    startAutoSlide();
                }, 800);
            } else {
                moveToIndex(currentIndex);
                setTimeout(() => {
                    isTransitioning = false;
                    startAutoSlide();
                }, 800);
            }
        } else {
            // Retroceder
            if (currentIndex <= 0) {
                currentIndex = totalProducts;
                moveToIndex(currentIndex, true);
                setTimeout(() => {
                    currentIndex = totalProducts - 1;
                    moveToIndex(currentIndex);
                    setTimeout(() => {
                        isTransitioning = false;
                        startAutoSlide();
                    }, 800);
                }, 50);
            } else {
                currentIndex--;
                moveToIndex(currentIndex);
                setTimeout(() => {
                    isTransitioning = false;
                    startAutoSlide();
                }, 800);
            }
        }
    };
    
    // Iniciar carrusel automático
    function startAutoSlide() {
        const visibleProducts = getVisibleProducts();
        
        if (totalProducts > visibleProducts) {
            clearInterval(autoSlideInterval);
            autoSlideInterval = setInterval(autoSlide, 2000); // Cada 2 segundos
            console.log('Carrusel automático iniciado');
        }
    }
    
    // Pausar al hacer hover
    const carousel = document.getElementById('autoProductCarousel');
    if (carousel) {
        carousel.addEventListener('mouseenter', function() {
            clearInterval(autoSlideInterval);
            console.log('Carrusel pausado');
        });
        
        carousel.addEventListener('mouseleave', function() {
            if (!isTransitioning) {
                startAutoSlide();
                console.log('Carrusel reanudado');
            }
        });
    }
    
    // Ajustar en cambio de tamaño de ventana
    window.addEventListener('resize', function() {
        console.log('Redimensionando ventana');
        clearInterval(autoSlideInterval);
        isTransitioning = false;
        
        // Reconfigurar carrusel para nuevo tamaño
        setupInfiniteCarousel();
        currentIndex = 0;
        moveToIndex(currentIndex, true);
        
        setTimeout(() => {
            startAutoSlide();
        }, 100);
    });
    
    // Inicializar carrusel infinito
    console.log('Inicializando carrusel infinito...');
    setupInfiniteCarousel();
    moveToIndex(0, true);
    startAutoSlide();
});