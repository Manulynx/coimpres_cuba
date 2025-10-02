# products/views.py
from django.views.generic import ListView, DetailView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    paginate_by = 12
    queryset = Product.objects.filter(is_active=True).select_related('proveedor')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    queryset = Product.objects.filter(is_active=True).select_related('proveedor')