// Galería Profesional de Producto - JavaScript

class ProductGallery {
    constructor() {
        this.currentIndex = 0;
        this.modalCurrentIndex = 0;
        this.mediaItems = [];
        this.thumbnailsTrack = document.getElementById('thumbnailsTrack');
        this.mainMedia = document.getElementById('mainMedia');
        this.videoOverlay = document.getElementById('videoOverlay');
        this.mediaCounter = document.getElementById('mediaCounter');
        this.totalMedia = document.getElementById('totalMedia');
        this.prevBtn = document.getElementById('thumbPrev');
        this.nextBtn = document.getElementById('thumbNext');
        
        this.init();
    }
    
    init() {
        // Verificar que los elementos existen
        if (!this.thumbnailsTrack) {
            console.warn('thumbnailsTrack no encontrado');
            return;
        }
        
        if (!this.mainMedia) {
            console.warn('mainMedia no encontrado');
            return;
        }
        
        this.loadMediaItems();
        this.setupEventListeners();
        this.updateUI();
        this.setupKeyboardNavigation();
        
        console.log('Galería inicializada con', this.mediaItems.length, 'elementos');
    }
    
    loadMediaItems() {
        const thumbnails = this.thumbnailsTrack?.querySelectorAll('.thumbnail-item');
        if (!thumbnails) return;
        
        this.mediaItems = Array.from(thumbnails).map((item, index) => ({
            element: item,
            type: item.dataset.type,
            src: item.dataset.src,
            alt: item.dataset.alt,
            index: index
        }));
        
        // Marcar el primer elemento como activo
        if (this.mediaItems.length > 0) {
            this.setActiveItem(0);
        }
    }
    
