from django.urls import path

from api.analytics_views import (
    dashboard_view,
    export_sales_excel_view,
    forecast_view,
    overview_view,
    stores_view,
)
from api.auth_views import login_view, logout_view, me_view

urlpatterns = [
    path('auth/login/', login_view, name='auth-login'),
    path('auth/me/', me_view, name='auth-me'),
    path('auth/logout/', logout_view, name='auth-logout'),
    path('insights/overview/', overview_view, name='insights-overview'),
    path('insights/dashboard/', dashboard_view, name='insights-dashboard'),
    path('insights/stores/', stores_view, name='insights-stores'),
    path('insights/forecast/', forecast_view, name='insights-forecast'),
    path('exports/sales.xlsx', export_sales_excel_view, name='exports-sales'),
]
