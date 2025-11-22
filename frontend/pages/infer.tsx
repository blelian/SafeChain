import { useState } from "react";
import { authClient } from "../lib/authClient";

export default function InferPage() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<any>(null);
  const [err, setErr] = useState<string | null>(null);

  const run = async () => {
    setErr(null);

    // Convert comma-separated string to numbers
    const nums = input
      .split(",")
      .map(s => parseFloat(s.trim()))
      .filter(n => !Number.isNaN(n));

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/infer`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authClient.authHeader() },
        body: JSON.stringify({ input: nums }),
      });

      if (!res.ok) {
        if (res.status === 401) setErr("Unauthorized - login required");
        else setErr(`Error: ${res.status}`);
        return;
      }

      const data = await res.json();
      setResult(data);
    } catch (e) {
      setErr("Network error");
      console.error(e);
    }
  };

  return (
    <main style={{ padding: 24 }}>
      <h1>AI Inference</h1>
      <div>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="1,2,3"
        />
        <button onClick={run} style={{ marginLeft: 8 }}>Run</button>
        <button onClick={() => { authClient.logout(); setResult(null); }} style={{ marginLeft: 8 }}>
          Logout
        </button>
      </div>
      {err && <p style={{ color: "red" }}>{err}</p>}
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </main>
  );
}
