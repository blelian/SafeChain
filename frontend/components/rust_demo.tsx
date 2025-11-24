// frontend/components/rust_demo.tsx
import { useState } from "react";

export default function RustDemoButton() {
  const [output, setOutput] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchRustOutput = async () => {
    setLoading(true);
    setOutput(null);
    try {
      // Minimal Rust backend URL
      const RUST_API_URL = process.env.NEXT_PUBLIC_RUST_API_URL || "http://localhost:9000";
      
      const res = await fetch(RUST_API_URL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!res.ok) {
        setOutput(`Error: ${res.status}`);
      } else {
        const text = await res.text();
        // Minimal backend returns raw JSON string, parse it safely
        try {
          const data = JSON.parse(text);
          setOutput(data.message || JSON.stringify(data));
        } catch {
          setOutput(text); // fallback if not valid JSON
        }
      }
    } catch (err) {
      console.error(err);
      setOutput("Rust backend not reachable");
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
