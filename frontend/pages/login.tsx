import { useState } from "react";
import { authClient } from "../lib/authClient";
import { useRouter } from "next/router";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleLogin = async () => {
    setError(null);
    const success = await authClient.login(email, password);
    if (success) {
      router.push("/infer");
    } else {
      setError("Login failed");
    }
  };

  const handleRegister = async () => {
    setError(null);
    const success = await authClient.register(email, password);
    if (success) {
      // Auto-login after registration
      await handleLogin();
    } else {
      setError("Registration failed (maybe email already exists)");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await handleLogin();
  };

  return (
    <main style={{ padding: 24 }}>
      <h1>Login / Register</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email</label><br/>
          <input value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div style={{ marginTop: 8 }}>
          <label>Password</label><br/>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div>
        <div style={{ marginTop: 12 }}>
          <button type="submit">Login</button>
          <button type="button" onClick={handleRegister} style={{ marginLeft: 8 }}>
            Register
          </button>
        </div>
        {error && <p style={{ color: "red" }}>{error}</p>}
      </form>
    </main>
  );
}
