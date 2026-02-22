from django.contrib import admin
from .models import Store, Category, Product, WeatherCondition, Season, InventoryFact

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_id', 'region']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'category_name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'product_name', 'category', 'base_price']

@admin.register(WeatherCondition)
class WeatherConditionAdmin(admin.ModelAdmin):
    list_display = ['weather_id', 'weather_type']

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['season_id', 'season_name']

@admin.register(InventoryFact)
class InventoryFactAdmin(admin.ModelAdmin):
    list_display = ['fact_id', 'date', 'store', 'product', 'units_sold', 'price']
    list_filter = ['date', 'store', 'season', 'holiday_promotion']
    date_hierarchy = 'date'