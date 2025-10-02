from django.contrib import admin
from .models import Category, Product, Proveedor, Subcategory, StatusProcedencia

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(StatusProcedencia)
class StatusProcedenciaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'proveedor', 'category', 'subcategory', 'price', 'is_active', 'created_at')
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('is_active', 'category', 'subcategory', 'proveedor', 'status_procedencia')
    search_fields = ('name', 'description', 'short_description', 'sku')
    date_hierarchy = 'created_at'
