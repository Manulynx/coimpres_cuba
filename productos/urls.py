# productos/urls.py
from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    
    # URLs de autenticación (secretas) - DEBEN IR ANTES que el slug genérico
    path('secret-admin-login/', views.secret_login_view, name='secret_login'),
    path('admin/logout/', views.admin_logout_view, name='admin_logout'),
    
    # URLs del panel de administración (protegidas)
    path('admin/', views.admin_panel, name='admin_panel'),
    
    # URLs para agregar entidades
    path('admin/add-proveedor/', views.add_proveedor, name='add_proveedor'),
    path('admin/add-category/', views.add_category, name='add_category'),
    path('admin/add-subcategory/', views.add_subcategory, name='add_subcategory'),
    path('admin/add-estatus/', views.add_estatus, name='add_estatus'),
    path('admin/add-product/', views.add_product, name='add_product'),
    
    # URLs para gestionar proveedores
    path('admin/proveedores/', views.manage_proveedores, name='manage_proveedores'),
    path('admin/proveedores/edit/<int:pk>/', views.edit_proveedor, name='edit_proveedor'),
    path('admin/proveedores/delete/<int:pk>/', views.delete_proveedor, name='delete_proveedor'),
    
    # URLs para gestionar categorías
    path('admin/categorias/', views.manage_categories, name='manage_categories'),
    path('admin/categorias/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('admin/categorias/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    # URLs para gestionar subcategorías
    path('admin/subcategorias/', views.manage_subcategories, name='manage_subcategories'),
    path('admin/subcategorias/edit/<int:pk>/', views.edit_subcategory, name='edit_subcategory'),
    path('admin/subcategorias/delete/<int:pk>/', views.delete_subcategory, name='delete_subcategory'),
    
    # URLs para gestionar estatus
    path('admin/estatus/', views.manage_estatus, name='manage_estatus'),
    path('admin/estatus/edit/<int:pk>/', views.edit_estatus, name='edit_estatus'),
    path('admin/estatus/delete/<int:pk>/', views.delete_estatus, name='delete_estatus'),
    
    # URLs para gestionar productos
    path('admin/productos/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('admin/productos/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('admin/productos/toggle-status/<int:pk>/', views.toggle_product_status, name='toggle_product_status'),
    
    # URLs para gestionar imágenes de productos
    path('admin/producto-imagen/add/<int:product_pk>/', views.add_product_image, name='add_product_image'),
    path('admin/producto-imagen/edit/<int:pk>/', views.edit_product_image, name='edit_product_image'),
    path('admin/producto-imagen/delete/<int:pk>/', views.delete_product_image, name='delete_product_image'),
    
    # URLs para gestionar videos de productos
    path('admin/producto-video/add/<int:product_pk>/', views.add_product_video, name='add_product_video'),
    path('admin/producto-video/edit/<int:pk>/', views.edit_product_video, name='edit_product_video'),
    path('admin/producto-video/delete/<int:pk>/', views.delete_product_video, name='delete_product_video'),
    
    # URL genérica para productos - DEBE IR AL FINAL
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]