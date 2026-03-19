from __future__ import annotations

from functools import lru_cache
from typing import Dict, List

import numpy as np
import pandas as pd

from api.models import InventoryFact


STORE_REGION_COORDS = {
    'North': {'lat': 25.6866, 'lng': -100.3161},
    'South': {'lat': 16.8531, 'lng': -99.8237},
    'East': {'lat': 19.1738, 'lng': -96.1342},
    'West': {'lat': 20.6597, 'lng': -103.3496},
}

STORE_OFFSETS = {
    'S001': (0.00, 0.00),
    'S002': (0.12, -0.18),
    'S003': (-0.15, 0.16),
    'S004': (0.20, 0.10),
    'S005': (-0.08, -0.22),
}


def _safe_float(value) -> float:
    if pd.isna(value):
        return 0.0
    return float(value)


@lru_cache(maxsize=8)
def load_inventory_dataframe() -> pd.DataFrame:
    queryset = InventoryFact.objects.select_related(
        'store',
        'product',
        'product__category',
        'weather',
        'season'
    ).values(
        'date',
        'store_id',
        'store__region',
        'product_id',
        'product__product_name',
        'product__category__category_name',
        'inventory_level',
        'units_sold',
        'units_ordered',
        'demand_forecast',
        'price',
        'discount',
        'weather__weather_type',
        'season__season_name',
        'holiday_promotion',
        'competitor_pricing',
    )

    df = pd.DataFrame(list(queryset))

    if df.empty:
        return df

    df = df.rename(columns={
        'store_id': 'store_id',
        'store__region': 'region',
        'product_id': 'product_id',
        'product__product_name': 'product_name',
        'product__category__category_name': 'category',
        'weather__weather_type': 'weather',
        'season__season_name': 'season',
    })

    df['date'] = pd.to_datetime(df['date'])
    numeric_columns = [
        'inventory_level',
        'units_sold',
        'units_ordered',
        'demand_forecast',
        'price',
        'discount',
        'competitor_pricing',
    ]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['revenue'] = df['units_sold'] * df['price']
    df['fill_rate'] = np.where(
        df['units_ordered'] > 0,
        df['units_sold'] / df['units_ordered'],
        0
    )
    df['sell_through'] = np.where(
        df['inventory_level'] > 0,
        df['units_sold'] / df['inventory_level'],
        0
    )
    df['product_name'] = df['product_name'].fillna('')
    df['display_product'] = np.where(
        df['product_name'].str.strip() != '',
        df['product_name'] + ' (' + df['product_id'] + ')',
        df['product_id'] + ' · ' + df['category']
    )

    return df


def choose_reference_year(df: pd.DataFrame) -> int:
    years = sorted(df['date'].dt.year.unique().tolist())
    if len(years) == 1:
        return years[0]

    max_date = df['date'].max()
    latest_year = max_date.year
    counts = df.groupby(df['date'].dt.year)['date'].count().to_dict()

    # Si el último año está incompleto, usar el anterior para YoY.
    if counts.get(latest_year, 0) < (counts.get(years[-2], 0) * 0.6):
        return years[-2]
    return latest_year


def build_overview_payload() -> Dict:
    df = load_inventory_dataframe()
    if df.empty:
        return {'kpis': [], 'top_products': [], 'top_stores': [], 'top_categories': [], 'insights': [], 'recent_products': []}

    total_revenue = float(df['revenue'].sum())
    total_units = int(df['units_sold'].sum())
    total_stores = int(df['store_id'].nunique())
    total_products = int(df['product_id'].nunique())
    avg_discount = float(df['discount'].mean())

    understock_risk = int((df['inventory_level'] < df['demand_forecast']).sum())
    promo_uplift = (
        df[df['holiday_promotion'] == True]['units_sold'].mean()
        - df[df['holiday_promotion'] == False]['units_sold'].mean()
    )
    competitor_gap = float((df['price'] - df['competitor_pricing']).mean())

    top_products = (
        df.groupby(['product_id', 'display_product', 'category'], as_index=False)
        .agg(units_sold=('units_sold', 'sum'), revenue=('revenue', 'sum'))
        .sort_values('units_sold', ascending=False)
        .head(10)
    )

    top_stores = (
        df.groupby(['store_id', 'region'], as_index=False)
        .agg(units_sold=('units_sold', 'sum'), revenue=('revenue', 'sum'), avg_fill_rate=('fill_rate', 'mean'))
        .sort_values('revenue', ascending=False)
        .head(10)
    )

    top_categories = (
        df.groupby('category', as_index=False)
        .agg(units_sold=('units_sold', 'sum'), revenue=('revenue', 'sum'))
        .sort_values('revenue', ascending=False)
        .head(10)
    )

    latest_cut = df['date'].max() - pd.Timedelta(days=30)
    recent_products = (
        df[df['date'] >= latest_cut]
        .groupby(['product_id', 'display_product', 'category'], as_index=False)
        .agg(recent_units=('units_sold', 'sum'), recent_revenue=('revenue', 'sum'))
        .sort_values('recent_units', ascending=False)
        .head(6)
    )

    return {
        'kpis': [
            {'label': 'Ventas totales', 'value': round(total_revenue, 2), 'format': 'currency'},
            {'label': 'Unidades vendidas', 'value': total_units, 'format': 'integer'},
            {'label': 'Tiendas activas', 'value': total_stores, 'format': 'integer'},
            {'label': 'Productos activos', 'value': total_products, 'format': 'integer'},
            {'label': 'Descuento promedio', 'value': round(avg_discount, 2), 'format': 'percent'},
        ],
        'top_products': top_products.to_dict(orient='records'),
        'top_stores': top_stores.to_dict(orient='records'),
        'top_categories': top_categories.to_dict(orient='records'),
        'insights': [
            {
                'title': 'Riesgo de quiebre',
                'description': f'{understock_risk:,} registros tienen inventario menor al forecast de demanda.'
            },
            {
                'title': 'Impacto de promociones',
                'description': f'Las promociones elevan en promedio {promo_uplift:.2f} unidades por registro frente a días sin promoción.'
            },
            {
                'title': 'Precio vs competencia',
                'description': f'El diferencial promedio frente a la competencia es de {competitor_gap:.2f}.'
            }
        ],
        'recent_products': recent_products.to_dict(orient='records'),
        'notes': [
            'El dataset actual no trae fecha de alta del producto; la sección de nuevos agregados usa actividad reciente como proxy.',
        ]
    }


