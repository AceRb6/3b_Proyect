from django.db import models

class Store(models.Model):
    store_id = models.CharField(max_length=10, primary_key=True)
    region = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'stores'
        managed = False
    
    def __str__(self):
        return f"{self.store_id} - {self.region}"

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'categories'
        managed = False
    
    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_id = models.CharField(max_length=10, primary_key=True)
    product_name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_column='category_id')
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'products'
        managed = False
    
    def __str__(self):
        return self.product_id

class WeatherCondition(models.Model):
    weather_id = models.AutoField(primary_key=True)
    weather_type = models.CharField(max_length=20, unique=True)
    
    class Meta:
        db_table = 'weather_conditions'
        managed = False
    
    def __str__(self):
        return self.weather_type

class Season(models.Model):
    season_id = models.AutoField(primary_key=True)
    season_name = models.CharField(max_length=20, unique=True)
    
    class Meta:
        db_table = 'seasons'
        managed = False
    
    def __str__(self):
        return self.season_name

class InventoryFact(models.Model):
    fact_id = models.AutoField(primary_key=True)
    date = models.DateField()
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING, db_column='store_id')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, db_column='product_id')
    weather = models.ForeignKey(WeatherCondition, on_delete=models.DO_NOTHING, db_column='weather_id')
    season = models.ForeignKey(Season, on_delete=models.DO_NOTHING, db_column='season_id')
    inventory_level = models.IntegerField(null=True, blank=True)
    units_sold = models.IntegerField(null=True, blank=True)
    units_ordered = models.IntegerField(null=True, blank=True)
    demand_forecast = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    competitor_pricing = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    holiday_promotion = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'inventory_facts'
        managed = False
        unique_together = ['date', 'store', 'product']
    
    def __str__(self):
        return f"{self.date} - {self.store_id} - {self.product_id}"