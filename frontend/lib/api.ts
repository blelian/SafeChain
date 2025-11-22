// frontend/lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function apiRequest(path: string, init?: RequestInit) {
  const res = await fetch(`${API_URL}${path}`, {
    credentials: "include",
    ...init,
  });

  const text = await res.text();
  let payload: any = text;
  try { payload = text ? JSON.parse(text) : null; } catch(e) { /* not json */ }

  if (!res.ok) {
    const err = new Error(`API ${res.status}: ${text || res.statusText}`);
    // @ts-ignore
    err.status = res.status;
    // @ts-ignore
    err.payload = payload;
    throw err;
  }

  return payload;
}

export function apiGet(path: string, headers: Record<string,string> = {}) {
  return apiRequest(path, { method: "GET", headers: { "Content-Type": "application/json", ...headers } });
}

export function apiPost(path: string, body: any, headers: Record<string,string> = {}) {
  return apiRequest(path, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...headers },
    body: JSON.stringify(body),
  });
}
