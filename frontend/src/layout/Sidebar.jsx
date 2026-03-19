import { LayoutDashboard, MapPinned, PackageSearch, TrendingUp, Download, LogOut } from "lucide-react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const items = [
  { to: "/", label: "Inicio", icon: LayoutDashboard },
  { to: "/dashboard", label: "Dashboard", icon: PackageSearch },
  { to: "/tiendas", label: "Tiendas", icon: MapPinned },
  { to: "/forecast", label: "Forecast", icon: TrendingUp },
  { to: "/descargas", label: "Descargas", icon: Download },
];

export default function Sidebar() {
  const { logout } = useAuth();

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">
          <span>B</span>
          <span>BB</span>
        </div>
        <div>
          <strong>BB Retail</strong>
          <small>Analytics Suite</small>
        </div>
      </div>

      <nav className="nav-menu">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              <Icon size={18} />
              {item.label}
            </NavLink>
          );
        })}
      </nav>

      <button className="ghost-button logout" onClick={logout}>
        <LogOut size={16} />
        Cerrar sesión
      </button>
    </aside>
  );
}
