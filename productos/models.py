from django.db import models
from django.utils.text import slugify
import uuid
from datetime import datetime

class Proveedor(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField(upload_to='proveedores/', blank=True, null=True, verbose_name="Logo")
    id_unico = models.CharField(max_length=50, unique=True, verbose_name="ID Único", help_text="Identificador único del proveedor", default="temp_id")
    catalogo = models.FileField(upload_to='catalogos/', blank=True, null=True, verbose_name="Catálogo (PDF)")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    @property
    def productos_asociados(self):
        """Retorna todos los productos asociados a este proveedor"""
        return self.product_set.filter(is_active=True)
    
    def count_productos(self):
        """Cuenta los productos activos del proveedor"""
        return self.productos_asociados.count()
    count_productos.short_description = "Productos Activos"
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

class Category(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    @property
    def subcategorias_asociadas(self):
        """Retorna todas las subcategorías asociadas a esta categoría"""
        return self.subcategories.all()
    
    def count_subcategorias(self):
        """Cuenta las subcategorías de la categoría"""
        return self.subcategorias_asociadas.count()
    count_subcategorias.short_description = "Subcategorías"
    
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
    
    @property
    def productos_asociados(self):
        """Retorna todos los productos asociados a esta subcategoría"""
        return self.product_set.filter(is_active=True)
    
    def count_productos(self):
        """Cuenta los productos activos de la subcategoría"""
        return self.productos_asociados.count()
    count_productos.short_description = "Productos Activos"
    
    class Meta:
        verbose_name = "Subcategoría"
        verbose_name_plural = "Subcategorías"

class Estatus(models.Model):
    name = models.CharField(max_length=120, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Descripción")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    @property
    def productos_asociados(self):
        """Retorna todos los productos asociados a este estatus"""
        return self.product_set.filter(is_active=True)
    
    def count_productos(self):
        """Cuenta los productos activos del estatus"""
        return self.productos_asociados.count()
    count_productos.short_description = "Productos Activos"
    
    class Meta:
        verbose_name = "Estatus de Procedencia"
        verbose_name_plural = "Estatus de Procedencia"

class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name="Nombre")
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=50, verbose_name="Código SKU", blank=True, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Proveedor")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Categoría")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Subcategoría")
    short_description = models.CharField(max_length=500, blank=True, verbose_name="Descripción Corta")
    description = models.TextField(blank=True, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imagen")
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name="Video del Producto")
    ficha_tecnica = models.FileField(upload_to='fichas_tecnicas/', blank=True, null=True, verbose_name="Ficha Técnica (PDF)")
    origen = models.CharField(max_length=100, blank=True, verbose_name="País de Origen")
    peso = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    estatus = models.ForeignKey(Estatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Estatus de Procedencia")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    en_oferta = models.BooleanField(default=False, verbose_name="En Oferta")
    destacado = models.BooleanField(default=False, verbose_name="Producto Destacado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    def generate_sku(self):
        """Genera un SKU único para el producto"""
        if self.proveedor:
            # Usar las primeras 3 letras del proveedor
            proveedor_code = self.proveedor.name[:3].upper().replace(' ', '')
        else:
            proveedor_code = 'GEN'  # General si no hay proveedor
        
        if self.category:
            # Usar las primeras 2 letras de la categoría
            category_code = self.category.name[:2].upper().replace(' ', '')
        else:
            category_code = 'XX'  # Default si no hay categoría
        
        # Fecha actual en formato YYMMDD
        date_code = datetime.now().strftime('%y%m%d')
        
        # Número secuencial basado en la hora actual + últimos 4 dígitos del UUID
        time_code = datetime.now().strftime('%H%M')
        uuid_suffix = str(uuid.uuid4().hex)[-4:].upper()
        
        # Formato: PROV-CAT-YYMMDD-HHMM-UUID4
        base_sku = f"{proveedor_code}-{category_code}-{date_code}-{time_code}-{uuid_suffix}"
        
        # Verificar que el SKU sea único
        counter = 1
        sku = base_sku
        while Product.objects.filter(sku=sku).exclude(pk=self.pk).exists():
            sku = f"{base_sku}-{counter:02d}"
            counter += 1
        
        return sku

    def save(self, *args, **kwargs):
        # Generar slug si no existe
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Generar SKU automáticamente si no existe o está vacío
        if not self.sku:
            self.sku = self.generate_sku()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """URL absoluta del producto - Importante para SEO"""
        from django.urls import reverse
        return reverse('productos:product_detail', args=[self.slug])
    
    @property
    def is_featured(self):
        """Retorna True si el producto está destacado"""
        return self.destacado
    
    @property
    def is_on_sale(self):
        """Retorna True si el producto está en oferta"""
        return self.en_oferta
    
    def get_status_badges(self):
        """Retorna una lista de badges de estado para mostrar en templates"""
        badges = []
        if self.en_oferta:
            badges.append({'text': 'EN OFERTA', 'class': 'bg-danger'})
        if self.destacado:
            badges.append({'text': 'DESTACADO', 'class': 'bg-warning text-dark'})
        if not self.is_active:
            badges.append({'text': 'INACTIVO', 'class': 'bg-secondary'})
        return badges
    
    @classmethod
    def get_featured_products(cls):
        """Retorna productos destacados activos"""
        return cls.objects.filter(is_active=True, destacado=True)
    
    @classmethod
    def get_on_sale_products(cls):
        """Retorna productos en oferta activos"""
        return cls.objects.filter(is_active=True, en_oferta=True)
    
    @classmethod
    def get_featured_and_on_sale(cls):
        """Retorna productos que están destacados Y en oferta"""
        return cls.objects.filter(is_active=True, destacado=True, en_oferta=True)
    
    def get_main_image(self):
        """Retorna la imagen principal del producto o la primera imagen disponible"""
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image.image
        first_image = self.images.first()
        if first_image:
            return first_image.image
        return self.image  # Fallback a la imagen original del modelo
    
    def get_all_images(self):
        """Retorna todas las imágenes del producto ordenadas"""
        return self.images.all()
    
    def get_main_video(self):
        """Retorna el primer video del producto disponible"""
        first_video = self.videos.first()
        if first_video:
            return first_video.video
        return self.video  # Fallback al video original del modelo
    
    def get_all_videos(self):
        """Retorna todos los videos del producto ordenados"""
        return self.videos.all()
    
    def has_multiple_images(self):
        """Retorna True si el producto tiene múltiples imágenes"""
        return self.images.count() > 1
    
    def has_multiple_videos(self):
        """Retorna True si el producto tiene múltiples videos"""
        return self.videos.count() > 1
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-destacado', '-en_oferta', '-created_at']  # Destacados y ofertas primero
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'destacado']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['proveedor', 'is_active']),
        ]


class ProductImage(models.Model):
    """Modelo para múltiples imágenes por producto - Galería de imágenes"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Producto")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Imagen")
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Texto alternativo")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden de visualización")
    is_main = models.BooleanField(default=False, verbose_name="Imagen principal")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen de {self.product.name} - {self.order}"

    class Meta:
        ordering = ['order', '-is_main']
        verbose_name = "Imagen de Galería"
        verbose_name_plural = "Imágenes de Galería"

    def save(self, *args, **kwargs):
        # Si es imagen principal, desmarcar otras como principales
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)


class ProductVideo(models.Model):
    """Modelo para múltiples videos por producto - Galería de videos"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='videos', verbose_name="Producto")
    video = models.FileField(upload_to='products/videos/', verbose_name="Video")
    title = models.CharField(max_length=255, blank=True, verbose_name="Título del Video")
    description = models.TextField(blank=True, verbose_name="Descripción")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden de visualización")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video de {self.product.name} - {self.title or f'Video {self.order}'}"

    class Meta:
        ordering = ['order']
        verbose_name = "Video de Galería"
        verbose_name_plural = "Videos de Galería"
