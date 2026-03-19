import { TrendingUp } from "lucide-react";

function formatMetric(value, format) {
  if (format === "currency") {
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
      maximumFractionDigits: 0,
    }).format(value);
  }
  if (format === "percent") {
    return `${Number(value).toFixed(1)}%`;
  }
  return new Intl.NumberFormat("es-MX").format(value);
}

export default function MetricCard({ label, value, format, helper }) {
  return (
    <div className="metric-card">
      <div className="metric-top">
        <span>{label}</span>
        <TrendingUp size={18} />
      </div>
      <strong>{formatMetric(value, format)}</strong>
      {helper ? <small>{helper}</small> : null}
    </div>
  );
}
