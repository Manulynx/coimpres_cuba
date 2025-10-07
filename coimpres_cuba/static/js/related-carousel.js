// Lógica del carrusel de productos relacionados extraída desde product_detail.html
// Requiere estructura HTML con .related-carousel-track y botones .related-prev / .related-next
(function(){
  document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.related-carousel-track');
    if(!track) return;
    const prevButtons = document.querySelectorAll('.related-prev');
    const nextButtons = document.querySelectorAll('.related-next');
    const firstItem = track.querySelector('.related-item');
    const itemWidth = () => firstItem?.getBoundingClientRect().width || 260;
    const scrollAmount = () => itemWidth() * (window.innerWidth < 576 ? 1 : 2.5);

    function scroll(dir) {
      track.scrollBy({ left: dir * scrollAmount(), behavior: 'smooth'});
    }
    prevButtons.forEach(btn => btn.addEventListener('click', () => scroll(-1)));
    nextButtons.forEach(btn => btn.addEventListener('click', () => scroll(1)));

    // Drag / swipe desktop
    let isDown = false, startX, scrollLeft;
    track.addEventListener('mousedown', (e) => { isDown = true; track.classList.add('grabbing'); startX = e.pageX - track.offsetLeft; scrollLeft = track.scrollLeft; });
    track.addEventListener('mouseleave', () => { isDown = false; track.classList.remove('grabbing'); });
    track.addEventListener('mouseup', () => { isDown = false; track.classList.remove('grabbing'); });
    track.addEventListener('mousemove', (e) => { if(!isDown) return; e.preventDefault(); const x = e.pageX - track.offsetLeft; const walk = (x - startX) * 1.2; track.scrollLeft = scrollLeft - walk; });

    // Touch
    let touchStartX = 0, touchScrollLeft = 0;
    track.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; touchScrollLeft = track.scrollLeft; }, {passive:true});
    track.addEventListener('touchmove', (e) => { const dx = e.touches[0].clientX - touchStartX; track.scrollLeft = touchScrollLeft - dx; }, {passive:true});

    // ===== Autoplay (rotación automática) =====
    let autoplayDelay = 4000; // ms
    let autoplayTimer = null;
    let userPausedUntil = 0;

    function atEnd() {
        return track.scrollLeft + track.clientWidth >= track.scrollWidth - 5; // margen de tolerancia
    }

    function doAutoplayStep() {
        if(Date.now() < userPausedUntil) return; // respetar pausa
        if(atEnd()) {
            track.scrollTo({ left: 0, behavior: 'smooth' });
        } else {
            track.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
        }
    }

    function startAutoplay() {
        stopAutoplay();
        autoplayTimer = setInterval(doAutoplayStep, autoplayDelay);
    }
    function stopAutoplay() { if(autoplayTimer) { clearInterval(autoplayTimer); autoplayTimer = null; } }

    function pauseAfterUserAction(extra = 8000) { // pausa extendida
        userPausedUntil = Date.now() + extra;
        startAutoplay(); // reinicia para respetar nueva pausa
    }

    ['mouseenter','focusin','touchstart'].forEach(evt => { track.addEventListener(evt, () => { stopAutoplay(); }); });
    ['mouseleave','focusout','touchend'].forEach(evt => { track.addEventListener(evt, () => { pauseAfterUserAction(); }); });
    prevButtons.forEach(btn => btn.addEventListener('click', () => pauseAfterUserAction()));
    nextButtons.forEach(btn => btn.addEventListener('click', () => pauseAfterUserAction()));
    track.addEventListener('mousedown', () => pauseAfterUserAction());
    track.addEventListener('mouseup', () => pauseAfterUserAction());

    startAutoplay();
  });
})();
