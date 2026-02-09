import React, { useEffect, useState } from "react";
import http from "../api/http";

export default function BalancePage() {
  const [data, setData] = useState({ balance: "", currency: "EUR" });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await http.get("/api/user/user-balance");
        setData({
          balance: res.data?.balance ?? "0.00",
          currency: res.data?.currency ?? "EUR",
        });
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div className="bank-center-inner">
      <div className="bank-center-text">
        {loading ? "LOADING..." : `CURRENT BALANCE : ${data.balance} ${data.currency}`}
      </div>
    </div>
  );
}
