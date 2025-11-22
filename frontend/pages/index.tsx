import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { authClient } from "../lib/authClient";

export default function Home() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // If token exists, user is logged in → go to /infer
    if (authClient.getToken()) {
      router.push("/infer");
    } else {
      setLoading(false); // show login redirect message
    }
  }, [router]);

  const handleLogout = () => {
    authClient.logout();
    router.push("/login");
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-gray-100">
        <p className="text-xl text-gray-600">Checking session...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col justify-center items-center h-screen bg-gray-100">
      <h1 className="text-3xl font-bold mb-4 text-blue-600">SafeChain Frontend</h1>
      <p className="mb-4 text-gray-700">You are not logged in.</p>
      <button
        onClick={() => router.push("/login")}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 mb-2"
      >
        Go to Login
      </button>
      <button
        onClick={handleLogout}
        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Logout
      </button>
    </div>
  );
}
