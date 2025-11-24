import { useState } from "react";

export default function RustDemoButton() {
  const [output, setOutput] = useState<string | null>(null);

  const fetchRustOutput = async () => {
    try {
      const RUST_API_URL = process.env.NEXT_PUBLIC_RUST_API_URL || "http://localhost:9000"; // Rust backend URL
      const res = await fetch(`${RUST_API_URL}/demo`); // <-- fetch endpoint from Rust backend
      const data = await res.json();
      setOutput(data.message || JSON.stringify(data));
    } catch (err) {
      setOutput("Rust backend not reachable");
    }
  };

  return (
    <div className="mt-6 text-center">
      <button
        onClick={fetchRustOutput}
        className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 rounded-lg font-semibold"
      >
        Show Rust Output
      </button>

      {output && (
        <div className="mt-4 p-3 bg-black/20 rounded text-gray-200">
          {output}
        </div>
      )}
    </div>
  );
}
