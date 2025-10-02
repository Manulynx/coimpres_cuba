import os
import django
import random
from decimal import Decimal

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coimpres_cuba.settings')
django.setup()

from productos.models import Category, Subcategory, StatusProcedencia, Product, Proveedor

def create_sample_data():
    # Limpiar datos existentes
    Product.objects.all().delete()
    Subcategory.objects.all().delete()
    Category.objects.all().delete()
    Proveedor.objects.all().delete()
    StatusProcedencia.objects.all().delete()
    
    # Crear proveedores
    proveedores = [
        {"name": "Barilla"},
        {"name": "Ferrari Formaggi"},
        {"name": "Lavazza"},
        {"name": "Ferrero"},
        {"name": "Mapei"},
    ]
    
    created_proveedores = []
    for proveedor_data in proveedores:
        proveedor = Proveedor.objects.create(
            name=proveedor_data["name"]
        )
        created_proveedores.append(proveedor)
    
    # Crear categorías
    categories = [
        {"name": "comida"},
        {"name": "construccion"},
    ]
    
    created_categories = []
    for category_data in categories:
        category = Category.objects.create(
            name=category_data["name"]
        )
        created_categories.append(category)
    
    # Crear subcategorías
    subcategories = [
        {"name": "Pasta", "category": created_categories[0]},  # Comida
        {"name": "Café", "category": created_categories[0]},   # Comida
        {"name": "Quesos", "category": created_categories[0]}, # Comida
        {"name": "Aceites", "category": created_categories[0]}, # Comida
        {"name": "Cementos", "category": created_categories[1]}, # Construcción
        {"name": "Adhesivos", "category": created_categories[1]}, # Construcción
        {"name": "Pinturas", "category": created_categories[1]}, # Construcción
    ]
    
    created_subcategories = []
    for subcategory_data in subcategories:
        subcategory = Subcategory.objects.create(
            name=subcategory_data["name"],
            category=subcategory_data["category"]
        )
        created_subcategories.append(subcategory)
    
    # Crear estados de procedencia
    status_procedencias = [
        {"name": "En stock", "description": "Producto disponible en almacén."},
        {"name": "Por pedido", "description": "Se pide directamente a Italia con un tiempo de entrega de 45 días."},
        {"name": "Próximamente", "description": "Próximamente disponible en stock."},
    ]
    
    created_status = []
    for status_data in status_procedencias:
        status = StatusProcedencia.objects.create(
            name=status_data["name"],
            description=status_data["description"]
        )
        created_status.append(status)
    
    # Crear productos
    products = [
        {
            "name": "Spaghetti Barilla n.5", 
            "proveedor": created_proveedores[0],
            "category": created_categories[0],  # Comida
            "subcategory": created_subcategories[0],  # Pasta
            "short_description": "Pasta de sémola de trigo duro, formato spaghetti.",
            "description": "Los Spaghetti Barilla n.5 son el formato clásico de pasta italiana, elaborados con trigo duro seleccionado y agua. Perfectos para acompañar con salsas tradicionales italianas.",
            "price": Decimal('4.50'),
            "origen": "Italia",
            "peso": Decimal('1.0'),
            "sku": "BAR-SPAG-5",
            "status_procedencia": created_status[0]  # En stock
        },
        {
            "name": "Café Lavazza Qualità Oro", 
            "proveedor": created_proveedores[2],
            "category": created_categories[0],  # Comida
            "subcategory": created_subcategories[1],  # Café
            "short_description": "Mezcla de cafés 100% arábica, tueste medio.",
            "description": "El café Qualità Oro es la mezcla más emblemática de Lavazza, creada en 1956. Se compone de seis variedades diferentes de café Arábica, procedentes de América Central y del Sur, que se combinan para crear un aroma suave y un sabor dulce y aterciopelado.",
            "price": Decimal('12.90'),
            "origen": "Italia",
            "peso": Decimal('0.25'),
            "sku": "LAV-QO-250",
            "status_procedencia": created_status[0]  # En stock
        },
        {
            "name": "Parmigiano Reggiano 24 meses", 
            "proveedor": created_proveedores[1],
            "category": created_categories[0],  # Comida
            "subcategory": created_subcategories[2],  # Quesos
            "short_description": "Queso Parmigiano Reggiano DOP envejecido 24 meses.",
            "description": "El Parmigiano Reggiano es un queso italiano con Denominación de Origen Protegida (DOP). Este queso ha sido envejecido durante 24 meses, desarrollando su característico sabor intenso y granulado con notas de frutos secos.",
            "price": Decimal('22.50'),
            "origen": "Italia",
            "peso": Decimal('0.50'),
            "sku": "FER-PARM-24",
            "status_procedencia": created_status[1]  # Por pedido
        },
        {
            "name": "Adhesivo Mapei Keraflex", 
            "proveedor": created_proveedores[4],
            "category": created_categories[1],  # Construcción
            "subcategory": created_subcategories[5],  # Adhesivos
            "short_description": "Adhesivo cementoso de altas prestaciones para baldosas cerámicas.",
            "description": "Keraflex es un adhesivo cementoso de altas prestaciones, con deslizamiento vertical nulo, de tiempo abierto prolongado, para baldosas cerámicas y material pétreo. Especialmente adecuado para la colocación de gres porcelánico y piedras naturales.",
            "price": Decimal('18.75'),
            "origen": "Italia",
            "peso": Decimal('25.0'),
            "sku": "MAP-KFX-25",
            "status_procedencia": created_status[2]  # Próximamente
        },
        {
            "name": "Nutella", 
            "proveedor": created_proveedores[3],
            "category": created_categories[0],  # Comida
            "subcategory": None,
            "short_description": "Crema de avellanas con cacao.",
            "description": "Nutella es una crema de avellanas con cacao creada por la empresa italiana Ferrero. Su receta incluye azúcar, aceite de palma, avellanas, leche desnatada en polvo, cacao desgrasado, lecitina de soja y vainillina.",
            "price": Decimal('8.90'),
            "origen": "Italia",
            "peso": Decimal('0.4'),
            "sku": "FER-NUT-400",
            "status_procedencia": created_status[0]  # En stock
        },
    ]
    
    for product_data in products:
        product = Product.objects.create(
            name=product_data["name"],
            proveedor=product_data["proveedor"],
            category=product_data["category"],
            subcategory=product_data["subcategory"],
            short_description=product_data["short_description"],
            description=product_data["description"],
            price=product_data["price"],
            origen=product_data["origen"],
            peso=product_data["peso"],
            sku=product_data["sku"],
            status_procedencia=product_data["status_procedencia"],
            is_active=True
        )
    
    print("¡Datos de ejemplo creados con éxito!")

if __name__ == "__main__":
    create_sample_data()