def build_dashboard_payload(year: int | None = None) -> Dict:
    df = load_inventory_dataframe()
    if df.empty:
        return {'top_chain': [], 'top_by_category': [], 'monthly_compare': [], 'yoy_table': [], 'meta': {}}

    year = year or choose_reference_year(df)
    prev_year = year - 1

    current_df = df[df['date'].dt.year == year].copy()
    previous_df = df[df['date'].dt.year == prev_year].copy()

    top_chain = (
        current_df.groupby(['product_id', 'display_product', 'category'], as_index=False)
        .agg(units_sold=('units_sold', 'sum'), revenue=('revenue', 'sum'))
        .sort_values('units_sold', ascending=False)
        .head(10)
    )

    top_by_category = (
        current_df.groupby(['category', 'product_id', 'display_product'], as_index=False)
        .agg(units_sold=('units_sold', 'sum'), revenue=('revenue', 'sum'))
        .sort_values(['category', 'units_sold'], ascending=[True, False])
    )
    top_by_category = (
        top_by_category.groupby('category', group_keys=False)
        .head(3)
        .to_dict(orient='records')
    )

    current_month = (
        current_df.assign(month=current_df['date'].dt.month)
        .groupby('month', as_index=False)
        .agg(revenue=('revenue', 'sum'), units_sold=('units_sold', 'sum'))
    )
    previous_month = (
        previous_df.assign(month=previous_df['date'].dt.month)
        .groupby('month', as_index=False)
        .agg(revenue_prev=('revenue', 'sum'), units_prev=('units_sold', 'sum'))
    )

    monthly_compare = current_month.merge(previous_month, on='month', how='left').fillna(0)
    monthly_compare['revenue_variation_pct'] = np.where(
        monthly_compare['revenue_prev'] > 0,
        ((monthly_compare['revenue'] - monthly_compare['revenue_prev']) / monthly_compare['revenue_prev']) * 100,
        0
    )

    yoy_table = (
        current_df.groupby('category', as_index=False)
        .agg(current_revenue=('revenue', 'sum'), current_units=('units_sold', 'sum'))
        .merge(
            previous_df.groupby('category', as_index=False)
            .agg(previous_revenue=('revenue', 'sum'), previous_units=('units_sold', 'sum')),
            on='category',
            how='left'
        )
        .fillna(0)
    )
    yoy_table['revenue_change_pct'] = np.where(
        yoy_table['previous_revenue'] > 0,
        ((yoy_table['current_revenue'] - yoy_table['previous_revenue']) / yoy_table['previous_revenue']) * 100,
        0
    )
    yoy_table['units_change_pct'] = np.where(
        yoy_table['previous_units'] > 0,
        ((yoy_table['current_units'] - yoy_table['previous_units']) / yoy_table['previous_units']) * 100,
        0
    )

    distributor_note = {
        'supported_today': [
            'cadena',
            'categoría',
            'tienda',
            'producto',
            'región',
            'temporada',
            'clima',
        ],
        'next_step': 'Para bajar al nivel distribuidor/proveedor se debe incorporar distributor_id, lead_time, costo y OTIF al fact table.'
    }

    return {
        'top_chain': top_chain.to_dict(orient='records'),
        'top_by_category': top_by_category,
        'monthly_compare': monthly_compare.to_dict(orient='records'),
        'yoy_table': yoy_table.to_dict(orient='records'),
        'meta': {
            'year': year,
            'previous_year': prev_year,
            'distributor_scope': distributor_note,
        }
    }


def enrich_store_coordinates(store_row: pd.Series) -> Dict:
    region = store_row['region']
    center = STORE_REGION_COORDS.get(region, {'lat': 19.4326, 'lng': -99.1332})
    offset = STORE_OFFSETS.get(store_row['store_id'], (0.0, 0.0))
    return {
        'lat': center['lat'] + offset[0],
        'lng': center['lng'] + offset[1],
    }


def build_export_dataframe(filters: Dict[str, str]) -> pd.DataFrame:
    df = load_inventory_dataframe().copy()
    if df.empty:
        return df

    if filters.get('store_id'):
        df = df[df['store_id'] == filters['store_id']]
    if filters.get('product_id'):
        df = df[df['product_id'] == filters['product_id']]
    if filters.get('category'):
        df = df[df['category'] == filters['category']]
    if filters.get('region'):
        df = df[df['region'] == filters['region']]
    if filters.get('date_from'):
        df = df[df['date'] >= pd.to_datetime(filters['date_from'])]
    if filters.get('date_to'):
        df = df[df['date'] <= pd.to_datetime(filters['date_to'])]

    return df.sort_values('date')
