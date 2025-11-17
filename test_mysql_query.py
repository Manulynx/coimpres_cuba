#!/usr/bin/env python
# test_mysql_query.py
# Script para probar la nueva consulta sin subconsultas problemáticas

import os
import sys
import django

# Configurar Django
sys.path.append('/home/Coimpre/coimpres_cuba')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coimpres_cuba.settings.production')
django.setup()

from productos.models import Product

def test_home_query():
    """Probar la consulta corregida de la vista home"""
    print("🧪 Probando consulta corregida...")
    
    # Consulta corregida (sin subconsultas con LIMIT)
    featured_products_query = Product.objects.filter(is_active=True, destacado=True).select_related('category', 'subcategory', 'proveedor', 'estatus')
    featured_products_list = list(featured_products_query[:28])
    
    print(f"✅ Productos destacados encontrados: {len(featured_products_list)}")
    
    if len(featured_products_list) < 28:
        featured_ids = [p.id for p in featured_products_list]
        needed_count = 28 - len(featured_products_list)
        
        additional_products = Product.objects.filter(
            is_active=True
        ).exclude(
            id__in=featured_ids
        ).select_related('category', 'subcategory', 'proveedor', 'estatus')[:needed_count]
        
        additional_list = list(additional_products)
        featured_products_list.extend(additional_list)
        
        print(f"✅ Productos adicionales agregados: {len(additional_list)}")
    
    print(f"✅ Total de productos: {len(featured_products_list)}")
    print("🎉 ¡Consulta ejecutada exitosamente sin errores de MySQL!")
    
    return featured_products_list

if __name__ == "__main__":
    try:
        products = test_home_query()
        print("✅ Test completado - Sin errores de subconsulta MySQL")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()