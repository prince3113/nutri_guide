import { useState } from "react";
import { apiRequest, setToken } from "../api";

export default function AuthScreen({ onLogin, showToast }) {
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);

  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  const [registerName, setRegisterName] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");

  async function handleLogin(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await apiRequest("/login", {
        method: "POST",
        body: JSON.stringify({
          email: loginEmail,
          password: loginPassword,
        }),
      });
      setToken(data.access_token);
      showToast("Login successful!", "success");
      onLogin();
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setLoading(false);
    }
  }

  async function handleRegister(e) {
    e.preventDefault();
    setLoading(true);
    try {
      await apiRequest("/register", {
        method: "POST",
        body: JSON.stringify({
          name: registerName,
          email: registerEmail,
          password: registerPassword,
        }),
      });
      showToast("Account created! Please sign in.", "success");
      setIsRegister(false);
      setLoginEmail(registerEmail);
      setLoginPassword("");
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-screen">
      <div className="auth-container">
        {/* Brand */}
        <div className="brand">
          <div className="brand-icon">
            <svg viewBox="0 0 48 48" fill="none">
              <path
                d="M24 4C20 4 12 8 12 20C12 28 16 36 24 44C32 36 36 28 36 20C36 8 28 4 24 4Z"
                fill="url(#leaf-auth)"
                opacity="0.9"
              />
              <path
                d="M24 12V36M18 18C20 20 22 22 24 24M30 18C28 20 26 22 24 24"
                stroke="white"
                strokeWidth="2"
                strokeLinecap="round"
              />
              <defs>
                <linearGradient id="leaf-auth" x1="12" y1="4" x2="36" y2="44">
                  <stop stopColor="#34d399" />
                  <stop offset="1" stopColor="#059669" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h1 className="brand-name">NutriGuide</h1>
          <p className="brand-tagline">Your personalized health companion</p>
        </div>

        {/* Login Form */}
        {!isRegister && (
          <form className="auth-form glass-card" onSubmit={handleLogin} key="login">
            <h2>Welcome Back</h2>
            <p className="auth-subtitle">Sign in to your account</p>
            <div className="form-group">
              <label htmlFor="login-email">Email</label>
              <input
                type="email"
                id="login-email"
                placeholder="you@example.com"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="login-password">Password</label>
              <input
                type="password"
                id="login-password"
                placeholder="••••••••"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <div className="spinner"></div> : (
                <>
                  <span>Sign In</span>
                  <svg className="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                  </svg>
                </>
              )}
            </button>
            <p className="auth-switch">
              Don&apos;t have an account?{" "}
              <a href="#" onClick={(e) => { e.preventDefault(); setIsRegister(true); }}>
                Create one
              </a>
            </p>
          </form>
        )}

        {/* Register Form */}
        {isRegister && (
          <form className="auth-form glass-card" onSubmit={handleRegister} key="register">
            <h2>Create Account</h2>
            <p className="auth-subtitle">Start your health journey today</p>
            <div className="form-group">
              <label htmlFor="register-name">Full Name</label>
              <input
                type="text"
                id="register-name"
                placeholder="John Doe"
                value={registerName}
                onChange={(e) => setRegisterName(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="register-email">Email</label>
              <input
                type="email"
                id="register-email"
                placeholder="you@example.com"
                value={registerEmail}
                onChange={(e) => setRegisterEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="register-password">Password</label>
              <input
                type="password"
                id="register-password"
                placeholder="••••••••"
                value={registerPassword}
                onChange={(e) => setRegisterPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <div className="spinner"></div> : (
                <>
                  <span>Create Account</span>
                  <svg className="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                  </svg>
                </>
              )}
            </button>
            <p className="auth-switch">
              Already have an account?{" "}
              <a href="#" onClick={(e) => { e.preventDefault(); setIsRegister(false); }}>
                Sign in
              </a>
            </p>
          </form>
        )}
      </div>
    </div>
  );
}
