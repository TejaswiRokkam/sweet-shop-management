import { apiRequest } from "../api/api";
import { useState } from "react";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = async () => {
    try {
      const data = await apiRequest("/auth/login", "POST", {
        email,
        password,
      });

      // Store token
      localStorage.setItem("token", data.access_token);

      // Store admin safely as string
      localStorage.setItem("isAdmin", data.is_admin ? "true" : "false");

      // Notify parent
      onLogin({
        isAdmin: data.is_admin,
      });
    } catch (err) {
      alert(err.message);
    }
  };

  return (
  <div className="bg-white p-6 rounded-xl shadow-md">
    <h2 className="text-xl font-semibold mb-4 text-gray-800">
      Login
    </h2>

    <input
      className="w-full border border-gray-300 p-2 rounded mb-3 focus:outline-none focus:ring-2 focus:ring-green-400"
      placeholder="Email"
      onChange={(e) => setEmail(e.target.value)}
    />

    <input
      className="w-full border border-gray-300 p-2 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-green-400"
      type="password"
      placeholder="Password"
      onChange={(e) => setPassword(e.target.value)}
    />

    <button
      onClick={submit}
      className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600 transition"
    >
      Login
    </button>
  </div>
  );

}
