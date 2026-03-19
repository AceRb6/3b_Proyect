from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import pandas as pd

from api.services.insights import load_inventory_dataframe

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
except Exception:  # pragma: no cover
    ExponentialSmoothing = None


@dataclass
class ForecastMeta:
    method: str
    horizon_days: int
    explanation: str
    mape: float


def _prepare_series(category: Optional[str] = None, store_id: Optional[str] = None) -> pd.Series:
    df = load_inventory_dataframe().copy()
    if category:
        df = df[df['category'] == category]
    if store_id:
        df = df[df['store_id'] == store_id]

    series = (
        df.groupby('date', as_index=True)['revenue']
        .sum()
        .sort_index()
        .asfreq('D', fill_value=0)
    )
    return series


def _forecast_with_holt_winters(series: pd.Series, horizon_days: int):
    train = series.iloc[:-30] if len(series) > 90 else series
    test = series.iloc[-30:] if len(series) > 90 else pd.Series(dtype=float)

    model = ExponentialSmoothing(
        train,
        trend='add',
        seasonal='add',
        seasonal_periods=7,
        initialization_method='estimated'
    )
    fit = model.fit(optimized=True)
    forecast = fit.forecast(horizon_days)

    mape = 0.0
    if not test.empty:
        eval_forecast = fit.forecast(len(test))
        denominator = test.replace(0, np.nan)
        mape = float(np.nanmean(np.abs((test - eval_forecast) / denominator)) * 100)

    return forecast, mape


def _forecast_with_linear_trend(series: pd.Series, horizon_days: int):
    train = series.reset_index(drop=True)
    x = np.arange(len(train))
    coeffs = np.polyfit(x, train.values, deg=1)
    future_x = np.arange(len(train), len(train) + horizon_days)
    pred = np.polyval(coeffs, future_x)
    pred = np.maximum(pred, 0)
    future_index = pd.date_range(series.index.max() + pd.Timedelta(days=1), periods=horizon_days, freq='D')
    forecast = pd.Series(pred, index=future_index)

    mape = 0.0
    if len(series) > 60:
        test = series.iloc[-14:]
        train2 = series.iloc[:-14].reset_index(drop=True)
        x2 = np.arange(len(train2))
        coeffs2 = np.polyfit(x2, train2.values, deg=1)
        pred2 = np.polyval(coeffs2, np.arange(len(train2), len(train2) + len(test)))
        denominator = test.replace(0, np.nan)
        mape = float(np.nanmean(np.abs((test.values - pred2) / denominator)) * 100)
    return forecast, mape


def build_forecast_payload(category: Optional[str] = None, store_id: Optional[str] = None, horizon_days: int = 30) -> Dict:
    series = _prepare_series(category=category, store_id=store_id)
    if series.empty:
        return {'history': [], 'forecast': [], 'meta': {}}

    if ExponentialSmoothing is not None and len(series) >= 90:
        forecast, mape = _forecast_with_holt_winters(series, horizon_days)
        method = 'Holt-Winters'
        explanation = (
            'Se usa Holt-Winters porque las ventas diarias presentan tendencia y estacionalidad semanal. '
            'Es una opción interpretable y defendible para storytelling ejecutivo.'
        )
    else:
        forecast, mape = _forecast_with_linear_trend(series, horizon_days)
        method = 'Tendencia lineal'
        explanation = (
            'Se usa una tendencia lineal como fallback cuando no hay suficientes datos o la librería avanzada no está disponible.'
        )

    history = series.tail(90).reset_index()
    history.columns = ['date', 'value']

    forecast_df = forecast.reset_index()
    forecast_df.columns = ['date', 'value']

    return {
        'history': history.assign(date=lambda x: x['date'].dt.strftime('%Y-%m-%d')).to_dict(orient='records'),
        'forecast': forecast_df.assign(date=lambda x: x['date'].dt.strftime('%Y-%m-%d')).to_dict(orient='records'),
        'meta': {
            'method': method,
            'horizon_days': horizon_days,
            'mape': round(mape, 2),
            'explanation': explanation,
            'filters': {
                'category': category,
                'store_id': store_id,
            }
        }
    }
