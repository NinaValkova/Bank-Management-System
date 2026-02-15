import React from "react";
import { Link, useNavigate } from "react-router-dom";
import http from "../api/http";
import { useAuth } from "../context/AuthContext";

export default function AppNavbar() {
  const auth = useAuth();
  const navigate = useNavigate();

  const logout = async () => {
    try {
      if (auth.isAdmin) {
        await http.post("/api/admin/logout");
      } else {
        await http.post("/api/user/logout");
      }
    } catch {
      // ignore
    }

    auth.clearToken();
    navigate("/user/login");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-3">
      <Link className="navbar-brand" to="/">
        Banking App
      </Link>

      <div className="ms-auto d-flex gap-2">
        {!auth.isLoggedIn && (
          <>
            <Link className="btn btn-outline-light btn-sm" to="/user/login">
              User Login
            </Link>
            <Link className="btn btn-outline-light btn-sm" to="/admin/login">
              Admin Login
            </Link>
          </>
        )}

        {auth.isLoggedIn && (
          <button className="btn btn-outline-light btn-sm" onClick={logout}>
            Logout
          </button>
        )}
      </div>
    </nav>
  );
}
