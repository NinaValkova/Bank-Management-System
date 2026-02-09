import { useEffect, useState } from "react";
import { Card, Form, Button } from "react-bootstrap";
import http from "../api/http";

export default function UpdateUserPage() {
  const [form, setForm] = useState({
    first_name: "",
    second_name: "",
    email: "",
    birth_number: "",
  });

  useEffect(() => {
    (async () => {
      const res = await http.get("/api/user/user-info");
      setForm({
        first_name: res.data.first_name || "",
        second_name: res.data.second_name || "",
        email: res.data.email || "",
        birth_number: res.data.birth_number || "",
      });
    })();
  }, []);

  const onChange = (k) => (e) =>
    setForm((p) => ({ ...p, [k]: e.target.value }));

  const submit = async () => {
    try {
      await http.put("/api/user/update-user", form);
      alert("User information updated successfully");
    } catch (err) {
      alert(
        err?.response?.data?.message || "Update failed"
      );
    }
  };

  return (
    <div className="bank-center-inner">
      <Card style={{ width: "28rem" }}>
        <Card.Body>
          <h4 className="text-center mb-3">Update User Information</h4>

          <Form.Group className="mb-2">
            <Form.Label>First Name</Form.Label>
            <Form.Control value={form.first_name} onChange={onChange("first_name")} />
          </Form.Group>

          <Form.Group className="mb-2">
            <Form.Label>Second Name</Form.Label>
            <Form.Control value={form.second_name} onChange={onChange("second_name")} />
          </Form.Group>

          <Form.Group className="mb-2">
            <Form.Label>Email</Form.Label>
            <Form.Control value={form.email} onChange={onChange("email")} />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Birth Number</Form.Label>
            <Form.Control value={form.birth_number} onChange={onChange("birth_number")} />
          </Form.Group>

          <div className="d-flex justify-content-center">
            <Button onClick={submit}>Update</Button>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
}
