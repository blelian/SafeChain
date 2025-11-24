import { useState, useEffect } from "react";
import { authClient } from "../lib/authClient";
import { useRouter } from "next/router";

export default function LoginPage() {
  console.log("LoginPage — v2 loaded"); // marker to confirm deployed bundle

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  // optional: if user already logged in, redirect (keeps behaviour)
  useEffect(() => {
    if (typeof window !== "undefined" && authClient.getToken()) {
      router.push("/infer");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleLogin = async () => {
    setLoading(true);
    setError(null);
    const { success, message } = await authClient.login(email, password) as any;
    setLoading(false);
    if (success || success === true) router.push("/infer");
    else setError(message || "Login failed");
  };

  const handleRegister = async () => {
    setLoading(true);
    setError(null);
    const { success, message } = await authClient.register(email, password) as any;
    setLoading(false);
    if (success) await handleLogin();
    else setError(message || "Registration failed (maybe email already exists)");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await handleLogin();
  };

  return (
    <div className="page-container bg-gradient-to-br from-gray-900 via-emerald-900 to-gray-800 p-4">
      <div className="card max-w-md w-full p-8 space-y-6 text-center">
        <button
          onClick={() => router.push("/")}
          className="text-sm text-emerald-300 hover:underline mb-2 self-start"
        >
          ← Back to Homepage
        </button>

        <h1 className="text-2xl font-bold text-emerald-400 mb-4">Login / Register</h1>

        <form onSubmit={handleSubmit} className="w-full">
          {/* Email */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center mb-3">
            <label className="md:col-span-3 md:text-right text-sm text-gray-300">Email</label>
            <div className="md:col-span-9 min-w-0">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full p-3 rounded-lg bg-black/20 placeholder-gray-400 focus:ring-emerald-400 focus:outline-none min-w-0"
                required
              />
            </div>
          </div>

          {/* Password */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center mb-3">
            <label className="md:col-span-3 md:text-right text-sm text-gray-300">Password</label>
            <div className="md:col-span-9 min-w-0">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full p-3 rounded-lg bg-black/20 placeholder-gray-400 focus:ring-emerald-400 focus:outline-none min-w-0"
                required
              />
            </div>
          </div>

          {/* Buttons */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center mt-4">
            <div className="md:col-start-4 md:col-span-9 flex flex-col sm:flex-row gap-3">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 w-full sm:w-auto py-3 bg-emerald-500 hover:bg-emerald-600 rounded-lg font-semibold transition-all disabled:opacity-50"
              >
                {loading ? "Logging in..." : "Login"}
              </button>
              <button
                type="button"
                onClick={handleRegister}
                disabled={loading}
                className="flex-1 w-full sm:w-auto py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-semibold transition-all disabled:opacity-50"
              >
                {loading ? "Registering..." : "Register"}
              </button>
            </div>
          </div>

          {error && (
            <div className="mt-4 text-center">
              <p className="text-red-500">{error}</p>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
