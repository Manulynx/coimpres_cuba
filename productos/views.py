# products/views.py
from django.views.generic import ListView, DetailView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'productos/product_list.html'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('proveedor', 'category', 'subcategory')
        
        # Filtrar por categoría si está presente en la URL
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filtrar por subcategoría si está presente en la URL
        subcategory_slug = self.request.GET.get('subcategory')
        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)
        
        # Búsqueda por término
        search_term = self.request.GET.get('q')
        if search_term:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(name__icontains=search_term) | 
                Q(description__icontains=search_term) | 
                Q(short_description__icontains=search_term) |
                Q(sku__icontains=search_term)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Category, Subcategory
        
        # Añadir categorías al contexto
        context['categories'] = Category.objects.all()
        
        # Obtener categoría seleccionada
        category_slug = self.request.GET.get('category')
        if category_slug:
            context['selected_category'] = Category.objects.filter(slug=category_slug).first()
            context['subcategories'] = Subcategory.objects.filter(category__slug=category_slug)
        
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'productos/product_detail.html'
    queryset = Product.objects.filter(is_active=True).select_related('proveedor')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener productos relacionados (de la misma categoría)
        product = self.get_object()
        if product.category:
            related_products = Product.objects.filter(
                category=product.category,
                is_active=True
            ).exclude(pk=product.pk)[:3]  # Limitar a 3 productos relacionados
            context['related_products'] = related_products
            
        return context