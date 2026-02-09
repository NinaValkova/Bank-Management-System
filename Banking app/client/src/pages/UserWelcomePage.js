import { useEffect, useState } from "react";
import http from "../api/http";

export default function UserWelcomePage() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    (async () => {
      const res = await http.get("/api/user/user-info");
      setUser(res.data);
    })();
  }, []);

  if (!user) {
    return (
      <div className="bank-center-inner">
        <div className="bank-center-text">LOADING...</div>
      </div>
    );
  }

  return (
    <div className="bank-center-inner">
      <div className="welcome-card">
        <h2>Welcome, {user.first_name}!</h2>
      </div>
    </div>
  );
}
