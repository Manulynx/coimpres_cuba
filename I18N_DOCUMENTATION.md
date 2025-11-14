# Sistema de Internacionalización (i18n) - COIMPRE S.r.l.

## Resumen
Se ha implementado un sistema de traducciones centralizado usando **context processors** de Django que permite que todas las plantillas tengan acceso a las traducciones sin necesidad de duplicar código en cada vista.

## Arquitectura

### 1. Context Processor Global (`coimpres_cuba/context_processors.py`)
- Contiene todas las traducciones en español, inglés e italiano
- Se ejecuta automáticamente en cada request
- Proporciona las variables `lang` e `i18n` a todas las plantillas

### 2. Configuración en `settings.py`
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... otros context processors ...
                'coimpres_cuba.context_processors.i18n_context',  # ← Nuevo
            ],
        },
    },
]
```

### 3. Vistas Simplificadas (`views.py`)
- Ya no manejan traducciones individualmente
- Se enfocan solo en la lógica de negocio
- Las traducciones están disponibles automáticamente

## Uso en Plantillas

### Sintaxis
```html
{{ i18n.clave_traduccion|default:"Texto por defecto" }}
```

### Ejemplos Prácticos

#### Navegación
```html
<a href="/">{{ i18n.home|default:"Inicio" }}</a>
<a href="/productos/">{{ i18n.products|default:"Productos" }}</a>
<a href="/proveedores/">{{ i18n.suppliers|default:"Proveedores" }}</a>
<a href="/contact/">{{ i18n.exclusive_orders|default:"Pedidos Exclusivos" }}</a>
```

#### Información de la Empresa
```html
<h1>{{ i18n.company_tagline|default:"COIMPRE S.r.l. - Productos Made in Italy desde 2014" }}</h1>
<p>{{ i18n.office_miramar|default:"Oficina en Miramar" }}</p>
<p>{{ i18n.miramar_havana|default:"Miramar, La Habana" }}</p>
```

#### Footer
```html
<p>{{ i18n.footer_description|default:"Empresa italiana especializada en..." }}</p>
<p>&copy; 2025 COIMPRE S.r.l. {{ i18n.rights|default:"Todos los derechos reservados" }}</p>
```

## Cambio de Idioma

### URL con Parámetro
```
/?lang=es  → Español (por defecto)
/?lang=en  → Inglés  
/?lang=it  → Italiano
```

### Botones de Idioma (Ejemplo)
```html
<div class="language-selector">
    <a href="?lang=es" class="{% if lang == 'es' %}active{% endif %}">ES</a>
    <a href="?lang=en" class="{% if lang == 'en' %}active{% endif %}">EN</a>
    <a href="?lang=it" class="{% if lang == 'it' %}active{% endif %}">IT</a>
</div>
```

## Claves de Traducción Disponibles

### Navegación
- `home`, `products`, `suppliers`, `contact`, `exclusive_orders`

### Información COIMPRE S.r.l.
- `company_tagline`, `since_2014`, `office_miramar`, `customs_warehouse`
- `office_cuba`, `miramar_havana`

### Contenido General
- `hero_title`, `hero_subtitle`, `about_us`, `our_story`, `our_mission`
- `our_values`, `featured_products`, `view_products`, `contact_us`

### Footer
- `footer_description`, `quick_links`, `rights`, `made_with_love`, `in_italy`

### Valores de la Empresa
- `value_quality`, `value_authenticity`, `value_tradition`, `value_customer`
- Y sus descripciones correspondientes con sufijo `_desc`

## Ventajas de este Sistema

1. **Centralizado**: Todas las traducciones en un solo lugar
2. **Automático**: No hay que modificar vistas para agregar traducciones
3. **Escalable**: Fácil agregar nuevos idiomas o claves
4. **Eficiente**: Sin duplicación de código
5. **Mantenible**: Un solo archivo para mantener todas las traducciones

## Agregar Nuevas Traducciones

1. Editar `coimpres_cuba/context_processors.py`
2. Agregar la nueva clave en los tres idiomas (es, en, it)
3. Usar en plantillas con `{{ i18n.nueva_clave|default:"Texto por defecto" }}`

¡El sistema está listo para soportar completamente el sitio web de COIMPRE S.r.l. en tres idiomas!