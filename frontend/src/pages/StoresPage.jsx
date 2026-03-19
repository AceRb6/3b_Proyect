import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Circle, Popup } from "react-leaflet";
import { getJson } from "../api/client";
import { useAuth } from "../hooks/useAuth";
import SectionCard from "../components/SectionCard";
import DataTable from "../components/DataTable";

function formatCurrency(value) {
  return new Intl.NumberFormat("es-MX", {
    style: "currency",
    currency: "MXN",
    maximumFractionDigits: 0,
  }).format(value || 0);
}

export default function StoresPage() {
  const { token } = useAuth();
  const [data, setData] = useState({
    stores: [],
    clusters: [],
    heatmap: [],
    meta: {},
  });

  useEffect(() => {
    getJson("/insights/stores/", token).then(setData);
  }, [token]);

  return (
    <div className="page-grid">
      <div className="hero-panel compact">
        <div>
          <span className="eyebrow">Tiendas y territorios</span>
          <h1>Ranking, clusters y lectura geográfica del punto de venta</h1>
          <p>
            El mapa usa coordenadas de demostración por región. En producción se
            reemplazan por latitud y longitud reales del POS.
          </p>
        </div>
      </div>

      <SectionCard title="Mapa de calor y agrupación por cluster">
        <div className="map-wrap">
          <MapContainer center={[23.6345, -102.5528]} zoom={5} scrollWheelZoom={false}>
            <TileLayer
              attribution='&copy; OpenStreetMap'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {data.heatmap.map((point) => (
              <Circle
                key={point.store_id}
                center={[point.lat, point.lng]}
                radius={15000 + point.intensity * 65000}
                pathOptions={{
                  color: "#e20a19",
                  fillColor: "#e20a19",
                  fillOpacity: 0.18 + point.intensity * 0.22,
                }}
              >
                <Popup>
                  <strong>{point.store_id}</strong>
                  <br />
                  Intensidad: {(point.intensity * 100).toFixed(1)}%
                </Popup>
              </Circle>
            ))}
          </MapContainer>
        </div>
        <small className="helper-text">{data.meta.note}</small>
      </SectionCard>

      <div className="split-grid">
        <SectionCard title="Tiendas con más ventas">
          <DataTable
            columns={[
              { key: "store_id", label: "Tienda" },
              { key: "region", label: "Región" },
              {
                key: "revenue",
                label: "Ventas",
                render: (value) => formatCurrency(value),
              },
              {
                key: "avg_fill_rate",
                label: "Fill rate",
                render: (value) => `${(value * 100).toFixed(1)}%`,
              },
              { key: "cluster", label: "Cluster" },
            ]}
            rows={data.stores}
          />
        </SectionCard>

        <SectionCard title="Resumen de clusters">
          <DataTable
            columns={[
              { key: "cluster", label: "Cluster" },
              { key: "stores", label: "Tiendas" },
              {
                key: "revenue",
                label: "Ventas",
                render: (value) => formatCurrency(value),
              },
              {
                key: "avg_fill_rate",
                label: "Fill rate promedio",
                render: (value) => `${(value * 100).toFixed(1)}%`,
              },
            ]}
            rows={data.clusters}
          />
        </SectionCard>
      </div>
    </div>
  );
}
