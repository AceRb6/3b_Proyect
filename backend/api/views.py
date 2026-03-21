from datetime import datetime, timedelta

from django.db.models import F, Sum
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets

from .models import (
    Category,
    InventoryFact,
    Product,
    Season,
    Store,
    WeatherCondition,
)
from .serializers import (
    CategorySerializer,
    InventoryFactSerializer,
    ProductSerializer,
    SeasonSerializer,
    StoreSerializer,
    WeatherConditionSerializer,
)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all().order_by("store_id")
    serializer_class = StoreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("category_id")
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all().order_by("product_id")
    serializer_class = ProductSerializer


class WeatherConditionViewSet(viewsets.ModelViewSet):
    queryset = WeatherCondition.objects.all().order_by("weather_id")
    serializer_class = WeatherConditionSerializer


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.all().order_by("season_id")
    serializer_class = SeasonSerializer


class InventoryFactViewSet(viewsets.ModelViewSet):
    queryset = (
        InventoryFact.objects.select_related("store", "product__category", "weather", "season")
        .all()
        .order_by("-date")
    )
    serializer_class = InventoryFactSerializer

# ----------------------------------------------------------------------
# Vista que devuelve la página HTML del dashboard
# ----------------------------------------------------------------------
def dashboard(request):
    """Renderiza la plantilla del panel de control."""
    return render(request, "dashboard.html")   # Django buscará en api/templates/

def tiendas(request):
    return render(request, "tiendas.html")

# ----------------------------------------------------------------------
# Vista que devuelve los datos agregados para el dashboard (JSON)
# ----------------------------------------------------------------------
def dashboard_data(request):
    """
    JSON con:
      - top_10_products, top_10_stores, low_inventory,
        monthly_sales, last_update
    """
    # Top 10 productos
    top_products_qs = (
        InventoryFact.objects
        .values('product__product_id', 'product__product_name')
        .annotate(units_sold=Sum('units_sold'))
        .order_by('-units_sold')[:10]
    )
    top_products = [
        {"product_id": p["product__product_id"],
         "product_name": p["product__product_name"],
         "units_sold": p["units_sold"]} for p in top_products_qs
    ]

    # Top 10 tiendas
    top_stores_qs = (
        InventoryFact.objects
        .values('store__store_id', 'store__region')
        .annotate(units_sold=Sum('units_sold'))
        .order_by('-units_sold')[:10]
    )
    top_stores = [
        {"store_id": s["store__store_id"],
         "region": s["store__region"],
         "units_sold": s["units_sold"]} for s in top_stores_qs
    ]

    # Inventario bajo
    LOW_THRESHOLD = 10
    low_inventory_qs = (
        InventoryFact.objects
        .filter(inventory_level__lt=LOW_THRESHOLD)
        .values('store__store_id', 'product__product_id', 'inventory_level')
    )
    low_inventory = [
        {"store_id": a["store__store_id"],
         "product_id": a["product__product_id"],
         "inventory_level": a["inventory_level"]} for a in low_inventory_qs
    ]

    # Ventas mensuales del último año (MULTIPLICANDO units_sold * price)
    today = datetime.today().date()
    one_year_ago = today - timedelta(days=365)
    monthly_qs = (
        InventoryFact.objects
        .filter(date__gte=one_year_ago)
        .annotate(month=F('date__year') * 100 + F('date__month'))
        .annotate(total_sales=F('units_sold') * F('price'))
        .values('month')
        .annotate(sales_value=Sum('total_sales'))
        .order_by('month')
    )
    monthly_sales = {
        f"{m['month'] // 100:04d}-{m['month'] % 100:02d}": float(m["sales_value"] or 0)
        for m in monthly_qs
    }

    # Última actualización
    last_fact = InventoryFact.objects.order_by('-date').first()
    last_update = last_fact.date.isoformat() if last_fact else None

    return JsonResponse({
        "top_10_products": top_products,
        "top_10_stores": top_stores,
        "low_inventory": low_inventory,
        "monthly_sales": monthly_sales,
        "last_update": last_update,
    })
    
    