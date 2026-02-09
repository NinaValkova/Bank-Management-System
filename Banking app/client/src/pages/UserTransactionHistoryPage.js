import { useEffect, useState } from "react";
import http from "../api/http";
import { Table, Form } from "react-bootstrap";

export default function UserTransactionHistoryPage() {
  const [txs, setTxs] = useState([]);
  const [loading, setLoading] = useState(true);

  // NEW: sort order state
  const [sortOrder, setSortOrder] = useState("desc"); // "desc" = newest first
  // Optional: operation filter if you want to use it too
  // const [operation, setOperation] = useState("");

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        params.set("sort", sortOrder);
        // if (operation) params.set("operation", operation);

        const res = await http.get(`/api/user/transactions?${params.toString()}`);
        setTxs(res.data);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [sortOrder]); // re-fetch whenever sort changes (and operation if you add it)

  if (loading) {
    return (
      <div className="bank-center-inner">
        <div className="bank-center-text">LOADING...</div>
      </div>
    );
  }

  return (
    <div className="bank-center-inner">
      <div style={{ width: "95%" }}>
        <div className="d-flex align-items-center justify-content-between mb-3">
          <h4 className="mb-0">Transaction History</h4>

          {/* NEW: sort UI */}
          <Form.Select
            style={{ width: 220 }}
            size="sm"
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
          >
            <option value="desc">Date: Newest → Oldest</option>
            <option value="asc">Date: Oldest → Newest</option>
          </Form.Select>
        </div>

        <Table striped bordered hover size="sm">
          <thead>
            <tr>
              <th>Date</th>
              <th>Operation</th>
              <th>Type</th>
              <th>From</th>
              <th>To</th>
              <th>Amount</th>
              <th>Balance</th>
            </tr>
          </thead>
          <tbody>
            {txs.length === 0 && (
              <tr>
                <td colSpan="7" className="text-center">
                  No transactions found
                </td>
              </tr>
            )}

            {txs.map((t) => (
              <tr key={t.id}>
                <td>{t.date ? new Date(t.date).toLocaleString() : "-"}</td>
                <td>{t.operation}</td>
                <td>{t.type}</td>
                <td>{t.from_account || "-"}</td>
                <td>{t.to_account || "-"}</td>
                <td>
                  {t.amount} {t.currency}
                </td>
                <td>{t.balance}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    </div>
  );
}
