import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ShieldCheck } from "lucide-react";
import { useAuth } from "../hooks/useAuth";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      await login(form.username, form.password);
      navigate("/");
    } catch (err) {
      setError("No fue posible iniciar sesión. Revisa usuario y contraseña.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-hero">
        <div className="brand-mark big">
          <span>B</span>
          <span>BB</span>
        </div>
        <h1>Retail analytics</h1>
        <p>
          
          Esta cosa es para el hackaton de 3B. Es un dashboard de analítica para retail, con métricas, forecasting y exportaciones para storytelling.
        </p>

        <div className="highlight-box">
          <ShieldCheck size={18} />
          Acceso seguro a métricas, forecasting y exportaciones para storytelling.
        </div>
      </div>

      <form className="login-card" onSubmit={onSubmit}>
        <h2>Iniciar sesión</h2>
        <p>Usa un superusuario de Django o un usuario interno.</p>

        <label>
          Usuario
          <input
            value={form.username}
            onChange={(event) =>
              setForm((prev) => ({ ...prev, username: event.target.value }))
            }
            placeholder="admin"
          />
        </label>

        <label>
          Contraseña
          <input
            type="password"
            value={form.password}
            onChange={(event) =>
              setForm((prev) => ({ ...prev, password: event.target.value }))
            }
            placeholder="••••••••"
          />
        </label>

        {error ? <div className="error-box">{error}</div> : null}

        <button className="primary-button" disabled={loading}>
          {loading ? "Entrando..." : "Entrar al dashboard"}
        </button>
      </form>
    </div>
  );
}
