// frontend/lib/authClient.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

let token: string | null = null;

// Load token from localStorage if in browser
if (typeof window !== "undefined") {
  token = localStorage.getItem("token");
}

export const authClient = {
  register: async (email: string, password: string): Promise<{ success: boolean; message?: string }> => {
    try {
      const res = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include", // allow cookies
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        return { success: false, message: errData.detail || "Registration failed" };
      }

      return { success: true };
    } catch (err: any) {
      return { success: false, message: err.message || "Network error" };
    }
  },

  login: async (email: string, password: string): Promise<{ success: boolean; message?: string }> => {
    try {
      const res = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include", // allow cookies
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        return { success: false, message: data.detail || "Login failed" };
      }

      token = data.access_token;

      if (typeof window !== "undefined") {
        localStorage.setItem("token", token);
      }

      return { success: true };
    } catch (err: any) {
      return { success: false, message: err.message || "Network error" };
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
