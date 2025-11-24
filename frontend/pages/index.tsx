// frontend/pages/index.tsx
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { authClient } from "../lib/authClient";

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (authClient.getToken()) {
      router.push("/infer");
    } else {
      setLoading(false);
    }
  }, [router]);

  const handleLogout = () => {
    authClient.logout();
    router.push("/login");
  };

  if (loading) {
    return (
      <div className="page-container">
        <p className="text-xl text-gray-400 animate-pulse">Checking session...</p>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="card text-center">
        <h1 className="text-3xl font-bold text-emerald-400 mb-4">SafeChain Frontend</h1>
        <p className="text-gray-300 mb-6">You are not logged in.</p>
        <div className="flex flex-col gap-4">
          <button
            onClick={() => router.push("/login")}
            className="px-6 py-2 bg-emerald-500 hover:bg-emerald-600 rounded-lg font-semibold"
          >
            Go to Login
          </button>
          <button
            onClick={handleLogout}
            className="px-6 py-2 bg-red-600 hover:bg-red-500 rounded-lg font-semibold"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}
