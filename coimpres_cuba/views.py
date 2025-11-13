# coimpres_cuba/views.py
from django.shortcuts import render
from productos.models import Product
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages

def home_view(request):
    """Vista para la página de inicio"""
    lang = request.GET.get('lang', 'es')
    
    # Obtener productos para carrusel automático (hasta 12 productos)
    featured_products_query = Product.objects.filter(is_active=True, destacado=True).select_related('category', 'subcategory', 'proveedor', 'estatus')[:12]
    
    # Si no hay suficientes productos destacados, completar con productos activos
    if featured_products_query.count() < 12:
        additional_products = Product.objects.filter(is_active=True).exclude(id__in=featured_products_query).select_related('category', 'subcategory', 'proveedor', 'estatus')[:12-featured_products_query.count()]
        featured_products_list = list(featured_products_query) + list(additional_products)
    else:
        featured_products_list = list(featured_products_query)
    
    # Para carrusel automático no necesitamos chunks, enviamos todos los productos
    
    hero_image = "/static/img/hero-image.jpg"  # Default hero image path
    
    # Definiciones de texto en diferentes idiomas
    i18n = {
        'en': {
            'home': 'Home',
            'products': 'Products',
            'suppliers': 'Suppliers',
            'about': 'About Us',
            'contact': 'Contact',
            'exclusive_orders': 'Exclusive Orders',
            'rights': 'All Rights Reserved',
            'hero_title': 'Quality Italian Products in Cuba',
            'hero_subtitle': 'We bring the best Italian quality directly to Havana. Wide catalog of products from the best Italian brands.',
            'view_products': 'View Products',
            'contact_us': 'Contact Us',
            'about_us': 'About Us',
            'our_story': 'Our Story',
            'story_content': 'Founded in 2014, COIMPRE S.r.l. brings authentic Italian products to Cuban customers. With a passion for quality and tradition, we source the finest products directly from Italian manufacturers.',
            # Información oficial COIMPRE S.r.l.
            'company_tagline': 'COIMPRE S.r.l. - Made in Italy Products since 2014',
            'since_2014': 'Since 2014',
            'office_miramar': 'Miramar Office',
            'customs_warehouse': 'Customs Warehouse',
            'office_cuba': 'Cuba Office',
            'miramar_havana': 'Miramar, Havana',
            'our_mission': 'Our Mission',
            'mission_content': 'To provide access to high-quality Italian goods and foster cultural exchange between Italy and Cuba.',
            'our_values': 'Our Values',
            'value_quality': 'Premium Quality',
            'value_quality_desc': 'We select only the finest Italian products',
            'value_authenticity': 'Authenticity',
            'value_authenticity_desc': 'We guarantee the authenticity of all our products',
            'value_tradition': 'Italian Tradition',
            'value_tradition_desc': 'We respect Italian tradition and craftsmanship',
            'value_customer': 'Customer Satisfaction',
            'value_customer_desc': 'Your satisfaction is our priority',
            'featured_products': 'Featured Products',
            'featured_subtitle': 'Explore our selection of premium Italian products',
            'view_details': 'View Details',
            'all_products': 'View All Products',
            'contact_cta': 'Need More Information?',
            'contact_desc': 'Our team is ready to assist you with any questions about our products.',
            'contact_us': 'Contact Us',
            'footer_description': 'Italian company specialized in import and export of Made in Italy products for construction and food. Present in Cuba since 2023.',
            'quick_links': 'Quick Links',
            'made_with_love': 'Made with',
            'in_italy': 'in Italy',
        },
        'es': {
            'home': 'Inicio',
            'products': 'Productos',
            'suppliers': 'Proveedores',
            'about': 'Sobre Nosotros',
            'contact': 'Contacto',
            'exclusive_orders': 'Pedidos Exclusivos',
            'rights': 'Todos los Derechos Reservados',
            'hero_title': 'Productos Italianos de Calidad en Cuba',
            'hero_subtitle': 'Traemos la mejor calidad italiana directamente a La Habana. Amplio catálogo de productos de las mejores marcas italianas.',
            'view_products': 'Ver Productos',
            'contact_us': 'Contáctanos',
            'about_us': 'Sobre Nosotros',
            'our_story': 'Nuestra Historia',
            'story_content': 'Fundada en 2014, COIMPRE S.r.l. trae productos auténticos italianos a los clientes cubanos. Con pasión por la calidad y la tradición, obtenemos los mejores productos directamente de fabricantes italianos.',
            # Información oficial COIMPRE S.r.l.
            'company_tagline': 'COIMPRE S.r.l. - Productos Made in Italy desde 2014',
            'since_2014': 'Desde 2014',
            'office_miramar': 'Oficina en Miramar',
            'customs_warehouse': 'Depósito Aduanero',
            'office_cuba': 'Oficina Cuba',
            'miramar_havana': 'Miramar, La Habana',
            'our_mission': 'Nuestra Misión',
            'mission_content': 'Proporcionar acceso a productos italianos de alta calidad y fomentar el intercambio cultural entre Italia y Cuba.',
            'our_values': 'Nuestros Valores',
            'value_quality': 'Calidad Premium',
            'value_quality_desc': 'Seleccionamos solo los mejores productos italianos',
            'value_authenticity': 'Autenticidad',
            'value_authenticity_desc': 'Garantizamos la autenticidad de todos nuestros productos',
            'value_tradition': 'Tradición Italiana',
            'value_tradition_desc': 'Respetamos la tradición y artesanía italiana',
            'value_customer': 'Satisfacción del Cliente',
            'value_customer_desc': 'Tu satisfacción es nuestra prioridad',
            'featured_products': 'Productos Destacados',
            'featured_subtitle': 'Explora nuestra selección de productos italianos premium',
            'view_details': 'Ver Detalles',
            'all_products': 'Ver Todos los Productos',
            'contact_cta': '¿Necesitas Más Información?',
            'contact_desc': 'Nuestro equipo está listo para ayudarte con cualquier pregunta sobre nuestros productos.',
            'contact_us': 'Contáctanos',
            'footer_description': 'Empresa italiana especializada en importación y exportación de productos Made in Italy para construcción y alimentación. Presente en Cuba desde 2023.',
            'quick_links': 'Enlaces Rápidos',
            'made_with_love': 'Hecho con',
            'in_italy': 'en Italia',
        },
        'it': {
            'home': 'Home',
            'products': 'Prodotti',
            'suppliers': 'Fornitori',
            'about': 'Chi Siamo',
            'contact': 'Contatti',
            'exclusive_orders': 'Ordini Esclusivi',
            'rights': 'Tutti i Diritti Riservati',
            'hero_title': 'Prodotti Italiani di Qualità a Cuba',
            'hero_subtitle': 'Portiamo la migliore qualità italiana direttamente all\'Avana. Ampio catalogo di prodotti dei migliori marchi italiani.',
            'view_products': 'Visualizza Prodotti',
            'contact_us': 'Contattaci',
            'about_us': 'Chi Siamo',
            'our_story': 'La Nostra Storia',
            'story_content': 'Fondata nel 2014, COIMPRE S.r.l. porta autentici prodotti italiani ai clienti cubani. Con passione per la qualità e la tradizione, acquistiamo i migliori prodotti direttamente dai produttori italiani.',
            # Información oficial COIMPRE S.r.l.
            'company_tagline': 'COIMPRE S.r.l. - Prodotti Made in Italy dal 2014',
            'since_2014': 'Dal 2014',
            'office_miramar': 'Ufficio Miramar',
            'customs_warehouse': 'Deposito Doganale',
            'office_cuba': 'Ufficio Cuba',
            'miramar_havana': 'Miramar, L\'Avana',
            'our_mission': 'La Nostra Missione',
            'mission_content': 'Fornire accesso a prodotti italiani di alta qualità e promuovere lo scambio culturale tra Italia e Cuba.',
            'our_values': 'I Nostri Valori',
            'value_quality': 'Qualità Premium',
            'value_quality_desc': 'Selezioniamo solo i migliori prodotti italiani',
            'value_authenticity': 'Autenticità',
            'value_authenticity_desc': 'Garantiamo l’autenticità di tutti i nostri prodotti',
            'value_tradition': 'Tradizione Italiana',
            'value_tradition_desc': 'Rispettiamo la tradizione e l’artigianalità italiana',
            'value_customer': 'Soddisfazione del Cliente',
            'value_customer_desc': 'La tua soddisfazione è la nostra priorità',
            'featured_products': 'Prodotti in Evidenza',
            'featured_subtitle': 'Esplora la nostra selezione di prodotti italiani premium',
            'view_details': 'Visualizza Dettagli',
            'all_products': 'Visualizza Tutti i Prodotti',
            'contact_cta': 'Hai Bisogno di Maggiori Informazioni?',
            'contact_desc': 'Il nostro team è pronto ad assisterti con qualsiasi domanda sui nostri prodotti.',
            'contact_us': 'Contattaci',
            'footer_description': 'Azienda italiana specializzata nell\'importazione ed esportazione di prodotti Made in Italy per edilizia e alimentazione. Presente a Cuba dal 2023.',
            'quick_links': 'Collegamenti Rapidi',
            'made_with_love': 'Fatto con',
            'in_italy': 'in Italia',
        }
    }
    
    # Usar el idioma seleccionado o español por defecto
    i18n_selected = i18n.get(lang, i18n['es'])
    
    # Preparar productos destacados
    context = {
        'lang': lang,
        'i18n': i18n_selected,
        'featured_products': featured_products_list,
        'hero_image': hero_image,
    }
    return render(request, 'coimpres_cuba/home.html', context)

