import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";
import api from "../api/api";
import "./LoginPage.css";

const LoginPage = () => {
    const navigate = useNavigate();
    const { login, token } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        if (token) {
            navigate("/dashboard");
        }
    }, [token, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await api.post("/login", {
                username: email,
                password,
            });

            login(response.data.access_token);
            navigate("/dashboard");

        } catch (error) {
            setError(`An error occurred ${error.response?.data?.detail || "Please check your credentials and try again."}`);
            console.error("Login error:", error);
        }
    };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="input-container">
          <label>Email:</label>
          <input
            className="input-field"
            placeholder="Enter your email"
            aria-label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="input-container">
          <label>Password:</label>
          <input
            className="input-field"
            type="password"
            placeholder="Enter your password"
            aria-label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {error && <div className="error">{error}</div>}
        <button className="submit-button" type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;