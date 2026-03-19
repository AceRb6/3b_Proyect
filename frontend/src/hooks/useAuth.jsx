import { createContext, useContext, useMemo, useState } from "react";
import { api } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("bb_token"));
  const [user, setUser] = useState(
    JSON.parse(localStorage.getItem("bb_user") || "null")
  );

  const login = async (username, password) => {
    const response = await api.post("/auth/login/", { username, password });
    const { token: authToken, user: authUser } = response.data;

    localStorage.setItem("bb_token", authToken);
    localStorage.setItem("bb_user", JSON.stringify(authUser));
    setToken(authToken);
    setUser(authUser);
  };

  const logout = async () => {
    try {
      if (token) {
        await api.post(
          "/auth/logout/",
          {},
          { headers: { Authorization: `Token ${token}` } }
        );
      }
    } catch (error) {
      console.warn("No se pudo cerrar la sesión en servidor", error);
    }
    localStorage.removeItem("bb_token");
    localStorage.removeItem("bb_user");
    setToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({
      token,
      user,
      login,
      logout,
    }),
    [token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
