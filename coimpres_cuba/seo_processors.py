# coimpres_cuba/seo_processors.py
from django.conf import settings

def seo_context(request):
    """Context processor para datos SEO básicos que complementan los templates"""
    
    # Datos SEO base que pueden ser usados en templates
    seo_data = {
    
        'seo_title': 'COIMPRE S.r.l. - Productos Made in Italy',
        'seo_description': 'Importador oficial de productos italianos de alta calidad en Cuba desde 2014. Productos Made in Italy para tu hogar y negocio.',
        'seo_keywords': 'productos italianos, made in Italy, COIMPRE, Cuba, La Habana, importación, calidad',
        'company_phone': '+53 72141480',
        'company_email': 'coimpresrl@gmail.com'
    }
    return seo_data