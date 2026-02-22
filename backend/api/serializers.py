from rest_framework import serializers
from .models import Store, Category, Product, WeatherCondition, Season, InventoryFact

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'category', 'category_name', 'base_price']

class WeatherConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCondition
        fields = '__all__'

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'

class InventoryFactSerializer(serializers.ModelSerializer):
    store_region = serializers.CharField(source='store.region', read_only=True)
    product_category = serializers.CharField(source='product.category.category_name', read_only=True)
    weather_type = serializers.CharField(source='weather.weather_type', read_only=True)
    season_name = serializers.CharField(source='season.season_name', read_only=True)
    
    class Meta:
        model = InventoryFact
        fields = [
            'fact_id', 'date', 'store', 'store_region', 'product', 'product_category',
            'weather', 'weather_type', 'season', 'season_name', 'inventory_level',
            'units_sold', 'units_ordered', 'demand_forecast', 'price', 'discount',
            'competitor_pricing', 'holiday_promotion'
        ]
        