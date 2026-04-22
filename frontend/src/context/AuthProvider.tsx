import { useState, useEffect } from "react";
import { AuthContext } from "./AuthContext";
import { setupInterceptors } from "../api/apiInterceptor";

export function AuthProvider({ children }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token") || null);

  const login = (token: string) => {
    localStorage.setItem("token", token);
    setToken(token);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };
  
  useEffect(() => {
    setupInterceptors(logout);
  }, []);

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};