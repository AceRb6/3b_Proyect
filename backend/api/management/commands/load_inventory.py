import csv
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Store, Category, Product, WeatherCondition, Season, InventoryFact
from datetime import datetime


class Command(BaseCommand):
    help = 'Carga datos de inventario desde CSV a la base de datos normalizada'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ruta al archivo CSV')
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Número de registros por batch (default: 1000)'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        batch_size = options['batch_size']
        
        self.stdout.write(self.style.SUCCESS(f'Iniciando carga desde: {csv_file}'))
        
        # Contar total de filas para progreso
        total_rows = sum(1 for _ in open(csv_file, 'r', encoding='utf-8')) - 1
        self.stdout.write(f'Total de registros a cargar: {total_rows}')
        
        # Diccionarios para cachear IDs y evitar consultas repetidas
        stores_cache = {}
        categories_cache = {}
        products_cache = {}
        weather_cache = {}
        seasons_cache = {}
        
        # Precargar datos existentes
        self.stdout.write('Precargando datos existentes...')
        for store in Store.objects.all():
            stores_cache[store.store_id] = store
            
        for cat in Category.objects.all():
            categories_cache[cat.category_name] = cat
            
        for prod in Product.objects.all():
            products_cache[prod.product_id] = prod
            
        for weather in WeatherCondition.objects.all():
            weather_cache[weather.weather_type] = weather
            
        for season in Season.objects.all():
            seasons_cache[season.season_name] = season
        
        records_created = 0
        records_skipped = 0
        batch = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader, 1):
                try:
                    # Procesar dimensiones (crear si no existen)
                    
                    # Store
                    store_id = row['Store ID']
                    if store_id not in stores_cache:
                        store, _ = Store.objects.get_or_create(
                            store_id=store_id,
                            defaults={'region': row['Region']}
                        )
                        stores_cache[store_id] = store
                    
                    # Category
                    cat_name = row['Category']
                    if cat_name not in categories_cache:
                        cat, _ = Category.objects.get_or_create(
                            category_name=cat_name
                        )
                        categories_cache[cat_name] = cat
                    
                    # Product
                    prod_id = row['Product ID']
                    if prod_id not in products_cache:
                        product, _ = Product.objects.get_or_create(
                            product_id=prod_id,
                            defaults={
                                'category': categories_cache[cat_name],
                                'base_price': float(row['Price']) if row['Price'] else None
                            }
                        )
                        products_cache[prod_id] = product
                    
                    # Weather Condition
                    weather_type = row['Weather Condition']
                    if weather_type not in weather_cache:
                        weather, _ = WeatherCondition.objects.get_or_create(
                            weather_type=weather_type
                        )
                        weather_cache[weather_type] = weather
                    
                    # Season
                    season_name = row['Seasonality']
                    if season_name not in seasons_cache:
                        season, _ = Season.objects.get_or_create(
                            season_name=season_name
                        )
                        seasons_cache[season_name] = season
                    
                    # Crear registro de hechos
                    fact = InventoryFact(
                        date=datetime.strptime(row['Date'], '%Y-%m-%d').date(),
                        store=stores_cache[store_id],
                        product=products_cache[prod_id],
                        weather=weather_cache[weather_type],
                        season=seasons_cache[season_name],
                        inventory_level=int(row['Inventory Level']) if row['Inventory Level'] else None,
                        units_sold=int(row['Units Sold']) if row['Units Sold'] else None,
                        units_ordered=int(row['Units Ordered']) if row['Units Ordered'] else None,
                        demand_forecast=float(row['Demand Forecast']) if row['Demand Forecast'] else None,
                        price=float(row['Price']) if row['Price'] else None,
                        discount=float(row['Discount']) if row['Discount'] else None,
                        competitor_pricing=float(row['Competitor Pricing']) if row['Competitor Pricing'] else None,
                        holiday_promotion=bool(int(row['Holiday/Promotion'])) if row['Holiday/Promotion'] else False
                    )
                    
                    batch.append(fact)
                    
                    # Insertar en batches
                    if len(batch) >= batch_size:
                        with transaction.atomic():
                            InventoryFact.objects.bulk_create(
                                batch, 
                                ignore_conflicts=True,
                                batch_size=batch_size
                            )
                        records_created += len(batch)
                        batch = []
                        
                        # Mostrar progreso
                        progress = (i / total_rows) * 100
                        self.stdout.write(
                            f'Progreso: {progress:.1f}% ({i}/{total_rows}) - '
                            f'Registros creados: {records_created}'
                        )
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Error en fila {i}: {str(e)}')
                    )
                    records_skipped += 1
                    continue
        
        # Insertar batch final
        if batch:
            with transaction.atomic():
                InventoryFact.objects.bulk_create(
                    batch,
                    ignore_conflicts=True,
                    batch_size=batch_size
                )
            records_created += len(batch)
        
        self.stdout.write(self.style.SUCCESS(
            f'\nCarga completada!\n'
            f'Registros creados: {records_created}\n'
            f'Registros omitidos: {records_skipped}'
        ))