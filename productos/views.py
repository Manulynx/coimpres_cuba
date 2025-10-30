# products/views.py
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.http import Http404
from .models import Product, Category, Subcategory, Proveedor, Estatus, ProductImage, ProductVideo

# =================== FUNCIONES DE AUTENTICACIÓN Y SEGURIDAD ===================

def is_staff_user(user):
    """Función para verificar si el usuario es staff o superuser"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def require_staff_login(view_func):
    """Decorador personalizado para requerir login de staff"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('productos:secret_login')
        
        if not is_staff_user(request.user):
            messages.error(request, 'No tienes permisos para acceder a esta página.')
            raise Http404("Página no encontrada")
        
        return view_func(request, *args, **kwargs)
    return wrapper

# =================== VISTAS PÚBLICAS ===================

class ProductListView(ListView):
    model = Product
    template_name = 'productos/product_list.html'
    paginate_by = 10
    
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
    queryset = Product.objects.filter(is_active=True).select_related('proveedor', 'category', 'subcategory', 'estatus').prefetch_related('images', 'videos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el producto actual
        product = self.get_object()
        
        # Galería de imágenes
        gallery_images = product.get_all_images()
        context['gallery_images'] = gallery_images
        
        # Imagen principal: priorizar imagen principal del producto, luego imagen marcada como main
        if product.image:
            context['main_image'] = product.image
        else:
            main_image_obj = gallery_images.filter(is_main=True).first()
            if main_image_obj:
                context['main_image'] = main_image_obj.image
            elif gallery_images.exists():
                context['main_image'] = gallery_images.first().image
            else:
                context['main_image'] = None
        
        context['has_multiple_images'] = gallery_images.count() > 0 or bool(product.image)
        
        # Galería de videos
        gallery_videos = product.get_all_videos()
        context['gallery_videos'] = gallery_videos
        context['has_multiple_videos'] = gallery_videos.count() > 0
        
        # Obtener productos relacionados (de la misma categoría)
        if product.category:
            related_products = Product.objects.filter(
                category=product.category,
                is_active=True
            ).exclude(pk=product.pk)[:3]  # Limitar a 3 productos relacionados
            context['related_products'] = related_products
            
        return context

# =================== VISTAS DE ADMINISTRACIÓN (PROTEGIDAS) ===================

@require_staff_login
def admin_panel(request):
    """Vista principal del panel de administración - Lista de Productos"""
    from django.core.paginator import Paginator
    
    products = Product.objects.all().select_related('proveedor', 'category', 'subcategory', 'estatus').order_by('-created_at')
    
    # Filtros opcionales
    search = request.GET.get('search', '')
    if search:
        from django.db.models import Q
        products = products.filter(
            Q(name__icontains=search) | 
            Q(sku__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Paginación
    paginator = Paginator(products, 10)  # 10 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'paginator': paginator,
        'search': search,
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'proveedores': Proveedor.objects.all(),
        'estatus_list': Estatus.objects.all(),
    }
    return render(request, 'productos/admin.html', context)

@require_staff_login
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

@require_staff_login
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

@require_staff_login
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

@require_staff_login
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

@require_staff_login
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
            
            if request.FILES.get('ficha_tecnica'):
                product.ficha_tecnica = request.FILES['ficha_tecnica']
            
            product.save()
            
            # Procesar galería de imágenes múltiples
            gallery_images = request.FILES.getlist('gallery_images[]')
            gallery_alt_texts = request.POST.getlist('gallery_alt_texts[]')
            gallery_orders = request.POST.getlist('gallery_orders[]')
            gallery_is_main = request.POST.getlist('gallery_is_main[]')
            
            for i, image in enumerate(gallery_images):
                if image:
                    ProductImage.objects.create(
                        product=product,
                        image=image,
                        alt_text=gallery_alt_texts[i] if i < len(gallery_alt_texts) else '',
                        order=int(gallery_orders[i]) if i < len(gallery_orders) and gallery_orders[i] else i + 1,
                        is_main=str(i + 1) in gallery_is_main
                    )
            
            # Procesar galería de videos múltiples
            gallery_videos = request.FILES.getlist('gallery_videos[]')
            video_titles = request.POST.getlist('video_titles[]')
            video_descriptions = request.POST.getlist('video_descriptions[]')
            video_orders = request.POST.getlist('video_orders[]')
            
            for i, video in enumerate(gallery_videos):
                if video:
                    ProductVideo.objects.create(
                        product=product,
                        video=video,
                        title=video_titles[i] if i < len(video_titles) else '',
                        description=video_descriptions[i] if i < len(video_descriptions) else '',
                        order=int(video_orders[i]) if i < len(video_orders) and video_orders[i] else i + 1
                    )
            
            messages.success(request, f'Producto "{product.name}" agregado exitosamente con {len(gallery_images)} imágenes y {len(gallery_videos)} videos.')
            
        except Exception as e:
            messages.error(request, f'Error al agregar el producto: {str(e)}')
    
    return redirect('productos:admin_panel')

# Vistas de gestión de Proveedores
@require_staff_login
def manage_proveedores(request):
    """Vista para gestionar proveedores"""
    proveedores = Proveedor.objects.all().order_by('name')
    context = {
        'proveedores': proveedores,
        'active_tab': 'proveedores'
    }
    return render(request, 'productos/manage_proveedores.html', context)

@require_staff_login
def edit_proveedor(request, pk):
    """Vista para editar un proveedor"""
    from django.shortcuts import get_object_or_404
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        try:
            proveedor.name = request.POST.get('name')
            proveedor.id_unico = request.POST.get('id_unico')
            
            if request.FILES.get('logo'):
                proveedor.logo = request.FILES['logo']
            
            if request.FILES.get('catalogo'):
                proveedor.catalogo = request.FILES['catalogo']
            
            proveedor.save()
            messages.success(request, f'Proveedor "{proveedor.name}" actualizado exitosamente.')
            return redirect('productos:manage_proveedores')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el proveedor: {str(e)}')
    
    context = {
        'proveedor': proveedor,
        'active_tab': 'proveedores'
    }
    return render(request, 'productos/edit_proveedor.html', context)

@require_staff_login
def delete_proveedor(request, pk):
    """Vista para eliminar un proveedor"""
    from django.shortcuts import get_object_or_404
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        try:
            name = proveedor.name
            proveedor.delete()
            messages.success(request, f'Proveedor "{name}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el proveedor: {str(e)}')
    
    return redirect('productos:manage_proveedores')

# Vistas de gestión de Categorías
@require_staff_login
def manage_categories(request):
    """Vista para gestionar categorías"""
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
        'active_tab': 'categorias'
    }
    return render(request, 'productos/manage_categories.html', context)

@require_staff_login
def edit_category(request, pk):
    """Vista para editar una categoría"""
    from django.shortcuts import get_object_or_404
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        try:
            category.name = request.POST.get('name')
            category.save()
            messages.success(request, f'Categoría "{category.name}" actualizada exitosamente.')
            return redirect('productos:manage_categories')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar la categoría: {str(e)}')
    
    context = {
        'category': category,
        'active_tab': 'categorias'
    }
    return render(request, 'productos/edit_category.html', context)

@require_staff_login
def delete_category(request, pk):
    """Vista para eliminar una categoría"""
    from django.shortcuts import get_object_or_404
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        try:
            name = category.name
            category.delete()
            messages.success(request, f'Categoría "{name}" eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar la categoría: {str(e)}')
    
    return redirect('productos:manage_categories')

# Vistas de gestión de Subcategorías
@require_staff_login
def manage_subcategories(request):
    """Vista para gestionar subcategorías"""
    subcategories = Subcategory.objects.all().select_related('category').order_by('category__name', 'name')
    categories = Category.objects.all()
    context = {
        'subcategories': subcategories,
        'categories': categories,
        'active_tab': 'subcategorias'
    }
    return render(request, 'productos/manage_subcategories.html', context)

@require_staff_login
def edit_subcategory(request, pk):
    """Vista para editar una subcategoría"""
    from django.shortcuts import get_object_or_404
    subcategory = get_object_or_404(Subcategory, pk=pk)
    
    if request.method == 'POST':
        try:
            subcategory.name = request.POST.get('name')
            category_id = request.POST.get('category')
            if category_id:
                subcategory.category = Category.objects.get(id=category_id)
            subcategory.save()
            messages.success(request, f'Subcategoría "{subcategory.name}" actualizada exitosamente.')
            return redirect('productos:manage_subcategories')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar la subcategoría: {str(e)}')
    
    context = {
        'subcategory': subcategory,
        'categories': Category.objects.all(),
        'active_tab': 'subcategorias'
    }
    return render(request, 'productos/edit_subcategory.html', context)

@require_staff_login
def delete_subcategory(request, pk):
    """Vista para eliminar una subcategoría"""
    from django.shortcuts import get_object_or_404
    subcategory = get_object_or_404(Subcategory, pk=pk)
    
    if request.method == 'POST':
        try:
            name = subcategory.name
            subcategory.delete()
            messages.success(request, f'Subcategoría "{name}" eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar la subcategoría: {str(e)}')
    
    return redirect('productos:manage_subcategories')

# Vistas de gestión de Estatus
@require_staff_login
def manage_estatus(request):
    """Vista para gestionar estatus"""
    estatus_list = Estatus.objects.all().order_by('name')
    context = {
        'estatus_list': estatus_list,
        'active_tab': 'estatus'
    }
    return render(request, 'productos/manage_estatus.html', context)

@require_staff_login
def edit_estatus(request, pk):
    """Vista para editar un estatus"""
    from django.shortcuts import get_object_or_404
    estatus = get_object_or_404(Estatus, pk=pk)
    
    if request.method == 'POST':
        try:
            estatus.name = request.POST.get('name')
            estatus.description = request.POST.get('description', '')
            estatus.save()
            messages.success(request, f'Estatus "{estatus.name}" actualizado exitosamente.')
            return redirect('productos:manage_estatus')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el estatus: {str(e)}')
    
    context = {
        'estatus': estatus,
        'active_tab': 'estatus'
    }
    return render(request, 'productos/edit_estatus.html', context)

@require_staff_login
def delete_estatus(request, pk):
    """Vista para eliminar un estatus"""
    from django.shortcuts import get_object_or_404
    estatus = get_object_or_404(Estatus, pk=pk)
    
    if request.method == 'POST':
        try:
            name = estatus.name
            estatus.delete()
            messages.success(request, f'Estatus "{name}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el estatus: {str(e)}')
    
    return redirect('productos:manage_estatus')

# Vistas de gestión de Productos
@require_staff_login
def edit_product(request, pk):
    """Vista para editar un producto"""
    from django.shortcuts import get_object_or_404
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        try:
            # Actualizar datos básicos
            product.name = request.POST.get('name')
            product.sku = request.POST.get('sku', '')
            product.short_description = request.POST.get('short_description', '')
            product.description = request.POST.get('description', '')
            product.origen = request.POST.get('origen', '')
            product.is_active = request.POST.get('is_active') == 'on'
            
            # Actualizar precio
            price = request.POST.get('price')
            if price:
                product.price = float(price)
            else:
                product.price = None
            
            # Actualizar peso
            peso = request.POST.get('peso')
            if peso:
                product.peso = float(peso)
            else:
                product.peso = None
            
            # Actualizar relaciones
            proveedor_id = request.POST.get('proveedor')
            product.proveedor = Proveedor.objects.get(id=proveedor_id) if proveedor_id else None
            
            category_id = request.POST.get('category')
            product.category = Category.objects.get(id=category_id) if category_id else None
            
            subcategory_id = request.POST.get('subcategory')
            product.subcategory = Subcategory.objects.get(id=subcategory_id) if subcategory_id else None
            
            estatus_id = request.POST.get('estatus')
            product.estatus = Estatus.objects.get(id=estatus_id) if estatus_id else None
            
            # Actualizar archivos solo si se proporcionan nuevos
            if request.FILES.get('image'):
                product.image = request.FILES['image']
            
            if request.FILES.get('ficha_tecnica'):
                product.ficha_tecnica = request.FILES['ficha_tecnica']
            
            product.save()
            messages.success(request, f'Producto "{product.name}" actualizado exitosamente.')
            return redirect('productos:admin_panel')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el producto: {str(e)}')
    
    context = {
        'product': product,
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'proveedores': Proveedor.objects.all(),
        'estatus_list': Estatus.objects.all(),
        'active_tab': 'productos'
    }
    return render(request, 'productos/edit_product.html', context)

@require_staff_login
def delete_product(request, pk):
    """Vista para eliminar un producto"""
    from django.shortcuts import get_object_or_404
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        try:
            name = product.name
            product.delete()
            messages.success(request, f'Producto "{name}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar el producto: {str(e)}')
    
    return redirect('productos:admin_panel')

# =================== VISTAS DE AUTENTICACIÓN ===================

def secret_login_view(request):
    """Vista de login secreto para staff/superusers"""
    # Si ya está autenticado y es staff, redirigir al admin
    if request.user.is_authenticated and is_staff_user(request.user):
        return redirect('productos:admin_panel')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if is_staff_user(user):
                    login(request, user)
                    messages.success(request, f'Bienvenido al panel de administración, {user.get_full_name() or user.username}')
                    
                    # Redirigir a la página solicitada o al admin por defecto
                    next_url = request.GET.get('next', 'productos:admin_panel')
                    return redirect(next_url)
                else:
                    messages.error(request, 'No tienes permisos para acceder al panel de administración.')
            else:
                messages.error(request, 'Credenciales incorrectas.')
        else:
            messages.error(request, 'Por favor, completa todos los campos.')
    
    return render(request, 'productos/secret_login.html')

def admin_logout_view(request):
    """Vista para cerrar sesión del admin"""
    if request.user.is_authenticated:
        user_name = request.user.get_full_name() or request.user.username
        logout(request)
        messages.success(request, f'Sesión cerrada correctamente. ¡Hasta luego, {user_name}!')
    
    return redirect('home')