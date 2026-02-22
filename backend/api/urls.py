from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StoreViewSet, CategoryViewSet, ProductViewSet,
    WeatherConditionViewSet, SeasonViewSet, InventoryFactViewSet
)

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'weather', WeatherConditionViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'inventory', InventoryFactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]