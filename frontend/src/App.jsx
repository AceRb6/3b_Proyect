import { Navigate, Route, Routes } from "react-router-dom";
import AppShell from "./layout/AppShell";
import LoginPage from "./pages/LoginPage";
import HomePage from "./pages/HomePage";
import DashboardPage from "./pages/DashboardPage";
import StoresPage from "./pages/StoresPage";
import ForecastPage from "./pages/ForecastPage";
import ExportsPage from "./pages/ExportsPage";
import { AuthProvider, useAuth } from "./hooks/useAuth";

function ProtectedRoute({ children }) {
  const { token } = useAuth();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function RoutedApp() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route index element={<HomePage />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="tiendas" element={<StoresPage />} />
        <Route path="forecast" element={<ForecastPage />} />
        <Route path="descargas" element={<ExportsPage />} />
      </Route>
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <RoutedApp />
    </AuthProvider>
  );
}
