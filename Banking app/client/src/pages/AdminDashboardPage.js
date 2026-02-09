import React, { useEffect, useState } from "react";
import { Card, Table, Button } from "react-bootstrap";
import http from "../api/http";

export default function AdminDashboardPage() {
  const [users, setUsers] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [txs, setTxs] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadAll = async () => {
    setLoading(true);
    try {
      const [uRes, aRes, tRes] = await Promise.all([
        http.get("/api/admin/users"),
        http.get("/api/admin/accounts"),
        http.get("/api/admin/transactions"),
      ]);

      setUsers(uRes.data || []);
      setAccounts(aRes.data || []);
      setTxs(tRes.data || []);
    } catch (err) {
      const msg = err?.response?.data?.message || "Failed to load admin data";
      alert(msg);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, []);

  return (
    <div className="container py-4">
      <Card className="mb-3">
        <Card.Body className="d-flex justify-content-between align-items-center">
          <h3 className="m-0">Admin Dashboard</h3>
        </Card.Body>
      </Card>

      <Card className="mb-4">
        <Card.Body>
          <h5>Users</h5>
          <div style={{ overflowX: "auto" }}>
            <Table striped bordered hover size="sm">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>First</th>
                  <th>Second</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Birth</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id}>
                    <td>{u.id}</td>
                    <td>{u.first_name}</td>
                    <td>{u.second_name}</td>
                    <td>{u.username}</td>
                    <td>{u.email}</td>
                    <td>{u.birth_number}</td>
                    <td>{u.created_at}</td>
                  </tr>
                ))}
                {users.length === 0 && (
                  <tr>
                    <td colSpan="7" className="text-center">
                      No users
                    </td>
                  </tr>
                )}
              </tbody>
            </Table>
          </div>
        </Card.Body>
      </Card>

      <Card className="mb-4">
        <Card.Body>
          <h5>Accounts</h5>
          <div style={{ overflowX: "auto" }}>
            <Table striped bordered hover size="sm">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Account Number</th>
                  <th>Balance</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {accounts.map((a) => (
                  <tr key={a.id}>
                    <td>{a.id}</td>
                    <td>{a.account_number}</td>
                    <td>{a.balance}</td>
                    <td>{a.created_at}</td>
                  </tr>
                ))}
                {accounts.length === 0 && (
                  <tr>
                    <td colSpan="4" className="text-center">
                      No accounts
                    </td>
                  </tr>
                )}
              </tbody>
            </Table>
          </div>
        </Card.Body>
      </Card>

      <Card className="mb-4">
        <Card.Body>
          <h5>Transactions</h5>
          <div style={{ overflowX: "auto" }}>
            <Table striped bordered hover size="sm">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Account ID</th>
                  <th>From</th>
                  <th>To</th>
                  <th>Amount</th>
                  <th>Balance</th>
                  <th>Currency</th>
                  <th>Type</th>
                  <th>Operation</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {txs.map((t) => (
                  <tr key={t.id}>
                    <td>{t.id}</td>
                    <td>{t.account_id}</td>
                    <td>{t.from_account}</td>
                    <td>{t.to_account}</td>
                    <td>{t.amount}</td>
                    <td>{t.balance}</td>
                    <td>{t.currency}</td>
                    <td>{t.type}</td>
                    <td>{t.operation}</td>
                    <td>{t.date}</td>
                  </tr>
                ))}
                {txs.length === 0 && (
                  <tr>
                    <td colSpan="10" className="text-center">
                      No transactions
                    </td>
                  </tr>
                )}
              </tbody>
            </Table>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
}
