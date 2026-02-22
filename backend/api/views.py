from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Store, Category, Product, WeatherCondition, Season, InventoryFact
from .serializers import (
    StoreSerializer, CategorySerializer, ProductSerializer,
    WeatherConditionSerializer, SeasonSerializer, InventoryFactSerializer
)

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['product_id', 'product_name']
    filterset_fields = ['category']

class WeatherConditionViewSet(viewsets.ModelViewSet):
    queryset = WeatherCondition.objects.all()
    serializer_class = WeatherConditionSerializer

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

class InventoryFactViewSet(viewsets.ModelViewSet):
    queryset = InventoryFact.objects.all().select_related(
        'store', 'product', 'product__category', 'weather', 'season'
    )
    serializer_class = InventoryFactSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'date': ['exact', 'gte', 'lte'],
        'store': ['exact'],
        'product': ['exact'],
        'season': ['exact'],
        'weather': ['exact'],
        'holiday_promotion': ['exact']
    }
    ordering_fields = ['date', 'units_sold', 'price']
    ordering = ['-date']
    