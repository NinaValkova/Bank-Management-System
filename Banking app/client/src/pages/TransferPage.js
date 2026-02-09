import React, { useState } from "react";
import { Card, Form, Button } from "react-bootstrap";
import http from "../api/http";

export default function TransferPage() {
  const [tx, setTx] = useState({
    to_account: "",
    amount: "",
    currency: "EUR",
  });

  const onChange = (k) => (e) => setTx((p) => ({ ...p, [k]: e.target.value }));

  const submit = async () => {
    try {
      const res = await http.post("/api/user/transfer", {
        to_account: tx.to_account,
        amount: tx.amount,
        currency: tx.currency || "EUR",
      });

      alert(res.data?.message || "Transfer done");
      setTx({ to_account: "", amount: "", currency: "EUR" });
    } catch (err) {
      const msg =
        err?.response?.data?.message ||
        err?.response?.data?.error ||
        "Transfer failed";
      alert(msg);
    }
  };

  return (
    <div className="page-wrap">
      <Card style={{ width: "36rem" }}>
        <Card.Body>
          <h3 className="text-center mb-3">Send Money</h3>

          <Form.Group className="mb-2">
            <Form.Label>To Account</Form.Label>
            <Form.Control value={tx.to_account} onChange={onChange("to_account")} />
          </Form.Group>

          <Form.Group className="mb-2">
            <Form.Label>Amount</Form.Label>
            <Form.Control type="number" step="0.01" value={tx.amount} onChange={onChange("amount")} />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Currency</Form.Label>
            <Form.Control value={tx.currency} onChange={onChange("currency")} />
          </Form.Group>

          <div className="d-flex justify-content-center">
            <Button onClick={submit}>Transfer</Button>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
}
