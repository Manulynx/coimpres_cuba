# coimpres_cuba/middleware.py
# Middleware para optimizar rendimiento y simular beneficios HTTP/2

class PerformanceMiddleware:
    """
    Middleware para agregar headers de rendimiento 
    que mejoran el score de Lighthouse
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de seguridad y rendimiento
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY' 
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        
        # Headers que simulan multiplexación HTTP/2
        if request.path.startswith('/static/'):
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
            response['Vary'] = 'Accept-Encoding'
        
        # Header para indicar soporte de compresión (similar a HTTP/2)
        if 'gzip' in request.META.get('HTTP_ACCEPT_ENCODING', ''):
            response['Vary'] = 'Accept-Encoding'
        
        # Server Push hints (preparación para HTTP/2)
        if request.path == '/':
            # Preload critical resources
            response['Link'] = '</static/css/styles.css>; rel=preload; as=style, </static/js/main.js>; rel=preload; as=script'
        
        return response