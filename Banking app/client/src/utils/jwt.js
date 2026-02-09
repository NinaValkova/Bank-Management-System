export function decodeJwt(token) {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;

    const payload = parts[1]
      .replace(/-/g, "+")
      .replace(/_/g, "/");

    const decoded = JSON.parse(atob(payload));
    return decoded;
  } catch {
    return null;
  }
}

export function getRoleFromToken(token) {
  const payload = decodeJwt(token);
  return payload?.role || null; // admin token has { role: "admin" }
}
