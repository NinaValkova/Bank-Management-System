import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ requireAdmin = false }) {
  const auth = useAuth();

  if (!auth.isLoggedIn) {
    return <Navigate to="/user/login" replace />;
  }

  if (requireAdmin && !auth.isAdmin) {
    return <Navigate to="/user/login" replace />;
  }

  return <Outlet />;
}
