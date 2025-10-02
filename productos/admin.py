from django.contrib import admin

# products/admin.py
from django.contrib import admin
from .models import Category, Product, Proveedor

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','proveedor','is_active','created_at')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name','brand__name')
