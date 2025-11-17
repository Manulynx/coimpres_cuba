# coimpres_cuba/whitenoise_headers.py
# ARCHIVO DESACTIVADO - Causaba errores en PythonAnywhere
# Los headers de rendimiento se manejan ahora a través del PerformanceMiddleware

# NOTA: Este archivo causaba el error "TypeError: 'str' object is not callable"
# porque WhiteNoise no podía importar correctamente la función en producción.

"""
def add_headers(headers, path, url):
    # Función para agregar headers HTTP optimizados 
    # que simulan beneficios de HTTP/2 en HTTP/1.1
    
    # Headers de caché agresivo para assets estáticos
    if path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2')):
        headers['Cache-Control'] = 'public, max-age=31536000, immutable'  # 1 año
        headers['Expires'] = 'Thu, 31 Dec 2037 23:55:55 GMT'
    
    # Headers de compresión
    if path.endswith(('.css', '.js', '.html', '.json', '.xml')):
        headers['Vary'] = 'Accept-Encoding'
    
    # Headers de seguridad para todos los archivos
    headers['X-Content-Type-Options'] = 'nosniff'
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Headers específicos para recursos críticos
    if path.endswith('.css'):
        headers['Content-Type'] = 'text/css; charset=utf-8'
        headers['X-Resource-Priority'] = 'high'
    
    if path.endswith('.js'):
        headers['Content-Type'] = 'application/javascript; charset=utf-8'
        
    # Headers para imágenes
    if path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
        file_ext = path.split(".")[-1]
        if file_ext == 'jpg':
            file_ext = 'jpeg'
        headers['Content-Type'] = f'image/{file_ext}'
        headers['X-Resource-Priority'] = 'low'
    
    return headers
"""