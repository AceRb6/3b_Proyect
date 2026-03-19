import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export function RevenueVsPreviousChart({ data = [] }) {
  return (
    <div className="chart-box">
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" />
          <XAxis dataKey="month" stroke="#c2c8ce" />
          <YAxis stroke="#c2c8ce" />
          <Tooltip />
          <Legend />
          <Bar dataKey="revenue" name="Año actual" fill="#e20a19" radius={[8, 8, 0, 0]} />
          <Bar dataKey="revenue_prev" name="Año anterior" fill="#7c8188" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function ForecastChart({ history = [], forecast = [] }) {
  const merged = [
    ...history.map((item) => ({ ...item, type: "Histórico" })),
    ...forecast.map((item) => ({ ...item, type: "Forecast" })),
  ];

  return (
    <div className="chart-box">
      <ResponsiveContainer width="100%" height={360}>
        <LineChart data={merged}>
          <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" />
          <XAxis dataKey="date" stroke="#c2c8ce" />
          <YAxis stroke="#c2c8ce" />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="value"
            name="Ventas"
            stroke="#e20a19"
            strokeWidth={3}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
