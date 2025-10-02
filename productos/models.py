from django.db import models
from django.utils.text import slugify

class Proveedor(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='proveedores/', blank=True, null=True, verbose_name="Logo")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('construccion', 'Construcción'),
        ('comida', 'Comida'),
    ]
    name = models.CharField(max_length=120, choices=CATEGORY_CHOICES, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Subcategory(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories", verbose_name="Categoría")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.category})"
    
    class Meta:
        verbose_name = "Subcategoría"
        verbose_name_plural = "Subcategorías"

class StatusProcedencia(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Status de Procedencia"
        verbose_name_plural = "Status de Procedencia"

class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=50, verbose_name="Código SKU", blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Proveedor")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Categoría")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Subcategoría")
    short_description = models.CharField(max_length=500, blank=True, verbose_name="Descripción Corta")
    description = models.TextField(blank=True, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imagen")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL del Video")
    ficha_tecnica = models.FileField(upload_to='fichas_tecnicas/', blank=True, null=True, verbose_name="Ficha Técnica (PDF)")
    origen = models.CharField(max_length=100, blank=True, verbose_name="País de Origen")
    peso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    status_procedencia = models.ForeignKey(StatusProcedencia, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Status de Procedencia")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
