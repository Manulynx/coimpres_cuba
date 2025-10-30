#!/usr/bin/env python3
import re

# Leer el archivo
with open('productos/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Funciones que necesitan el decorador (excluyendo las que ya lo tienen y las públicas)
admin_functions = [
    'delete_proveedor', 'manage_categories', 'edit_category', 'delete_category',
    'manage_subcategories', 'edit_subcategory', 'delete_subcategory',
    'manage_estatus', 'edit_estatus', 'delete_estatus', 'edit_product', 'delete_product',
    'add_product_image', 'add_product_video', 'delete_product_image', 'delete_product_video'
]

# Agregar decorador a cada función
for func_name in admin_functions:
    # Buscar la definición de la función
    pattern = f'def {func_name}\\(request'
    if re.search(pattern, content):
        # Reemplazar def function_name(request con @require_staff_login\ndef function_name(request
        content = re.sub(
            f'def {func_name}\\(request',
            f'@require_staff_login\ndef {func_name}(request',
            content
        )
        print(f'✅ Agregado decorador a {func_name}')
    else:
        print(f'❌ No se encontró {func_name}')

# Escribir el archivo actualizado
with open('productos/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('🎉 Decoradores agregados exitosamente!')