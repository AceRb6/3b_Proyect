import { useState } from "react";
import { downloadExcel } from "../api/client";
import { useAuth } from "../hooks/useAuth";
import SectionCard from "../components/SectionCard";

export default function ExportsPage() {
  const { token } = useAuth();
  const [filters, setFilters] = useState({
    category: "",
    store_id: "",
    region: "",
    date_from: "",
    date_to: "",
  });
  const [downloading, setDownloading] = useState(false);

  const onChange = (event) => {
    const { name, value } = event.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  const onDownload = async () => {
    const query = new URLSearchParams(
      Object.entries(filters).filter(([, value]) => value)
    ).toString();

    setDownloading(true);
    try {
      await downloadExcel(
        `/exports/sales.xlsx${query ? `?${query}` : ""}`,
        token,
        "ventas_storytelling.xlsx"
      );
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="page-grid">
      <div className="hero-panel compact">
        <div>
          <span className="eyebrow">Descargas</span>
          <h1>Consultas listas para Excel y storytelling</h1>
          <p>
            Este módulo permite descargar ventas específicas con filtros para que
            el equipo genere análisis externos y presentaciones.
          </p>
        </div>
      </div>

      <SectionCard title="Filtros de exportación">
        <div className="filters-grid">
          <label>
            Categoría
            <input name="category" value={filters.category} onChange={onChange} />
          </label>
          <label>
            Tienda
            <input name="store_id" value={filters.store_id} onChange={onChange} />
          </label>
          <label>
            Región
            <input name="region" value={filters.region} onChange={onChange} />
          </label>
          <label>
            Desde
            <input type="date" name="date_from" value={filters.date_from} onChange={onChange} />
          </label>
          <label>
            Hasta
            <input type="date" name="date_to" value={filters.date_to} onChange={onChange} />
          </label>
        </div>

        <button className="primary-button" onClick={onDownload} disabled={downloading}>
          {downloading ? "Generando Excel..." : "Descargar Excel"}
        </button>
      </SectionCard>
    </div>
  );
}
