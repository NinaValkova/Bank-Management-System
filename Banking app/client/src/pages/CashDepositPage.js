import { useState } from "react";
import { Card, Form, Button } from "react-bootstrap";
import http from "../api/http";

export default function CashDepositPage() {
  const [amount, setAmount] = useState("");

  const submit = async () => {
    try {
      const res = await http.post("/api/user/cash-deposit", {
        amount,
      });

      alert(res.data?.message || "Deposit successful");
      setAmount("");
    } catch (err) {
      alert(err?.response?.data?.message || "Deposit failed");
    }
  };

  return (
    <div className="bank-center-inner">
      <Card style={{ width: "26rem" }}>
        <Card.Body>
          <h4 className="text-center mb-3">Cash Deposit</h4>

          <Form.Group className="mb-3">
            <Form.Label>Amount</Form.Label>
            <Form.Control
              type="number"
              step="0.01"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />
          </Form.Group>

          <div className="d-flex justify-content-center">
            <Button onClick={submit}>Deposit</Button>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
}
