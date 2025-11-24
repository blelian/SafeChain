import { useState } from "react";
import { authClient } from "../lib/authClient";

type BackendResult = {
  password?: string;
  strength?: string;
  reasons?: string[];
  suggestions?: string[];
};

export default function InferPage() {
  const [password, setPassword] = useState("");
  const [result, setResult] = useState<BackendResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_FASTAPI_URL || "http://localhost:8000";

  const heuristic = (pw: string): BackendResult => {
    if (!pw) return { strength: undefined };
    if (pw.length < 8)
      return { strength: "weak", reasons: ["Too short"], suggestions: ["Make it longer"] };
    if (pw.length < 12)
      return { strength: "medium", reasons: ["Short length"], suggestions: ["Consider using 12+ characters"] };
    return { strength: "strong", reasons: [], suggestions: ["Looks good — use a passphrase or password manager"] };
  };

  const check = async () => {
    setErr(null);
    setLoading(true);
    setResult(heuristic(password));

    try {
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      const ah = authClient.authHeader();
      if (ah.Authorization) headers.Authorization = ah.Authorization;

      const res = await fetch(`${API_URL}/api/password/check`, {
        method: "POST",
        headers,
        body: JSON.stringify({ password, user_id: null }),
      });

      if (!res.ok) {
        const txt = await res.text().catch(() => "");
        setErr(`Server error ${res.status}`);
        console.error("[Infer] server error:", res.status, txt);
        return;
      }

      const data: BackendResult = await res.json();
      setResult(data);
    } catch (e: any) {
      console.error("[Infer] network/error:", e);
      setErr("Network error (check console & server)");
    } finally {
      setLoading(false);
    }
  };

  const getStrengthBarStyle = (): React.CSSProperties => {
    if (!result?.strength)
      return { width: "0%", background: "linear-gradient(to right, #94a3b8, #64748b)" };
    const s = String(result.strength).toLowerCase();
    switch (s) {
      case "weak":
        return { width: "33%", background: "linear-gradient(to right, #f87171, #f43f5e)" };
      case "medium":
        return { width: "66%", background: "linear-gradient(to right, #facc15, #fbbf24)" };
      case "strong":
        return { width: "100%", background: "linear-gradient(to right, #4ade80, #16a34a)" };
      default:
        return { width: "0%", background: "linear-gradient(to right, #94a3b8, #64748b)" };
    }
  };

  return (
    <div className="page-container bg-gradient-to-br from-gray-900 via-emerald-900 to-gray-800 p-4">
      <div className="card text-center max-w-2xl p-6 md:p-10 space-y-6">
        <h1 className="text-3xl md:text-4xl font-extrabold mb-4 text-emerald-300">
          SafeChain — Password Tester
        </h1>
        <p className="text-sm text-gray-300 mb-6">
          Real AI-powered feedback. Strength meter updates in real-time.
        </p>

        {/* Input */}
        <div className="mb-4">
          <label className="block text-xs text-gray-300 mb-2">Enter password</label>
          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="password"
              placeholder="Type a password to test..."
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="flex-1 min-w-0 p-3 rounded-lg bg-white/5 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-400"
            />
            <button
              onClick={check}
              disabled={loading || password.length === 0}
              className="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-600 font-semibold transition-all disabled:opacity-50"
            >
              {loading ? "Checking..." : "Check"}
            </button>
          </div>
        </div>

        {/* Strength bar */}
        <div className="mb-4">
          <div className="h-4 rounded-full overflow-hidden bg-black/30 border border-black/40">
            <div className="h-4 transition-all duration-700" style={getStrengthBarStyle()} />
          </div>
          <div className="flex items-center justify-between text-xs text-gray-300 mt-2">
            <span>
              Strength: <b className="text-white ml-1">{result?.strength ?? "—"}</b>
            </span>
            <span>{result ? `${result.reasons?.length ?? 0} issues` : ""}</span>
          </div>
        </div>

        {/* Suggestions & Reasons */}
        <div className="grid md:grid-cols-2 gap-4 mb-4">
          <div className="p-4 rounded-lg bg-white/5">
            <h3 className="text-sm font-semibold mb-2">Reasons</h3>
            <ul className="list-disc list-inside text-sm text-gray-200">
              {result?.reasons?.length
                ? result.reasons.map((r, i) => <li key={i}>{r}</li>)
                : <li className="text-gray-500">No issues identified yet</li>}
            </ul>
          </div>
          <div className="p-4 rounded-lg bg-white/5">
            <h3 className="text-sm font-semibold mb-2">Suggestions</h3>
            <ul className="list-disc list-inside text-sm text-gray-200">
              {result?.suggestions?.length
                ? result.suggestions.map((s, i) => <li key={i}>{s}</li>)
                : <li className="text-gray-500">Type a password and press Check</li>}
            </ul>
          </div>
        </div>

        {/* Raw response */}
        <div className="mt-4">
          <details className="text-sm text-gray-300">
            <summary className="cursor-pointer">Show raw response</summary>
            <pre className="mt-2 p-3 bg-black/50 rounded text-xs text-gray-200 overflow-auto">
              {result ? JSON.stringify(result, null, 2) : "—"}
            </pre>
          </details>
        </div>

        {err && <p className="mt-4 text-red-400">{err}</p>}

        {/* Rust demo */}
        <div className="mt-6">
          <h2 className="text-sm text-gray-300 mb-2 font-semibold">Rust Backend Demo</h2>
          <RustDemoButton />
        </div>

        {/* Footer */}
        <div className="mt-6 flex gap-3 justify-center">
          <button
            onClick={() => {
              setPassword("");
              setResult(null);
            }}
            className="px-4 py-2 rounded-lg bg-gray-700 hover:bg-gray-600"
          >
            Clear
          </button>
          <button
            onClick={() => {
              authClient.logout();
              window.location.href = "/login";
            }}
            className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-500"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}

// RustDemoButton Component
export function RustDemoButton() {
  const [output, setOutput] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchRustOutput = async () => {
    setLoading(true);
    setOutput(null);
    try {
      const RUST_API_URL = process.env.NEXT_PUBLIC_RUST_URL || "https://rust-service-e4hc.onrender.com";
      const res = await fetch(RUST_API_URL, { method: "GET", headers: { "Content-Type": "application/json" } });
      if (!res.ok) {
        setOutput(`Error: ${res.status}`);
      } else {
        const text = await res.text();
        try {
          const data = JSON.parse(text);
          setOutput(data.message || JSON.stringify(data));
        } catch {
          setOutput(text);
        }
      }
    } catch (err) {
      console.error("[RustDemo] Error:", err);
      setOutput("Rust backend not reachable (check console)");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-6 text-center">
      <button
        onClick={fetchRustOutput}
        className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 rounded-lg font-semibold"
        disabled={loading}
      >
        {loading ? "Fetching..." : "Show Rust Output"}
      </button>

      {output && (
        <div className="mt-4 p-3 bg-black/20 rounded text-gray-200 break-words">
          {output}
        </div>
      )}
    </div>
  );
}
