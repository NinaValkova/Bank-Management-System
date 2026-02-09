import { useState } from "react";
import { Card, Form, Button } from "react-bootstrap";
import http from "../api/http";

export default function HelpSupportPage() {
  const [message, setMessage] = useState("");

  const submit = async () => {
    if (!message.trim()) {
      alert("Please enter a message");
      return;
    }

    try {
      await http.post("/api/user/help-support", { message });
      alert("Message sent to support");
      setMessage("");
    } catch (err) {
      alert(err?.response?.data?.message || "Failed to send message");
    }
  };

  return (
    <div className="bank-center-inner">
      <Card style={{ width: "32rem" }}>
        <Card.Body>
          <h4 className="text-center mb-3">Help & Support</h4>

          <Form.Group className="mb-3">
            <Form.Label>Your message</Form.Label>
            <Form.Control
              as="textarea"
              rows={5}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
          </Form.Group>

          <div className="d-flex justify-content-center">
            <Button onClick={submit}>Send</Button>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
}
