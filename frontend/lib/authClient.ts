const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

let token: string | null = null;

// Load token from localStorage if in browser
if (typeof window !== "undefined") {
  token = localStorage.getItem("token");
}

export const authClient = {
  register: async (email: string, password: string): Promise<boolean> => {
    try {
      const res = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      return res.ok;
    } catch {
      return false;
    }
  },

  login: async (email: string, password: string): Promise<boolean> => {
    try {
      const res = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) return false;

      const data: { access_token: string; token_type: string } = await res.json();
      token = data.access_token;

      if (typeof window !== "undefined") {
        localStorage.setItem("token", token); // persist token in browser
      }

      return true;
    } catch {
      return false;
    }
  },

  logout: () => {
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
