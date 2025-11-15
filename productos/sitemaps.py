# productos/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category, Subcategory, Proveedor
from datetime import datetime

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'contact', 'productos:product_list', 'productos:proveedor_list']

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return datetime.now()

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_active=True).select_related('category', 'proveedor')

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()

class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('productos:product_list') + f'?category={obj.slug}'

class ProveedorSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Proveedor.objects.filter(is_active=True)

    def location(self, obj):
        return reverse('productos:proveedor_list')