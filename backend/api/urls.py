from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'stores', views.StoreViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'weather', views.WeatherConditionViewSet)
router.register(r'seasons', views.SeasonViewSet)
router.register(r'inventory', views.InventoryFactViewSet)

urlpatterns = [
    # Router DRF (todos los endpoints de la API)
    path('', include(router.urls)),

    # Endpoint JSON que el front‑end consume
    path('dashboard/data/', views.dashboard_data, name='dashboard_data'),
]