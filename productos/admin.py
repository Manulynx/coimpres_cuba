from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import TextInput, Textarea
from .models import Category, Product, Proveedor, Subcategory, Estatus

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_unico', 'display_logo', 'display_catalogo', 'count_productos')
    list_filter = ('created_at', 'updated_at') if hasattr(Proveedor, 'created_at') else ()
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'id_unico')
    readonly_fields = ('count_productos',)
    ordering = ('name',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'id_unico')
        }),
        ('Archivos', {
            'fields': ('logo', 'catalogo'),
            'description': 'Sube el logo del proveedor y su catálogo en PDF'
        }),
    )
    
    def display_logo(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;" />',
                obj.logo.url
            )
        return format_html('<span class="text-muted">Sin logo</span>')
    display_logo.short_description = "Logo"
    
    def display_catalogo(self, obj):
        if obj.catalogo:
            return format_html(
                '<a href="{}" target="_blank" class="btn btn-sm btn-outline-primary">📄 Ver Catálogo</a>',
                obj.catalogo.url
            )
        return format_html('<span class="text-muted">Sin catálogo</span>')
    display_catalogo.short_description = "Catálogo"
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            # Aquí puedes agregar lógica adicional para nuevos proveedores
            pass
        super().save_model(request, obj, form, change)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'count_subcategorias', 'created_at') if hasattr(Category, 'created_at') else ('name', 'slug', 'count_subcategorias')
    list_filter = ('created_at',) if hasattr(Category, 'created_at') else ()
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
    readonly_fields = ('count_subcategorias',)
    ordering = ('name',)
    
    fieldsets = (
        ('Información de la Categoría', {
            'fields': ('name', 'slug'),
            'description': 'Información básica de la categoría'
        }),
    )
    
    # Inline para mostrar subcategorías relacionadas
    class SubcategoryInline(admin.TabularInline):
        model = Subcategory
        extra = 1
        prepopulated_fields = {"slug": ("name",)}
        fields = ('name', 'slug')
    
    inlines = [SubcategoryInline]

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug', 'count_productos', 'created_at') if hasattr(Subcategory, 'created_at') else ('name', 'category', 'slug', 'count_productos')
    list_filter = ('category', 'created_at') if hasattr(Subcategory, 'created_at') else ('category',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'category__name')
    readonly_fields = ('count_productos',)
    ordering = ('category__name', 'name')
    
    fieldsets = (
        ('Información de la Subcategoría', {
            'fields': ('name', 'slug', 'category'),
            'description': 'Información básica de la subcategoría'
        }),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Estatus)
class EstatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'slug', 'count_productos', 'created_at') if hasattr(Estatus, 'created_at') else ('name', 'description_short', 'slug', 'count_productos')
    list_filter = ('created_at',) if hasattr(Estatus, 'created_at') else ()
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'description')
    readonly_fields = ('count_productos',)
    ordering = ('name',)
    
    fieldsets = (
        ('Información del Estatus', {
            'fields': ('name', 'slug', 'description'),
            'description': 'Información del estatus de procedencia'
        }),
    )
    
    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "Sin descripción"
    description_short.short_description = "Descripción"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'proveedor', 'category', 'subcategory', 'price', 'display_image', 'is_active', 'en_oferta', 'destacado', 'created_at')
    list_filter = ('is_active', 'en_oferta', 'destacado', 'category', 'subcategory', 'proveedor', 'estatus', 'created_at')
    search_fields = ('name', 'description', 'short_description', 'sku', 'proveedor__name', 'category__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 25
    ordering = ('-destacado', '-en_oferta', '-created_at')
    
    # Campos que se pueden editar directamente desde la lista
    list_editable = ('is_active', 'price', 'en_oferta', 'destacado')
    
    # Filtros en la barra lateral
    list_filter = (
        'is_active',
        'category',
        'subcategory', 
        'proveedor',
        'estatus',
        ('created_at', admin.DateFieldListFilter),
        ('updated_at', admin.DateFieldListFilter),
    )
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'sku', 'short_description'),
            'classes': ('wide',)
        }),
        ('Descripción Completa', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
        ('Clasificación', {
            'fields': ('proveedor', 'category', 'subcategory', 'estatus'),
            'classes': ('wide',)
        }),
        ('Detalles del Producto', {
            'fields': ('price', 'peso', 'origen'),
            'classes': ('wide',)
        }),
        ('Archivos Multimedia', {
            'fields': ('image', 'video', 'ficha_tecnica'),
            'description': 'Sube la imagen, video y ficha técnica del producto'
        }),
        ('Estado y Promociones', {
            'fields': ('is_active', 'en_oferta', 'destacado'),
            'classes': ('wide',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Personalizar el widget del campo descripción
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 80})},
        models.CharField: {'widget': TextInput(attrs={'size': '80'})},
    }
    
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;" />',
                obj.image.url
            )
        return format_html('<span class="text-muted">Sin imagen</span>')
    display_image.short_description = "Imagen"
    
    def display_price_formatted(self, obj):
        """Método alternativo para mostrar precio formateado cuando sea necesario"""
        if obj.price:
            return format_html('<span class="text-success fw-bold">${:,.2f}</span>', obj.price)
        return format_html('<span class="text-muted">Sin precio</span>')
    display_price_formatted.short_description = "Precio Formateado"
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Optimizar las consultas de claves foráneas
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.order_by('name')
        elif db_field.name == "subcategory":
            kwargs["queryset"] = Subcategory.objects.select_related('category').order_by('category__name', 'name')
        elif db_field.name == "proveedor":
            kwargs["queryset"] = Proveedor.objects.order_by('name')
        elif db_field.name == "estatus":
            kwargs["queryset"] = Estatus.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            # Aquí puedes agregar lógica adicional para nuevos productos
            pass
        super().save_model(request, obj, form, change)
    
    # Acciones personalizadas
    actions = ['make_active', 'make_inactive', 'duplicate_product', 'mark_featured', 'unmark_featured', 'mark_on_sale', 'unmark_on_sale']
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} productos fueron activados.')
    make_active.short_description = "Activar productos seleccionados"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} productos fueron desactivados.')
    make_inactive.short_description = "Desactivar productos seleccionados"
    
    def mark_featured(self, request, queryset):
        updated = queryset.update(destacado=True)
        self.message_user(request, f'{updated} productos fueron marcados como destacados.')
    mark_featured.short_description = "Marcar como destacados"
    
    def unmark_featured(self, request, queryset):
        updated = queryset.update(destacado=False)
        self.message_user(request, f'{updated} productos fueron desmarcados como destacados.')
    unmark_featured.short_description = "Desmarcar como destacados"
    
    def mark_on_sale(self, request, queryset):
        updated = queryset.update(en_oferta=True)
        self.message_user(request, f'{updated} productos fueron marcados en oferta.')
    mark_on_sale.short_description = "Marcar en oferta"
    
    def unmark_on_sale(self, request, queryset):
        updated = queryset.update(en_oferta=False)
        self.message_user(request, f'{updated} productos fueron desmarcados de oferta.')
    unmark_on_sale.short_description = "Desmarcar de oferta"
    
    def duplicate_product(self, request, queryset):
        for product in queryset:
            product.pk = None
            product.name = f"Copia de {product.name}"
            product.slug = f"copia-de-{product.slug}"
            product.sku = f"COPY-{product.sku}" if product.sku else ""
            product.save()
        self.message_user(request, f'{queryset.count()} productos fueron duplicados.')
    duplicate_product.short_description = "Duplicar productos seleccionados"

# Personalizar el sitio de administración
admin.site.site_header = "Administración de Coimpres Cuba"
admin.site.site_title = "Coimpres Admin"
admin.site.index_title = "Panel de Administración"
