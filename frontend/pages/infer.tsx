// frontend/pages/infer.tsx
import { useState } from "react";
import { authClient } from "../lib/authClient";
import RustDemoButton from "../components/rust_demo"; // <-- import Rust demo component

const strengthColor = {
  weak: "from-red-500 to-rose-500",
  medium: "from-amber-400 to-yellow-500",
  strong: "from-emerald-400 to-green-600",
  unknown: "from-slate-400 to-slate-600",
};

export default function InferPage() {
  const [password, setPassword] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const check = async () => {
    setErr(null);
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch(`${API_URL}/api/password/check`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authClient.authHeader(),
        },
        body: JSON.stringify({ password, user_id: null }),
      });

      if (!res.ok) {
        setErr(`Server error ${res.status}`);
        setLoading(false);
        return;
      }

      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
      setErr("Network error");
    } finally {
      setLoading(false);
    }
  };

  const colorClass =
    result?.strength ? strengthColor[result.strength] ?? strengthColor.unknown : "from-slate-300 to-slate-500";

  return (
    <div className="page-container bg-gradient-to-br from-gray-900 via-emerald-900 to-gray-800 p-4">
      <div className="card text-center max-w-2xl p-6 md:p-10 space-y-6">
        <h1 className="text-3xl md:text-4xl font-extrabold mb-4 text-emerald-300">SafeChain — Password Tester</h1>
        <p className="text-sm text-gray-300 mb-6">Real AI-powered feedback. Strength meter updates in real-time.</p>

        {/* Password Input */}
        <div className="mb-4">
          <label className="block text-xs text-gray-300 mb-2">Enter password</label>
          <div className="flex gap-2">
            <input
              className="flex-1 p-3 rounded-lg bg-white/5 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-400"
              placeholder="Type a password to test..."
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
            />
            <button
              onClick={check}
              className="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-600 font-semibold transition-all disabled:opacity-50"
              disabled={loading || password.length === 0}
            >
              {loading ? "Checking..." : "Check"}
            </button>
          </div>
        </div>

        {/* Strength Bar */}
        <div className="mb-4">
          <div className="h-4 rounded-full overflow-hidden bg-black/30 border border-black/40">
            <div
              className={`h-4 transition-all duration-700 bg-gradient-to-r ${colorClass}`}
              style={{
                width: result
                  ? result.strength === "weak"
                    ? "33%"
                    : result.strength === "medium"
                    ? "66%"
                    : "100%"
                  : "0%",
              }}
            />
          </div>
          <div className="flex items-center justify-between text-xs text-gray-300 mt-2">
            <span>
              Strength: <b className="text-white ml-1">{result?.strength ?? "—"}</b>
            </span>
            <span>{result ? `${result.reasons?.length ?? 0} issues` : ""}</span>
          </div>
        </div>

        {/* Suggestions and Reasons */}
        <div className="grid md:grid-cols-2 gap-4 mb-4">
          <div className="p-4 rounded-lg bg-white/5">
            <h3 className="text-sm font-semibold mb-2">Reasons</h3>
            <ul className="list-disc list-inside text-sm text-gray-200">
              {result?.reasons?.length
                ? result.reasons.map((r: string, i: number) => <li key={i}>{r}</li>)
                : <li className="text-gray-500">No issues identified yet</li>}
            </ul>
          </div>
          <div className="p-4 rounded-lg bg-white/5">
            <h3 className="text-sm font-semibold mb-2">Suggestions</h3>
            <ul className="list-disc list-inside text-sm text-gray-200">
              {result?.suggestions?.length
                ? result.suggestions.map((s: string, i: number) => <li key={i}>{s}</li>)
                : <li className="text-gray-500">Type a password and press Check</li>}
            </ul>
          </div>
        </div>

        {/* Raw result */}
        <div className="mt-4">
          <details className="text-sm text-gray-300">
            <summary className="cursor-pointer">Show raw response</summary>
            <pre className="mt-2 p-3 bg-black/50 rounded text-xs text-gray-200 overflow-auto">
              {result ? JSON.stringify(result, null, 2) : "—"}
            </pre>
          </details>
        </div>

        {err && <p className="mt-4 text-red-400">{err}</p>}

        {/* Rust Demo Component */}
        <div className="mt-6">
          <RustDemoButton />
        </div>

        {/* Footer Buttons */}
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
