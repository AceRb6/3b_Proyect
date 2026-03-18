from django.contrib import admin
from django.urls import path, include
from api import views as api_views   # vista del dashboard

urlpatterns = [
    # Dashboard como página principal
    path('', api_views.dashboard, name='home'),

    path('admin/', admin.site.urls),

    # API bajo el prefijo /api/
    path('api/', include('api.urls')),

    # Dashboard HTML expuesto directamente
    path('dashboard/', api_views.dashboard, name='dashboard'),

    # (Opcional) Si prefieres que el JSON también sea accesible sin /api/
    # path('dashboard/data/', api_views.dashboard_data, name='dashboard_data'),
]