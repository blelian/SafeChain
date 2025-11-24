const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

let token: string | null = null;

// Load token from localStorage if in browser
if (typeof window !== "undefined") {
  token = localStorage.getItem("token");
  console.log("[authClient] Loaded token from localStorage:", token);
}

export const authClient = {
  register: async (email: string, password: string): Promise<boolean> => {
    try {
      console.log("[authClient] Registering user:", email);
      const res = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const text = await res.text();
      console.log("[authClient] Register response:", res.status, text);
      return res.ok;
    } catch (err) {
      console.error("[authClient] Register error:", err);
      return false;
    }
  },

  login: async (email: string, password: string): Promise<boolean> => {
    try {
      console.log("[authClient] Logging in user:", email);
      const res = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const txt = await res.text();
        console.warn("[authClient] Login failed:", res.status, txt);
        return false;
      }

      const data: { access_token: string; token_type: string } = await res.json();
      token = data.access_token;
      console.log("[authClient] Login success, token:", token);

      if (typeof window !== "undefined") {
        localStorage.setItem("token", token);
      }

      return true;
    } catch (err) {
      console.error("[authClient] Login error:", err);
      return false;
    }
  },

  logout: () => {
    console.log("[authClient] Logging out");
    token = null;
    if (typeof window !== "undefined") {
      localStorage.removeItem("token");
    }
  },

  authHeader: (): { Authorization?: string } => {
    return token ? { Authorization: `Bearer ${token}` } : {};
  },

  getToken: () => token,
};
