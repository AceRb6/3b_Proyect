import { useEffect, useState } from "react";
import { getJson } from "../api/client";
import { useAuth } from "../hooks/useAuth";
import SectionCard from "../components/SectionCard";
import TopList from "../components/TopList";
import DataTable from "../components/DataTable";
import { RevenueVsPreviousChart } from "../components/Charts";

function formatCurrency(value) {
  return new Intl.NumberFormat("es-MX", {
    style: "currency",
    currency: "MXN",
    maximumFractionDigits: 0,
  }).format(value || 0);
}

export default function DashboardPage() {
  const { token } = useAuth();
  const [data, setData] = useState({
    top_chain: [],
    top_by_category: [],
    monthly_compare: [],
    yoy_table: [],
    meta: {},
  });

  useEffect(() => {
    getJson("/insights/dashboard/", token).then(setData);
  }, [token]);

  return (
    <div className="page-grid">
      <div className="hero-panel compact">
        <div>
          <span className="eyebrow">Dashboard analítico</span>
          <h1>Productos más vendidos, variación YoY y alcance analítico</h1>
          <p>
            Aquí se compara cadena vs. categoría y se deja visible hasta dónde
            llega el modelo con el dataset actual.
          </p>
        </div>
      </div>

      <div className="split-grid">
        <SectionCard title={`Top cadena ${data.meta.year || ""}`}>
          <TopList
            items={data.top_chain}
            primaryKey="product_id"
            titleKey="display_product"
            subtitleKey="category"
            valueKey="units_sold"
            valueFormatter={(value) => new Intl.NumberFormat("es-MX").format(value)}
          />
        </SectionCard>

        <SectionCard title="Top por categoría">
          <TopList
            items={data.top_by_category}
            primaryKey="product_id"
            titleKey="display_product"
            subtitleKey="category"
            valueKey="units_sold"
            valueFormatter={(value) => new Intl.NumberFormat("es-MX").format(value)}
          />
        </SectionCard>
      </div>

      <SectionCard title="Comparativo mensual vs año anterior">
        <RevenueVsPreviousChart data={data.monthly_compare} />
      </SectionCard>

      <SectionCard title="Tabla comparativa YoY">
        <DataTable
          columns={[
            { key: "category", label: "Categoría" },
            {
              key: "current_revenue",
              label: `Ventas ${data.meta.year || "actual"}`,
              render: (value) => formatCurrency(value),
            },
            {
              key: "previous_revenue",
              label: `Ventas ${data.meta.previous_year || "anterior"}`,
              render: (value) => formatCurrency(value),
            },
            {
              key: "revenue_change_pct",
              label: "Var. ventas %",
              render: (value) => `${Number(value).toFixed(1)}%`,
            },
            {
              key: "units_change_pct",
              label: "Var. unidades %",
              render: (value) => `${Number(value).toFixed(1)}%`,
            },
          ]}
          rows={data.yoy_table}
        />
      </SectionCard>

      <SectionCard title="Hasta dónde llega el data actual">
        <div className="insight-box">
          <strong>Granos actualmente soportados</strong>
          <p>
            {(data.meta.distributor_scope?.supported_today || []).join(", ")}
          </p>
          <strong>Siguiente paso para distribuidores</strong>
          <p>{data.meta.distributor_scope?.next_step}</p>
        </div>
      </SectionCard>
    </div>
  );
}
