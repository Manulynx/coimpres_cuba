// Main JavaScript file for the Italian Products website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any interactive elements
    initializeTooltips();
    setupScrollAnimations();

    // Add scroll event listener for the navigation bar
    window.addEventListener('scroll', function() {
        toggleStickyNav();
    });
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Toggle sticky navigation on scroll
function toggleStickyNav() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.classList.add('navbar-sticky', 'shadow-sm');
    } else {
        navbar.classList.remove('navbar-sticky', 'shadow-sm');
    }
}

// Animate elements on scroll
function setupScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animatedElements.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// Function to format WhatsApp message with product information
function formatWhatsAppMessage(productName) {
    // Get language from the html lang attribute
    const lang = document.documentElement.lang || 'es';
    
    let message = '';
    switch(lang) {
        case 'en':
            message = `Hello, I am interested in ${productName}. Can you provide more information?`;
            break;
        case 'it':
            message = `Ciao, sono interessato a ${productName}. Potete fornirmi maggiori informazioni?`;
            break;
        case 'es':
        default:
            message = `Hola, estoy interesado en ${productName}. ¿Pueden proporcionarme más información?`;
    }
    
    return encodeURIComponent(message);
}

// Create WhatsApp link with pre-filled message
function createWhatsAppLink(phoneNumber, productName) {
    const message = formatWhatsAppMessage(productName);
    return `https://wa.me/${phoneNumber}?text=${message}`;
}