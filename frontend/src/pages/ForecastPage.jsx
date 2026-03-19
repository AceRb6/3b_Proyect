import { useEffect, useState } from "react";
import { getJson } from "../api/client";
import { useAuth } from "../hooks/useAuth";
import SectionCard from "../components/SectionCard";
import { ForecastChart } from "../components/Charts";

export default function ForecastPage() {
  const { token } = useAuth();
  const [category, setCategory] = useState("");
  const [data, setData] = useState({ history: [], forecast: [], meta: {} });

  useEffect(() => {
    const query = category ? `?category=${encodeURIComponent(category)}` : "";
    getJson(`/insights/forecast/${query}`, token).then(setData);
  }, [token, category]);

  return (
    <div className="page-grid">
      <div className="hero-panel compact">
        <div>
          <span className="eyebrow">Forecasting</span>
          <h1>Predicción de ventas con justificación de negocio</h1>
          <p>
            La predicción devuelve serie histórica, proyección futura y el
            argumento para defender el modelo ante dirección.
          </p>
        </div>

        <div className="filters-inline">
          <input
            placeholder="Filtrar por categoría, ej. Electronics"
            value={category}
            onChange={(event) => setCategory(event.target.value)}
          />
        </div>
      </div>

      <SectionCard title="Serie histórica vs forecast">
        <ForecastChart history={data.history} forecast={data.forecast} />
      </SectionCard>

      <SectionCard title="Justificación del modelo">
        <div className="insights-list">
          <article className="insight-box">
            <strong>Método</strong>
            <p>{data.meta.method}</p>
          </article>
          <article className="insight-box">
            <strong>Horizonte</strong>
            <p>{data.meta.horizon_days} días</p>
          </article>
          <article className="insight-box">
            <strong>MAPE</strong>
            <p>{data.meta.mape}%</p>
          </article>
          <article className="insight-box">
            <strong>Justificación</strong>
            <p>{data.meta.explanation}</p>
          </article>
        </div>
      </SectionCard>
    </div>
  );
}
