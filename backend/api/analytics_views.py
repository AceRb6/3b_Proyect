from __future__ import annotations

from io import BytesIO

import pandas as pd
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from api.services.forecasting import build_forecast_payload
from api.services.insights import (
    build_dashboard_payload,
    build_export_dataframe,
    build_overview_payload,
    enrich_store_coordinates,
    load_inventory_dataframe,
)


@api_view(['GET'])
def overview_view(request):
    return Response(build_overview_payload())


@api_view(['GET'])
def dashboard_view(request):
    year = request.query_params.get('year')
    year = int(year) if year else None
    return Response(build_dashboard_payload(year=year))


@api_view(['GET'])
def stores_view(request):
    df = load_inventory_dataframe().copy()
    if df.empty:
        return Response({'stores': [], 'clusters': [], 'heatmap': [], 'meta': {}})

    stores = (
        df.groupby(['store_id', 'region'], as_index=False)
        .agg(
            revenue=('revenue', 'sum'),
            units_sold=('units_sold', 'sum'),
            avg_discount=('discount', 'mean'),
            avg_fill_rate=('fill_rate', 'mean'),
            avg_sell_through=('sell_through', 'mean'),
        )
        .sort_values('revenue', ascending=False)
    )

    features = stores[['revenue', 'units_sold', 'avg_discount', 'avg_fill_rate', 'avg_sell_through']].fillna(0)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    clusters_count = min(3, len(stores))
    if clusters_count > 1:
        model = KMeans(n_clusters=clusters_count, random_state=42, n_init=10)
        stores['cluster'] = model.fit_predict(scaled)
    else:
        stores['cluster'] = 0

    coords = stores.apply(enrich_store_coordinates, axis=1, result_type='expand')
    stores['lat'] = coords['lat']
    stores['lng'] = coords['lng']

    cluster_summary = (
        stores.groupby('cluster', as_index=False)
        .agg(
            stores=('store_id', 'count'),
            revenue=('revenue', 'sum'),
            avg_fill_rate=('avg_fill_rate', 'mean'),
        )
        .sort_values('revenue', ascending=False)
    )

    heatmap = stores[['store_id', 'lat', 'lng', 'revenue']].copy()
    max_revenue = max(float(heatmap['revenue'].max()), 1.0)
    heatmap['intensity'] = heatmap['revenue'] / max_revenue

    return Response({
        'stores': stores.to_dict(orient='records'),
        'clusters': cluster_summary.to_dict(orient='records'),
        'heatmap': heatmap.to_dict(orient='records'),
        'meta': {
            'note': 'Las coordenadas son demostrativas por región. Para producción se recomienda usar lat/lng reales del punto de venta.'
        }
    })


@api_view(['GET'])
def forecast_view(request):
    category = request.query_params.get('category')
    store_id = request.query_params.get('store_id')
    horizon_days = int(request.query_params.get('horizon_days', 30))
    return Response(build_forecast_payload(category=category, store_id=store_id, horizon_days=horizon_days))


@api_view(['GET'])
def export_sales_excel_view(request):
    filters = {
        'store_id': request.query_params.get('store_id'),
        'product_id': request.query_params.get('product_id'),
        'category': request.query_params.get('category'),
        'region': request.query_params.get('region'),
        'date_from': request.query_params.get('date_from'),
        'date_to': request.query_params.get('date_to'),
    }

    df = build_export_dataframe(filters)
    if df.empty:
        return Response({'detail': 'No hay datos para exportar con esos filtros.'}, status=404)

    detail = df.copy()
    detail['date'] = detail['date'].dt.strftime('%Y-%m-%d')

    summary = (
        df.groupby(['store_id', 'category'], as_index=False)
        .agg(
            revenue=('revenue', 'sum'),
            units_sold=('units_sold', 'sum'),
            avg_price=('price', 'mean'),
            avg_discount=('discount', 'mean'),
        )
        .sort_values('revenue', ascending=False)
    )

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        detail.to_excel(writer, index=False, sheet_name='Detalle')
        summary.to_excel(writer, index=False, sheet_name='Resumen')
        pd.DataFrame([filters]).to_excel(writer, index=False, sheet_name='Filtros')

    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="ventas_filtradas.xlsx"'
    return response
