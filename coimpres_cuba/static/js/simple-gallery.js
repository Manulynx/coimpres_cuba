// Galería Simple y Robusta - Fallback
document.addEventListener('DOMContentLoaded', function() {
    const mainMedia = document.getElementById('mainMedia');
    const thumbnails = document.querySelectorAll('.thumbnail-item');
    const videoOverlay = document.getElementById('videoOverlay');
    
    if (!mainMedia || thumbnails.length === 0) {
        console.log('No hay galería para inicializar');
        return;
    }
    
    console.log('Inicializando galería simple con', thumbnails.length, 'thumbnails');
    
    // Configurar cada thumbnail
    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const src = this.dataset.src;
            const type = this.dataset.type;
            const alt = this.dataset.alt || 'Imagen del producto';
            
            console.log('Cambiando media a:', src, 'tipo:', type);
            
            // Actualizar clases activas
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Cambiar el contenido principal
            changeMainMedia(src, type, alt);
        });
    });
    
    function changeMainMedia(src, type, alt) {
        const container = mainMedia.parentNode;
        
        if (type === 'video') {
            // Si es video, crear elemento video
            if (mainMedia.tagName !== 'VIDEO') {
                const video = document.createElement('video');
                video.id = 'mainMedia';
                video.className = mainMedia.className;
                video.style.cssText = mainMedia.style.cssText;
                video.controls = true;
                video.preload = 'metadata';
                video.muted = false; // Permitir audio
                video.playsinline = true; // Para dispositivos móviles
                video.alt = alt;
                
                // Crear fuente de video
                const source = document.createElement('source');
                source.src = src;
                source.type = 'video/mp4';
                video.appendChild(source);
                
                // Agregar texto de respaldo
                video.innerHTML += 'Tu navegador no soporta el elemento video.';
                
                // Event listener para errores de video
                video.addEventListener('error', function(e) {
                    console.error('Error al cargar video:', e);
                    console.log('URL del video:', src);
                });
                
                // Event listener para cuando el video está listo
                video.addEventListener('loadedmetadata', function() {
                    console.log('Video cargado correctamente:', src);
                });
                
                container.replaceChild(video, mainMedia);
                // Actualizar referencia global
                window.currentMainMedia = video;
                
                // Mostrar overlay de video
                if (videoOverlay) {
                    videoOverlay.classList.remove('d-none');
                }
                
                console.log('Video creado:', video);
            } else {
                // Limpiar fuentes existentes
                mainMedia.innerHTML = '';
                const source = document.createElement('source');
                source.src = src;
                source.type = 'video/mp4';
                mainMedia.appendChild(source);
                mainMedia.alt = alt;
                mainMedia.load(); // Recargar el video
            }
        } else {
            // Si es imagen, crear elemento img
            if (mainMedia.tagName !== 'IMG') {
                const img = document.createElement('img');
                img.id = 'mainMedia';
                img.className = mainMedia.className;
                img.style.cssText = mainMedia.style.cssText;
                img.src = src;
                img.alt = alt;
                
                container.replaceChild(img, mainMedia);
                // Actualizar referencia global
                window.currentMainMedia = img;
                
                // Ocultar overlay de video
                if (videoOverlay) {
                    videoOverlay.classList.add('d-none');
                }
            } else {
                mainMedia.src = src;
                mainMedia.alt = alt;
            }
        }
        
        console.log('Media cambiado exitosamente a:', src, 'tipo:', type);
    }
    
    // Funcionalidad de navegación con teclado
    document.addEventListener('keydown', function(e) {
        if (e.target.closest('.product-gallery')) {
            const currentActive = document.querySelector('.thumbnail-item.active');
            const allThumbnails = Array.from(thumbnails);
            const currentIndex = allThumbnails.indexOf(currentActive);
            
            if (currentIndex === -1) return;
            
            let newIndex;
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    newIndex = currentIndex > 0 ? currentIndex - 1 : allThumbnails.length - 1;
                    allThumbnails[newIndex].click();
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    newIndex = currentIndex < allThumbnails.length - 1 ? currentIndex + 1 : 0;
                    allThumbnails[newIndex].click();
                    break;
            }
        }
    });
    
    console.log('Galería simple inicializada correctamente');
});