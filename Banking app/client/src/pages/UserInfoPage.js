import { useEffect, useState } from "react";
import http from "../api/http";

export default function UserInfoPage() {
  const [u, setU] = useState(null);

  useEffect(() => {
    (async () => {
      const res = await http.get("/api/user/user-info");
      setU(res.data);
    })();
  }, []);

  if (!u) {
    return (
      <div className="bank-center-inner">
        <div className="bank-center-text">LOADING...</div>
      </div>
    );
  }

  return (
    <div className="bank-center-inner">
      <div className="user-info-card">
        <h4>User Information</h4>
        <div><b>First Name:</b> {u.first_name}</div>
        <div><b>Second Name:</b> {u.second_name}</div>
        <div><b>Email:</b> {u.email}</div>
        <div><b>Birth Number:</b> {u.birth_number || "-"}</div>
        <div style={{ marginTop: 12 }}>
          <b>Balance:</b> {u.balance}
        </div>
      </div>
    </div>
  );
}
