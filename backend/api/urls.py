from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .auth_views import login_view, me_view, logout_view

router = DefaultRouter()
router.register(r'stores', views.StoreViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'weather', views.WeatherConditionViewSet)
router.register(r'seasons', views.SeasonViewSet)
router.register(r'inventory', views.InventoryFactViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/data/', views.dashboard_data, name='dashboard_data'),

    path('auth/login/', login_view, name='auth-login'),
    path('auth/me/', me_view, name='auth-me'),
    path('auth/logout/', logout_view, name='auth-logout'),
]