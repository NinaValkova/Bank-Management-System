import React, { useState } from "react";
import { Card, Form, Button } from "react-bootstrap";
import { useNavigate, Link } from "react-router-dom";
import http from "../api/http";
import { useAuth } from "../context/AuthContext";

export default function UserAuthPage({ mode }) {
  const isLogin = mode === "login";
  const navigate = useNavigate();
  const auth = useAuth();

  const [form, setForm] = useState({
    first_name: "",
    second_name: "",
    birth_date: "",
    email: "",
    username: "",
    password: "",
  });

  const onChange = (k) => (e) => setForm((p) => ({ ...p, [k]: e.target.value }));

  const submit = async () => {
    try {
      if (isLogin) {
        const res = await http.post("/api/user/login", {
          username: form.username,
          password: form.password,
        });
        const token = res.data?.access_token;
        if (!token) {
          alert("Login failed (no token returned).");
          return;
        }
        auth.saveToken(token);
        navigate("/app");
      } else {
        const res = await http.post("/api/user/register", {
          first_name: form.first_name,
          second_name: form.second_name,
          username: form.username,
          email: form.email,
          password: form.password,
          birth_date: form.birth_date || null,
        });

        // your backend returns {message, account_number}, 201
        const msg = res.data?.message || "Registered";
        const acct = res.data?.account_number;
        alert(acct ? `${msg}\nAccount: ${acct}` : msg);

        navigate("/user/login");
      }
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
          <h3 className="text-center mb-3">{isLogin ? "User Login" : "User Register"}</h3>

          {!isLogin && (
            <>
              <Form.Group className="mb-2">
                <Form.Label>First Name</Form.Label>
                <Form.Control value={form.first_name} onChange={onChange("first_name")} />
              </Form.Group>

              <Form.Group className="mb-2">
                <Form.Label>Second Name</Form.Label>
                <Form.Control value={form.second_name} onChange={onChange("second_name")} />
              </Form.Group>

              <Form.Group className="mb-2">
                <Form.Label>Birth Date (optional)</Form.Label>
                <Form.Control type="date" value={form.birth_date} onChange={onChange("birth_date")} />
              </Form.Group>

              <Form.Group className="mb-2">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" value={form.email} onChange={onChange("email")} />
              </Form.Group>
            </>
          )}

          <Form.Group className="mb-2">
            <Form.Label>Username</Form.Label>
            <Form.Control value={form.username} onChange={onChange("username")} />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" value={form.password} onChange={onChange("password")} />
          </Form.Group>

          <div className="d-flex justify-content-center btn-row">
            <Button onClick={submit}>{isLogin ? "Login" : "Create"}</Button>

            {isLogin ? (
              <Link className="btn btn-secondary" to="/user/register">
                Register
              </Link>
            ) : (
              <Link className="btn btn-secondary" to="/user/login">
                To Login
              </Link>
            )}
          </div>

          <div className="text-center mt-3">
            <small>
              Admin? <Link to="/admin/login">Go to Admin Login</Link>
            </small>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
}
