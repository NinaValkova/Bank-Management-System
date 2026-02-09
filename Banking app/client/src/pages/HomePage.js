import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function HomePage() {
  const auth = useAuth();
  const navigate = useNavigate();

  React.useEffect(() => {
    if (!auth.isLoggedIn) navigate("/user/login", { replace: true });
    else if (auth.isAdmin) navigate("/admin", { replace: true });
    else navigate("/app", { replace: true });
  }, [auth.isLoggedIn, auth.isAdmin, navigate]);

  return null;
}
