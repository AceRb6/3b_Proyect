import { useEffect, useState } from "react";
import { ChevronRight, MapPinned, Package, TrendingUp, Download } from "lucide-react";
import { Link } from "react-router-dom";
import { getJson } from "../api/client";
import { useAuth } from "../hooks/useAuth";
import MetricCard from "../components/MetricCard";
import SectionCard from "../components/SectionCard";
import TopList from "../components/TopList";

export default function HomePage() {
  const { token } = useAuth();
  const [data, setData] = useState({
    kpis: [],
    top_products: [],
    top_stores: [],
    top_categories: [],
    insights: [],
    recent_products: [],
  });

  useEffect(() => {
    getJson("/insights/overview/", token).then(setData);
  }, [token]);

  const menu = [
    { title: "Dashboard avanzado", to: "/dashboard", icon: Package },
    { title: "Info de tiendas", to: "/tiendas", icon: MapPinned },
    { title: "Forecasting", to: "/forecast", icon: TrendingUp },
    { title: "Descargas Excel", to: "/descargas", icon: Download },
  ];

  return (
    <div className="page-grid">
      <div className="hero-panel">
        <div>
          <span className="eyebrow">Visión general</span>
          <h1>Centro ejecutivo de ventas, tiendas y demanda</h1>
          <p>
            Esta portada concentra KPIs de cadena, top 10, hallazgos clave y
            accesos directos a vistas avanzadas.
          </p>
        </div>
      </div>

      <div className="metrics-grid">
        {data.kpis.map((metric) => (
          <MetricCard key={metric.label} {...metric} />
        ))}
      </div>

      <div className="home-grid">
        <SectionCard title="Top 10 productos">
          <TopList
            items={data.top_products}
            primaryKey="product_id"
            titleKey="display_product"
            subtitleKey="category"
            valueKey="units_sold"
            valueFormatter={(value) => new Intl.NumberFormat("es-MX").format(value)}
          />
        </SectionCard>

        <SectionCard title="Top tiendas por ventas">
          <TopList
            items={data.top_stores}
            primaryKey="store_id"
            titleKey="store_id"
            subtitleKey="region"
            valueKey="revenue"
            valueFormatter="currency"
          />
        </SectionCard>

        <SectionCard title="Categorías más relevantes">
          <TopList
            items={data.top_categories}
            primaryKey="category"
            titleKey="category"
            valueKey="revenue"
            valueFormatter="currency"
          />
        </SectionCard>

        <SectionCard title="Productos destacados recientemente">
          <TopList
            items={data.recent_products}
            primaryKey="product_id"
            titleKey="display_product"
            subtitleKey="category"
            valueKey="recent_units"
            valueFormatter={(value) => new Intl.NumberFormat("es-MX").format(value)}
          />
        </SectionCard>
      </div>

      <div className="split-grid">
        <SectionCard title="Hallazgos clave">
          <div className="insights-list">
            {data.insights.map((item) => (
              <article key={item.title} className="insight-box">
                <strong>{item.title}</strong>
                <p>{item.description}</p>
              </article>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Menú principal de vistas avanzadas">
          <div className="menu-grid">
            {menu.map((item) => {
              const Icon = item.icon;
              return (
                <Link key={item.to} to={item.to} className="menu-tile">
                  <Icon size={22} />
                  <div>
                    <strong>{item.title}</strong>
                    <span>Entrar</span>
                  </div>
                  <ChevronRight size={18} />
                </Link>
              );
            })}
          </div>
        </SectionCard>
      </div>
    </div>
  );
}
