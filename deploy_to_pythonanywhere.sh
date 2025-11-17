#!/bin/bash
# deploy_to_pythonanywhere.sh
# Script de despliegue para PythonAnywhere

echo "🚀 Iniciando despliegue en PythonAnywhere..."

# Navegar al directorio del proyecto
cd /home/Coimpre/coimpres_cuba

echo "📥 Descargando cambios del repositorio..."
git pull origin main

echo "📦 Recolectando archivos estáticos..."
python3.13 manage.py collectstatic --noinput --settings=coimpres_cuba.settings.production

echo "🔄 Aplicando migraciones..."
python3.13 manage.py migrate --settings=coimpres_cuba.settings.production

echo "🧹 Limpiando archivos temporales..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo "🔄 Reiniciando aplicación web..."
touch /var/www/coimpre_pythonanywhere_com_wsgi.py

echo "✅ Despliegue completado exitosamente!"
echo "🌐 Sitio web: https://coimpre.pythonanywhere.com"

# Verificar que la aplicación esté funcionando
echo "🔍 Verificando estado de la aplicación..."
curl -s -o /dev/null -w "%{http_code}" https://coimpre.pythonanywhere.com | grep -q "200" && echo "✅ Aplicación funcionando correctamente" || echo "❌ Error en la aplicación - revisar logs"