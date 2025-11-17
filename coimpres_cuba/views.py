# coimpres_cuba/views.py - VERSIÓN SIMPLIFICADA
from django.shortcuts import render
from productos.models import Product
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_GET

def home_view(request):
    """Vista para la página de inicio - Con más productos para collage ampliado"""
    # CORREGIDO: Obtener productos destacados sin LIMIT en subconsulta
    featured_products_query = Product.objects.filter(is_active=True, destacado=True).select_related('category', 'subcategory', 'proveedor', 'estatus')
    featured_products_list = list(featured_products_query[:28])  # Convertir a lista primero
    
    # Si no hay suficientes productos destacados, completar con productos activos
    if len(featured_products_list) < 28:
        # Obtener IDs de productos ya seleccionados para excluirlos
        featured_ids = [p.id for p in featured_products_list]
        needed_count = 28 - len(featured_products_list)
        
        # Consulta separada sin subconsulta problemática
        additional_products = Product.objects.filter(
            is_active=True
        ).exclude(
            id__in=featured_ids  # Usar lista de IDs en lugar de QuerySet
        ).select_related('category', 'subcategory', 'proveedor', 'estatus')[:needed_count]
        
        featured_products_list.extend(list(additional_products))
    
    hero_image = "/static/img/hero-image.jpg"  # Default hero image path
    
    # El contexto de traducciones (i18n y lang) ahora está disponible globalmente via context processor
    context = {
        'featured_products': featured_products_list,
        'hero_image': hero_image,
    }
    return render(request, 'coimpres_cuba/home.html', context)

class ContactView(TemplateView):
    """Vista para la página de contacto - Simplificada usando context processor global"""
    template_name = 'coimpres_cuba/contact.html'
    
    # Ya no necesitamos get_context_data porque las traducciones están disponibles globalmente
    
    def post(self, request, *args, **kwargs):
        # Aquí puedes implementar el envío de correo
        messages.success(request, 'Mensaje enviado correctamente')
        return self.get(request, *args, **kwargs)

def change_language(request):
    """Vista para cambiar idioma y redirigir a la página anterior"""
    from django.shortcuts import redirect
    from django.urls import reverse
    
    # Obtener el idioma solicitado
    lang = request.GET.get('lang', 'es')
    
    # Validar que sea un idioma válido
    if lang in ['es', 'en', 'it']:
        request.session['selected_language'] = lang
    
    # Obtener la URL de referencia (página anterior)
    referer = request.META.get('HTTP_REFERER')
    
    if referer:
        # Si hay referencia, redirigimos allí pero sin el parámetro lang en la URL
        # para que use el idioma de la sesión
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        parsed_url = urlparse(referer)
        query_params = parse_qs(parsed_url.query)
        
        # Remover el parámetro lang de la URL para evitar conflictos
        if 'lang' in query_params:
            del query_params['lang']
        
        # Reconstruir la URL sin el parámetro lang
        new_query = urlencode({k: v[0] if len(v) == 1 else v for k, v in query_params.items()}, doseq=True)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
        
        return redirect(new_url)
    else:
        # Si no hay referencia, ir al inicio
        return redirect('/')

@require_GET
def robots_txt(request):
    """Vista para robots.txt - Importante para SEO"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /productos/admin/",
        "Disallow: /productos/secret-admin-login/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")