class ContactView(TemplateView):
    template_name = 'coimpres_cuba/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.request.GET.get('lang', 'es')
        
        # Traducciones para la página de contacto
        i18n = {
            'es': {
                'contact_us': 'Contáctanos',
                'exclusive_orders': 'Pedidos Exclusivos',
                'office_cuba': 'Oficina Cuba',
                'miramar_havana': 'Miramar, La Habana',
                'company_tagline': 'COIMPRE S.r.l. - Productos Made in Italy desde 2014',
            },
            'en': {
                'contact_us': 'Contact Us',
                'exclusive_orders': 'Exclusive Orders',
                'office_cuba': 'Cuba Office',
                'miramar_havana': 'Miramar, Havana',
                'company_tagline': 'COIMPRE S.r.l. - Made in Italy Products since 2014',
            },
            'it': {
                'contact_us': 'Contattaci',
                'exclusive_orders': 'Ordini Esclusivi',
                'office_cuba': 'Ufficio Cuba',
                'miramar_havana': 'Miramar, L\'Avana',
                'company_tagline': 'COIMPRE S.r.l. - Prodotti Made in Italy dal 2014',
            }
        }
        
        context['lang'] = lang
        context['i18n'] = i18n.get(lang, i18n['es'])
        return context

    def post(self, request, *args, **kwargs):
        # Aquí puedes implementar el envío de correo
        messages.success(request, 'Mensaje enviado correctamente')
        return self.get(request, *args, **kwargs)