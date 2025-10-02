# coimpres_cuba/views.py
from django.shortcuts import render
from productos.models import Product

def home_view(request):
    """Vista para la página de inicio"""
    lang = request.GET.get('lang', 'es')
    featured_products = Product.objects.filter(is_active=True)[:3]  # Get first 3 active products
    hero_image = "/static/img/hero-image.jpg"  # Default hero image path
    
    # Definiciones de texto en diferentes idiomas
    i18n = {
        'en': {
            'home': 'Home',
            'products': 'Products',
            'about': 'About Us',
            'contact': 'Contact',
            'rights': 'All Rights Reserved',
            'contact_info': 'Email: info@importadoraitaliana.com | Tel: +53 5555-5555',
            'hero_title': 'Authentic Italian Products',
            'hero_subtitle': 'We bring the best Italian quality directly to Cuba',
            'view_products': 'View Products',
            'about_us': 'About Us',
            'our_story': 'Our Story',
            'story_content': 'Founded in 2020, Importadora Italiana brings authentic Italian products to Cuban customers. With a passion for quality and tradition, we source the finest products directly from Italian manufacturers.',
            'our_mission': 'Our Mission',
            'mission_content': 'To provide access to high-quality Italian goods and foster cultural exchange between Italy and Cuba.',
            'our_values': 'Our Values',
            'value_quality': 'Premium Quality',
            'value_authenticity': 'Authenticity',
            'value_tradition': 'Italian Tradition',
            'value_customer': 'Customer Satisfaction',
            'featured_products': 'Featured Products',
            'featured_subtitle': 'Explore our selection of premium Italian products',
            'view_details': 'View Details',
            'all_products': 'View All Products',
            'contact_cta': 'Need More Information?',
            'contact_desc': 'Our team is ready to assist you with any questions about our products.',
            'contact_us': 'Contact Us',
        },
        'es': {
            'home': 'Inicio',
            'products': 'Productos',
            'about': 'Sobre Nosotros',
            'contact': 'Contacto',
            'rights': 'Todos los Derechos Reservados',
            'contact_info': 'Email: info@importadoraitaliana.com | Tel: +53 5555-5555',
            'hero_title': 'Productos Italianos Auténticos',
            'hero_subtitle': 'Traemos la mejor calidad italiana directamente a Cuba',
            'view_products': 'Ver Productos',
            'about_us': 'Sobre Nosotros',
            'our_story': 'Nuestra Historia',
            'story_content': 'Fundada en 2020, Importadora Italiana trae productos auténticos italianos a los clientes cubanos. Con pasión por la calidad y la tradición, obtenemos los mejores productos directamente de fabricantes italianos.',
            'our_mission': 'Nuestra Misión',
            'mission_content': 'Proporcionar acceso a productos italianos de alta calidad y fomentar el intercambio cultural entre Italia y Cuba.',
            'our_values': 'Nuestros Valores',
            'value_quality': 'Calidad Premium',
            'value_authenticity': 'Autenticidad',
            'value_tradition': 'Tradición Italiana',
            'value_customer': 'Satisfacción del Cliente',
            'featured_products': 'Productos Destacados',
            'featured_subtitle': 'Explora nuestra selección de productos italianos premium',
            'view_details': 'Ver Detalles',
            'all_products': 'Ver Todos los Productos',
            'contact_cta': '¿Necesitas Más Información?',
            'contact_desc': 'Nuestro equipo está listo para ayudarte con cualquier pregunta sobre nuestros productos.',
            'contact_us': 'Contáctanos',
        },
        'it': {
            'home': 'Home',
            'products': 'Prodotti',
            'about': 'Chi Siamo',
            'contact': 'Contatti',
            'rights': 'Tutti i Diritti Riservati',
            'contact_info': 'Email: info@importadoraitaliana.com | Tel: +53 5555-5555',
            'hero_title': 'Autentici Prodotti Italiani',
            'hero_subtitle': 'Portiamo la migliore qualità italiana direttamente a Cuba',
            'view_products': 'Visualizza Prodotti',
            'about_us': 'Chi Siamo',
            'our_story': 'La Nostra Storia',
            'story_content': 'Fondata nel 2020, Importadora Italiana porta autentici prodotti italiani ai clienti cubani. Con passione per la qualità e la tradizione, acquistiamo i migliori prodotti direttamente dai produttori italiani.',
            'our_mission': 'La Nostra Missione',
            'mission_content': 'Fornire accesso a prodotti italiani di alta qualità e promuovere lo scambio culturale tra Italia e Cuba.',
            'our_values': 'I Nostri Valori',
            'value_quality': 'Qualità Premium',
            'value_authenticity': 'Autenticità',
            'value_tradition': 'Tradizione Italiana',
            'value_customer': 'Soddisfazione del Cliente',
            'featured_products': 'Prodotti in Evidenza',
            'featured_subtitle': 'Esplora la nostra selezione di prodotti italiani premium',
            'view_details': 'Visualizza Dettagli',
            'all_products': 'Visualizza Tutti i Prodotti',
            'contact_cta': 'Hai Bisogno di Maggiori Informazioni?',
            'contact_desc': 'Il nostro team è pronto ad assisterti con qualsiasi domanda sui nostri prodotti.',
            'contact_us': 'Contattaci',
        }
    }
    
    # Usar el idioma seleccionado o español por defecto
    i18n_selected = i18n.get(lang, i18n['es'])
    
    # Preparar productos destacados
    context = {
        'lang': lang,
        'i18n': i18n_selected,
        'featured_products': featured_products,
        'hero_image': hero_image,
    }
    return render(request, 'coimpres_cuba/home.html', context)