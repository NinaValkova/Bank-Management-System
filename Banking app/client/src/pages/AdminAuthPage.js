import React, { useState } from "react";
import { Card, Form, Button } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import http from "../api/http";
import { useAuth } from "../context/AuthContext";

export default function AdminAuthPage() {
  const navigate = useNavigate();
  const auth = useAuth();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const onChange = (k) => (e) => setForm((p) => ({ ...p, [k]: e.target.value }));

  const submit = async () => {
    try {
      const res = await http.post("/api/admin/login", {
        username: form.username,
        password: form.password,
      });

      const token = res.data?.access_token;
      if (!token) {
        alert("Admin login failed (no token returned).");
        return;
      }

      auth.saveToken(token);
      navigate("/admin");
    } catch (err) {
      const msg =
        err?.response?.data?.message ||
        err?.response?.data?.error ||
        "Request failed";
      alert(msg);
    }
  };

  return (
    <div className="page-wrap">
      <Card className="auth-card p-2">
        <Card.Body>
          <h3 className="text-center mb-3">Admin Login</h3>

          <Form.Group className="mb-2">
            <Form.Label>Username</Form.Label>
            <Form.Control value={form.username} onChange={onChange("username")} />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" value={form.password} onChange={onChange("password")} />
          </Form.Group>

          <div className="d-flex justify-content-center btn-row">
            <Button onClick={submit}>Login</Button>
          </div>

          <div className="text-center mt-3">
            <small>
              User? <Link to="/user/login">Go to User Login</Link>
            </small>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
}
