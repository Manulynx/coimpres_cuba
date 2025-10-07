# products/views.py
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Product, Category, Subcategory, Proveedor, Estatus

class ProductListView(ListView):
    model = Product
    template_name = 'productos/product_list.html'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('proveedor', 'category', 'subcategory', 'estatus')
        
        # Filtrar por categoría si está presente en la URL
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filtrar por subcategoría si está presente en la URL
        subcategory_slug = self.request.GET.get('subcategory')
        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)
        
        # Filtrar por proveedor si está presente en la URL
        proveedor_slug = self.request.GET.get('proveedor')
        if proveedor_slug:
            queryset = queryset.filter(proveedor__slug=proveedor_slug)
        
        # Filtrar por estatus si está presente en la URL
        estatus_slug = self.request.GET.get('estatus')
        if estatus_slug:
            queryset = queryset.filter(estatus__slug=estatus_slug)
        
        # Filtrar productos destacados
        destacado = self.request.GET.get('destacado')
        if destacado == 'true':
            queryset = queryset.filter(destacado=True)
        
        # Filtrar productos en oferta
        en_oferta = self.request.GET.get('en_oferta')
        if en_oferta == 'true':
            queryset = queryset.filter(en_oferta=True)
        
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
        
        # Añadir categorías al contexto
        context['categories'] = Category.objects.all()
        
        # Añadir proveedores al contexto
        context['proveedores'] = Proveedor.objects.all()
        
        # Añadir estatus al contexto
        context['estatus_list'] = Estatus.objects.all()
        
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

# Vistas de Administración
def admin_panel(request):
    """Vista principal del panel de administración"""
    context = {
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'proveedores': Proveedor.objects.all(),
        'estatus_list': Estatus.objects.all(),
    }
    return render(request, 'productos/admin.html', context)

def add_proveedor(request):
    """Vista para agregar un nuevo proveedor"""
    if request.method == 'POST':
        try:
            proveedor = Proveedor(
                name=request.POST.get('name'),
                id_unico=request.POST.get('id_unico'),
            )
            
            if request.FILES.get('logo'):
                proveedor.logo = request.FILES['logo']
            
            if request.FILES.get('catalogo'):
                proveedor.catalogo = request.FILES['catalogo']
            
            proveedor.save()
            messages.success(request, f'Proveedor "{proveedor.name}" agregado exitosamente.')
            
        except Exception as e:
            messages.error(request, f'Error al agregar el proveedor: {str(e)}')
    
    return redirect('productos:admin_panel')

def add_category(request):
    """Vista para agregar una nueva categoría"""
    if request.method == 'POST':
        try:
            category = Category(
                name=request.POST.get('name')
            )
            category.save()
            messages.success(request, f'Categoría "{category.name}" agregada exitosamente.')
            
        except Exception as e:
            messages.error(request, f'Error al agregar la categoría: {str(e)}')
    
    return redirect('productos:admin_panel')

def add_subcategory(request):
    """Vista para agregar una nueva subcategoría"""
    if request.method == 'POST':
        try:
            category_id = request.POST.get('category')
            category = Category.objects.get(id=category_id)
            
            subcategory = Subcategory(
                name=request.POST.get('name'),
                category=category
            )
            subcategory.save()
            messages.success(request, f'Subcategoría "{subcategory.name}" agregada exitosamente.')
            
        except Category.DoesNotExist:
            messages.error(request, 'La categoría seleccionada no existe.')
        except Exception as e:
            messages.error(request, f'Error al agregar la subcategoría: {str(e)}')
    
    return redirect('productos:admin_panel')

def add_estatus(request):
    """Vista para agregar un nuevo estatus"""
    if request.method == 'POST':
        try:
            estatus = Estatus(
                name=request.POST.get('name'),
                description=request.POST.get('description', '')
            )
            estatus.save()
            messages.success(request, f'Estatus "{estatus.name}" agregado exitosamente.')
            
        except Exception as e:
            messages.error(request, f'Error al agregar el estatus: {str(e)}')
    
    return redirect('productos:admin_panel')

def add_product(request):
    """Vista para agregar un nuevo producto"""
    if request.method == 'POST':
        try:
            # Crear el producto con los datos básicos
            product = Product(
                name=request.POST.get('name'),
                sku=request.POST.get('sku', ''),
                short_description=request.POST.get('short_description', ''),
                description=request.POST.get('description', ''),
                origen=request.POST.get('origen', ''),
                is_active=request.POST.get('is_active') == 'on'
            )
            
            # Agregar precio si se proporciona
            price = request.POST.get('price')
            if price:
                product.price = float(price)
            
            # Agregar peso si se proporciona
            peso = request.POST.get('peso')
            if peso:
                product.peso = float(peso)
            
            # Agregar relaciones
            proveedor_id = request.POST.get('proveedor')
            if proveedor_id:
                product.proveedor = Proveedor.objects.get(id=proveedor_id)
            
            category_id = request.POST.get('category')
            if category_id:
                product.category = Category.objects.get(id=category_id)
            
            subcategory_id = request.POST.get('subcategory')
            if subcategory_id:
                product.subcategory = Subcategory.objects.get(id=subcategory_id)
            
            estatus_id = request.POST.get('estatus')
            if estatus_id:
                product.estatus = Estatus.objects.get(id=estatus_id)
            
            # Agregar archivos
            if request.FILES.get('image'):
                product.image = request.FILES['image']
            
            if request.FILES.get('video'):
                product.video = request.FILES['video']
            
            if request.FILES.get('ficha_tecnica'):
                product.ficha_tecnica = request.FILES['ficha_tecnica']
            
            product.save()
            messages.success(request, f'Producto "{product.name}" agregado exitosamente.')
            
        except Exception as e:
            messages.error(request, f'Error al agregar el producto: {str(e)}')
    
    return redirect('productos:admin_panel')