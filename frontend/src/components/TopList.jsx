function formatCurrency(value) {
  return new Intl.NumberFormat("es-MX", {
    style: "currency",
    currency: "MXN",
    maximumFractionDigits: 0,
  }).format(value || 0);
}

export default function TopList({
  items = [],
  primaryKey,
  titleKey,
  subtitleKey,
  valueKey,
  valueFormatter = (value) => value,
}) {
  return (
    <div className="top-list">
      {items.map((item, index) => (
        <div className="top-item" key={item[primaryKey] || index}>
          <div className="top-rank">{String(index + 1).padStart(2, "0")}</div>
          <div>
            <div className="top-title">{item[titleKey]}</div>
            {subtitleKey ? <small>{item[subtitleKey]}</small> : null}
          </div>
          <strong>
            {valueFormatter === "currency"
              ? formatCurrency(item[valueKey])
              : valueFormatter(item[valueKey])}
          </strong>
        </div>
      ))}
    </div>
  );
}
