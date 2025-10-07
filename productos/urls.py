# productos/urls.py
from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('admin/', views.admin_panel, name='admin_panel'),
    path('admin/add-proveedor/', views.add_proveedor, name='add_proveedor'),
    path('admin/add-category/', views.add_category, name='add_category'),
    path('admin/add-subcategory/', views.add_subcategory, name='add_subcategory'),
    path('admin/add-estatus/', views.add_estatus, name='add_estatus'),
    path('admin/add-product/', views.add_product, name='add_product'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]