    setupEventListeners() {
        // Click en thumbnails
        this.mediaItems.forEach((item, index) => {
            item.element.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Click en thumbnail', index, item.src);
                this.setActiveItem(index);
                this.scrollToThumbnail(index);
            });
        });
        
        // Botones de navegación
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.navigatePrev());
        }
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.navigateNext());
        }
        
        // Click en imagen principal para abrir modal - DESHABILITADO
        // if (this.mainMedia) {
        //     this.mainMedia.addEventListener('click', () => this.openModal());
        // }
        
        // Touch events para móvil
        this.setupTouchEvents();
    }
    
    setupTouchEvents() {
        if (!this.mainMedia) return;
        
        let startX = 0;
        let startY = 0;
        
        this.mainMedia.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        
        this.mainMedia.addEventListener('touchend', (e) => {
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            const diffX = startX - endX;
            const diffY = startY - endY;
            
            // Detectar swipe horizontal
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                if (diffX > 0) {
                    this.navigateNext();
                } else {
                    this.navigatePrev();
                }
            }
        });
    }
    
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (document.activeElement?.closest('.product-gallery')) {
                switch(e.key) {
                    case 'ArrowLeft':
                        e.preventDefault();
                        this.navigatePrev();
                        break;
                    case 'ArrowRight':
                        e.preventDefault();
                        this.navigateNext();
                        break;
                    // Enter y Space para abrir modal - DESHABILITADO
                    // case 'Enter':
                    // case ' ':
                    //     e.preventDefault();
                    //     this.openModal();
                    //     break;
                }
            }
        });
    }
    
    setActiveItem(index) {
        if (index < 0 || index >= this.mediaItems.length) return;
        
        // Remover clase activa de todos los elementos
        this.mediaItems.forEach(item => {
            item.element.classList.remove('active');
        });
        
        // Agregar clase activa al elemento actual
        this.mediaItems[index].element.classList.add('active');
        this.currentIndex = index;
        
        // Actualizar media principal
        this.updateMainMedia(this.mediaItems[index]);
        this.updateCounter();
        this.updateNavigationButtons();
    }
    
    updateMainMedia(mediaItem) {
        if (!this.mainMedia || !mediaItem) return;
        
        const isVideo = mediaItem.type === 'video';
        const container = this.mainMedia.parentNode;
        
        // Remover el elemento actual
        this.mainMedia.remove();
        
        if (isVideo) {
            // Crear elemento video
            const video = document.createElement('video');
            video.className = 'img-fluid rounded shadow-lg';
            video.alt = mediaItem.alt;
            video.style.cssText = 'width: 100%; max-height: 450px; object-fit: contain; background-color: #000; border-radius: 12px;';
            video.id = 'mainMedia';
            video.controls = true;
            video.preload = 'metadata';
            video.muted = false;
            video.playsinline = true;
            
            // Crear fuente de video
            const source = document.createElement('source');
            source.src = mediaItem.src;
            source.type = 'video/mp4';
            video.appendChild(source);
            
            // Texto de respaldo
            video.innerHTML += 'Tu navegador no soporta el elemento video.';
            
            // Event listeners para debugging
            video.addEventListener('error', function(e) {
                console.error('Error al cargar video:', e);
                console.log('URL del video:', mediaItem.src);
            });
            
            video.addEventListener('loadedmetadata', function() {
                console.log('Video cargado correctamente:', mediaItem.src);
            });
            
            // Agregar al contenedor antes del overlay
            container.insertBefore(video, this.videoOverlay);
            this.mainMedia = video;
            
            // Mostrar overlay de video
            if (this.videoOverlay) {
                this.videoOverlay.classList.remove('d-none');
            }
            
            console.log('Video actualizado:', video);
        } else {
            // Crear elemento imagen
            const img = document.createElement('img');
            img.src = mediaItem.src;
            img.className = 'img-fluid rounded shadow-lg';
            img.alt = mediaItem.alt;
            img.style.cssText = 'width: 100%; max-height: 450px; object-fit: scale-down; background-color: #f8f9fa; border-radius: 12px;';
            img.id = 'mainMedia';
            
            // Agregar al contenedor antes del overlay
            container.insertBefore(img, this.videoOverlay);
            this.mainMedia = img;
            
            // Ocultar overlay de video
            if (this.videoOverlay) {
                this.videoOverlay.classList.add('d-none');
            }
        }
        
        // Re-agregar event listeners - DESHABILITADO
        // this.mainMedia.addEventListener('click', () => this.openModal());
    }
    
    navigatePrev() {
        const newIndex = this.currentIndex > 0 ? this.currentIndex - 1 : this.mediaItems.length - 1;
        this.setActiveItem(newIndex);
        this.scrollToThumbnail(newIndex);
    }
    
    navigateNext() {
        const newIndex = this.currentIndex < this.mediaItems.length - 1 ? this.currentIndex + 1 : 0;
        this.setActiveItem(newIndex);
        this.scrollToThumbnail(newIndex);
    }
    
    scrollToThumbnail(index) {
        const thumbnail = this.mediaItems[index]?.element;
        if (thumbnail && this.thumbnailsTrack) {
            thumbnail.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest',
                inline: 'center'
            });
        }
    }
    
    updateCounter() {
        if (this.mediaCounter && this.totalMedia) {
            this.mediaCounter.textContent = this.currentIndex + 1;
            this.totalMedia.textContent = this.mediaItems.length;
        }
    }
    
    updateNavigationButtons() {
        if (this.prevBtn) {
            this.prevBtn.disabled = this.mediaItems.length <= 1;
        }
        if (this.nextBtn) {
            this.nextBtn.disabled = this.mediaItems.length <= 1;
        }
    }
    
    updateUI() {
        this.updateCounter();
        this.updateNavigationButtons();
    }
    
    // FUNCIONALIDAD DEL MODAL PROFESIONAL
    
    openModal() {
        const modal = document.getElementById('mediaModal');
        if (!modal) {
            console.error('Modal no encontrado');
            return;
        }
        
        // Configurar el modal con los datos actuales
        this.setupModal();
        
        // Mostrar el modal usando Bootstrap
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        // Event listener para cuando se cierre el modal
        modal.addEventListener('hidden.bs.modal', () => {
            this.cleanupModal();
        }, { once: true });
    }
    
    setupModal() {
        const modalMainMedia = document.getElementById('modalMainMedia');
        const modalThumbnailsTrack = document.getElementById('modalThumbnailsTrack');
        const modalCounter = document.getElementById('modalCounter');
        const modalTotal = document.getElementById('modalTotal');
        const modalTitle = document.getElementById('modalTitle');
        const modalPrev = document.getElementById('modalPrev');
        const modalNext = document.getElementById('modalNext');
        
        if (!modalMainMedia || !modalThumbnailsTrack) {
            console.error('Elementos del modal no encontrados');
            return;
        }
        
        // Limpiar contenido previo
        modalMainMedia.innerHTML = '';
        modalThumbnailsTrack.innerHTML = '';
        
        // Configurar thumbnails del modal
        this.mediaItems.forEach((item, index) => {
            const thumbnail = document.createElement('div');
            thumbnail.className = 'modal-thumbnail';
            thumbnail.dataset.type = item.type;
            thumbnail.dataset.index = index;
            
            if (index === this.currentIndex) {
                thumbnail.classList.add('active');
            }
            
            if (item.type === 'video') {
                thumbnail.innerHTML = `
                    <video muted preload="metadata">
                        <source src="${item.src}" type="video/mp4">
                    </video>
                `;
            } else {
                thumbnail.innerHTML = `<img src="${item.src}" alt="${item.alt}">`;
            }
            
            // Event listener para cambiar media
            thumbnail.addEventListener('click', () => {
                this.setModalMedia(index);
            });
            
            modalThumbnailsTrack.appendChild(thumbnail);
        });
        
        // Configurar media principal inicial
        this.modalCurrentIndex = this.currentIndex;
        this.setModalMedia(this.currentIndex);
        
        // Configurar contadores
        modalCounter.textContent = this.currentIndex + 1;
        modalTotal.textContent = this.mediaItems.length;
        modalTitle.textContent = this.mediaItems[this.currentIndex]?.alt || 'Imagen del producto';
        
        // Event listeners para navegación
        if (modalPrev) {
            modalPrev.onclick = () => this.modalNavigatePrev();
        }
        if (modalNext) {
            modalNext.onclick = () => this.modalNavigateNext();
        }
        
        // Actualizar botones de navegación
        this.updateModalNavigation();
        
        // Event listener para teclado
        document.addEventListener('keydown', this.modalKeyHandler);
    }
    
    setModalMedia(index) {
        if (index < 0 || index >= this.mediaItems.length) return;
        
        const modalMainMedia = document.getElementById('modalMainMedia');
        const modalCounter = document.getElementById('modalCounter');
        const modalTitle = document.getElementById('modalTitle');
        const modalThumbnails = document.querySelectorAll('.modal-thumbnail');
        
        if (!modalMainMedia) return;
        
        const mediaItem = this.mediaItems[index];
        
        // Limpiar contenido anterior
        modalMainMedia.innerHTML = '';
        
        // Crear nuevo elemento de media
        if (mediaItem.type === 'video') {
            const video = document.createElement('video');
            video.controls = true;
            video.preload = 'metadata';
            video.muted = false;
            video.playsinline = true;
            
            const source = document.createElement('source');
            source.src = mediaItem.src;
            source.type = 'video/mp4';
            video.appendChild(source);
            
            video.innerHTML += 'Tu navegador no soporta el elemento video.';
            modalMainMedia.appendChild(video);
        } else {
            const img = document.createElement('img');
            img.src = mediaItem.src;
            img.alt = mediaItem.alt;
            modalMainMedia.appendChild(img);
        }
        
        // Actualizar thumbnails activos
        modalThumbnails.forEach((thumb, i) => {
            thumb.classList.toggle('active', i === index);
        });
        
        // Actualizar contador y título
        modalCounter.textContent = index + 1;
        modalTitle.textContent = mediaItem.alt || 'Imagen del producto';
        
        // Actualizar índice actual del modal
        this.modalCurrentIndex = index;
        
        // Actualizar navegación
        this.updateModalNavigation();
        
        // Scroll al thumbnail activo
        const activeThumb = modalThumbnails[index];
        if (activeThumb) {
            activeThumb.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest',
                inline: 'center'
            });
        }
    }
    
    modalNavigatePrev() {
        const newIndex = this.modalCurrentIndex > 0 ? this.modalCurrentIndex - 1 : this.mediaItems.length - 1;
        this.setModalMedia(newIndex);
    }
    
    modalNavigateNext() {
        const newIndex = this.modalCurrentIndex < this.mediaItems.length - 1 ? this.modalCurrentIndex + 1 : 0;
        this.setModalMedia(newIndex);
    }
    
    updateModalNavigation() {
        const modalPrev = document.getElementById('modalPrev');
        const modalNext = document.getElementById('modalNext');
        
        if (modalPrev) {
            modalPrev.disabled = this.mediaItems.length <= 1;
        }
        if (modalNext) {
            modalNext.disabled = this.mediaItems.length <= 1;
        }
    }
    
    modalKeyHandler = (e) => {
        const modal = document.getElementById('mediaModal');
        if (!modal || !modal.classList.contains('show')) return;
        
        switch(e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                this.modalNavigatePrev();
                break;
            case 'ArrowRight':
                e.preventDefault();
                this.modalNavigateNext();
                break;
            case 'Escape':
                e.preventDefault();
                bootstrap.Modal.getInstance(modal)?.hide();
                break;
        }
    }
    
    cleanupModal() {
        // Remover event listener del teclado
        document.removeEventListener('keydown', this.modalKeyHandler);
        
        // Resetear índice del modal
        this.modalCurrentIndex = this.currentIndex;
    }
}

// Inicializar galería cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const gallery = new ProductGallery();
    console.log('Galería profesional de productos inicializada');
});

// Función legacy para compatibilidad
function changeMainImage(src) {
    const mainMedia = document.getElementById('mainMedia');
    if (mainMedia && mainMedia.tagName === 'IMG') {
        mainMedia.src = src;
    }
}