#!/usr/bin/env python
import os
import sys
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coimpres_cuba.settings')
django.setup()

from productos.models import Product

def fix_sku_duplicates():
    """Fix SKU duplicates before migration"""
    print("Checking existing products...")
    
    products = Product.objects.all()
    print(f"Total products: {products.count()}")
    
    # Check for products with empty or None SKU
    empty_sku_products = Product.objects.filter(sku__isnull=True) | Product.objects.filter(sku='')
    print(f"Products with empty SKU: {empty_sku_products.count()}")
    
    # Check for duplicate SKUs
    from django.db.models import Count
    duplicate_skus = Product.objects.values('sku').annotate(count=Count('sku')).filter(count__gt=1)
    print(f"Duplicate SKU groups: {duplicate_skus.count()}")
    
    # Show all current SKU values
    for product in products:
        print(f"ID: {product.id}, Name: {product.name[:30]}, SKU: '{product.sku}'")
    
    # Generate unique SKUs for all products
    print("\nGenerating unique SKUs for all products...")
    for product in products:
        old_sku = product.sku
        # Generate new SKU using the method we defined
        new_sku = product.generate_sku()
        product.sku = new_sku
        product.save()
        print(f"Updated product {product.id}: '{old_sku}' -> '{new_sku}'")
    
    print("SKU fix completed!")

if __name__ == "__main__":
    fix_sku_duplicates()