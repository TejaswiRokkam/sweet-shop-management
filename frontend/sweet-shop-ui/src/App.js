import { useEffect, useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import SweetList from "./components/SweetList";
import { apiRequest } from "./api/api";



function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [loading, setLoading] = useState(true);

  // Check auth on app load
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const user = await apiRequest("/auth/me");
        setIsLoggedIn(true);
        setIsAdmin(user.is_admin);
      } catch {
        // token invalid or expired
        localStorage.removeItem("token");
        localStorage.removeItem("isAdmin");
        setIsLoggedIn(false);
        setIsAdmin(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleLogin = ({ isAdmin }) => {
    setIsLoggedIn(true);
    setIsAdmin(isAdmin);
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("isAdmin");
    setIsLoggedIn(false);
    setIsAdmin(false);
  };

  if (loading) {
    return (
    <div className="min-h-screen flex items-center justify-center text-lg">
      Loading...
    </div>
    );
  }


  return (
  <div className="min-h-screen bg-gradient-to-br from-pink-50 to-orange-100 flex justify-center">
    <div className="w-full max-w-4xl p-6">
      <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
        🍬 Sweet Shop Management System
      </h1>

      {!isLoggedIn ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Register />
          <Login onLogin={handleLogin} />
        </div>
      ) : (
        <>
          <div className="flex justify-end mb-4">
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
            >
              Logout
            </button>
          </div>

          <SweetList isAdmin={isAdmin} />
        </>
      )}
    </div>
  </div>
  );

}

export default App;