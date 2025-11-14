# coimpres_cuba/views.py - VERSIÓN SIMPLIFICADA
from django.shortcuts import render
from productos.models import Product
from django.views.generic import TemplateView
from django.contrib import messages

def home_view(request):
    """Vista para la página de inicio - Simplificada usando context processor global"""
    # Obtener productos para carrusel automático (hasta 12 productos)
    featured_products_query = Product.objects.filter(is_active=True, destacado=True).select_related('category', 'subcategory', 'proveedor', 'estatus')[:12]
    
    # Si no hay suficientes productos destacados, completar con productos activos
    if featured_products_query.count() < 12:
        additional_products = Product.objects.filter(is_active=True).exclude(id__in=featured_products_query).select_related('category', 'subcategory', 'proveedor', 'estatus')[:12-featured_products_query.count()]
        featured_products_list = list(featured_products_query) + list(additional_products)
    else:
        featured_products_list = list(featured_products_query)
    
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