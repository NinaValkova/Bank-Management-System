import React, { createContext, useContext, useMemo, useState } from "react";
import { getRoleFromToken } from "../utils/jwt";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("access_token") || "");

  const role = useMemo(() => {
    if (!token) return null;
    return getRoleFromToken(token); // "admin" or null
  }, [token]);

  const isLoggedIn = !!token;
  const isAdmin = role === "admin";

  function saveToken(newToken) {
    localStorage.setItem("access_token", newToken);
    setToken(newToken);
  }

  function clearToken() {
    localStorage.removeItem("access_token");
    setToken("");
  }

  const value = {
    token,
    role,
    isLoggedIn,
    isAdmin,
    saveToken,
    clearToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
