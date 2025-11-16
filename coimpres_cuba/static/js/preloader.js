/* coimpres_cuba/static/js/preloader.js */
// Preloader para COIMPRE S.r.l.
class CoimprePreloader {
    constructor() {
        // Solo ejecutar si showPreloader es true (primera visita)
        if (!window.showPreloader) {
            return;
        }
        
        this.preloader = null;
        this.minDisplayTime = 2000; // Mínimo 2 segundos
        this.startTime = Date.now();
        this.init();
    }

    init() {
        // Crear el preloader solo si no existe
        if (!document.querySelector('.preloader')) {
            this.createPreloader();
        }
        
        // Ocultar el preloader cuando todo esté cargado
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.handlePageLoad();
            });
        } else {
            this.handlePageLoad();
        }
        
        // Fallback: ocultar después de 5 segundos máximo
        setTimeout(() => {
            this.hidePreloader();
        }, 5000);
    }

    createPreloader() {
        const preloaderHTML = `
            <div class="preloader" id="coimpresPreloader">
                <img src="/static/img/logo_3.png" alt="COIMPRE S.r.l." class="preloader-logo" />
                <div class="preloader-text">
                    COIMPRE S.r.l.<span class="loading-dots"></span>
                </div>
                <div class="preloader-spinner"></div>
                <div class="preloader-progress">
                    <div class="preloader-progress-bar"></div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('afterbegin', preloaderHTML);
        this.preloader = document.getElementById('coimpresPreloader');
        
        // Prevenir scroll del body mientras carga
        document.body.style.overflow = 'hidden';
    }

    handlePageLoad() {
        // Asegurar que el loader se muestre al menos el tiempo mínimo
        const elapsedTime = Date.now() - this.startTime;
        const remainingTime = Math.max(0, this.minDisplayTime - elapsedTime);
        
        setTimeout(() => {
            // Esperar a que las imágenes terminen de cargar
            if (document.images.length > 0) {
                this.waitForImages().then(() => {
                    this.hidePreloader();
                });
            } else {
                this.hidePreloader();
            }
        }, remainingTime);
    }

    waitForImages() {
        const images = Array.from(document.images);
        const imagePromises = images.map(img => {
            if (img.complete) {
                return Promise.resolve();
            }
            
            return new Promise((resolve) => {
                img.addEventListener('load', resolve);
                img.addEventListener('error', resolve); // Resolver incluso si hay error
                
                // Timeout por si una imagen no carga
                setTimeout(resolve, 3000);
            });
        });
        
        return Promise.all(imagePromises);
    }

    hidePreloader() {
        if (this.preloader) {
            this.preloader.classList.add('fade-out');
            
            // Remover del DOM después de la animación
            setTimeout(() => {
                if (this.preloader && this.preloader.parentNode) {
                    this.preloader.parentNode.removeChild(this.preloader);
                }
                // Restaurar scroll del body
                document.body.style.overflow = '';
                
                // Disparar evento personalizado cuando termine de cargar
                document.dispatchEvent(new CustomEvent('coimpresLoaded'));
            }, 800);
        }
    }
}

// Inicializar preloader solo si debe mostrarse
if (window.showPreloader) {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            new CoimprePreloader();
        });
    } else {
        new CoimprePreloader();
    }

    // También inicializar en el evento más temprano posible
    (() => {
        new CoimprePreloader();
    })();
}