import { Bell, Search } from "lucide-react";
import { useAuth } from "../hooks/useAuth";

export default function Topbar() {
  const { user } = useAuth();
  return (
    <header className="topbar">
      <div className="search-box">
        <Search size={18} />
        <input placeholder="Buscar producto, tienda o categoría..." />
      </div>

      <div className="topbar-right">
        <button className="icon-button">
          <Bell size={18} />
        </button>
        <div className="user-chip">
          <span>{user?.full_name?.charAt(0) || "A"}</span>
          <div>
            <strong>{user?.full_name || "Analista"}</strong>
            <small>{user?.email || "dashboard@bb.com"}</small>
          </div>
        </div>
      </div>
    </header>
  );
}
