import { useState } from "react";
import { apiRequest, setToken } from "../api";

export default function AuthScreen({ onLogin, showToast }) {
  const [isRegister, setIsRegister] = useState(false);
  const [showAuthForm, setShowAuthForm] = useState(false);
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
    <div className="auth-screen public-home">
      <nav className="public-nav">
        <a className="public-brand" href="#home" aria-label="NutriGuide home">
          <svg viewBox="0 0 48 48" fill="none" width="30" height="30">
            <path
              d="M24 4C20 4 12 8 12 20C12 28 16 36 24 44C32 36 36 28 36 20C36 8 28 4 24 4Z"
              fill="url(#leaf-public)"
            />
            <path
              d="M24 12V36M18 18C20 20 22 22 24 24M30 18C28 20 26 22 24 24"
              stroke="white"
              strokeWidth="2"
              strokeLinecap="round"
            />
            <defs>
              <linearGradient id="leaf-public" x1="12" y1="4" x2="36" y2="44">
                <stop stopColor="#34d399" />
                <stop offset="0.55" stopColor="#06b6d4" />
                <stop offset="1" stopColor="#fbbf24" />
              </linearGradient>
            </defs>
          </svg>
          <span>NutriGuide</span>
        </a>
        <div className="public-nav-links">
          <a href="#about">About</a>
          <button type="button" onClick={() => { setIsRegister(false); setShowAuthForm(true); }}>Login</button>
          <button type="button" className="nav-signup" onClick={() => { setIsRegister(true); setShowAuthForm(true); }}>Sign Up</button>
        </div>
      </nav>
      <div className={`auth-container ${showAuthForm ? "" : "auth-container-dashboard"}`}>
        <section className="auth-showcase animate-slide-up" id="home">
          <div className="brand auth-brand">
            <div className="brand-icon">
              <svg viewBox="0 0 48 48" fill="none">
                <path
                  d="M24 4C20 4 12 8 12 20C12 28 16 36 24 44C32 36 36 28 36 20C36 8 28 4 24 4Z"
                  fill="url(#leaf-auth)"
                  opacity="0.95"
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
                    <stop offset="0.55" stopColor="#06b6d4" />
                    <stop offset="1" stopColor="#7c3aed" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <h1 className="brand-name">NutriGuide</h1>
            <p className="brand-tagline">A sharper way to plan meals, hydration, and daily goals.</p>
          </div>

          <div className="nutrition-console glass-card">
            <div className="console-topline">
              <span>Today</span>
              <strong>2,180 kcal</strong>
            </div>
            <div className="console-ring" aria-hidden="true">
              <svg viewBox="0 0 160 160">
                <circle cx="80" cy="80" r="58" />
                <circle cx="80" cy="80" r="58" className="ring-protein" />
                <circle cx="80" cy="80" r="43" className="ring-water" />
              </svg>
              <div>
                <strong>82%</strong>
                <span>balanced</span>
              </div>
            </div>
            <div className="console-bars">
              <span style={{ "--bar": "72%" }}>Protein</span>
              <span style={{ "--bar": "58%" }}>Carbs</span>
              <span style={{ "--bar": "44%" }}>Fats</span>
            </div>
          </div>

          <div className="public-dashboard-grid">
            <div className="public-stat-card">
              <span>Smart BMI</span>
              <strong>22.4</strong>
              <small>Normal range</small>
            </div>
            <div className="public-stat-card highlight">
              <span>Daily Water</span>
              <strong>2.8L</strong>
              <small>Hydration goal</small>
            </div>
            <div className="public-stat-card">
              <span>Meal Plan</span>
              <strong>4x</strong>
              <small>Balanced meals</small>
            </div>
          </div>
        </section>

        {/* Login Form */}
        {showAuthForm && !isRegister && (
          <form className="auth-form glass-card" onSubmit={handleLogin} key="login">
            <h2>Login</h2>
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
        {showAuthForm && isRegister && (
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

      <section className="about-section" id="about">
        <div className="about-copy">
          <span className="eyebrow">About NutriGuide</span>
          <h2>A dashboard that turns health data into daily decisions.</h2>
          <p>
            NutriGuide calculates BMI, calorie targets, water intake, macros, micronutrients,
            and meal suggestions from your profile so your plan feels personal, readable, and easy to act on.
          </p>
        </div>
        <div className="about-feature-grid">
          <div>
            <span>01</span>
            <strong>Personal profiles</strong>
            <p>Save your body metrics, goal, activity level, and diet preference.</p>
          </div>
          <div>
            <span>02</span>
            <strong>Visual dashboard</strong>
            <p>Track calories, hydration, BMI, and nutrition breakdowns in one place.</p>
          </div>
          <div>
            <span>03</span>
            <strong>Adaptive diet plans</strong>
            <p>Refresh meal ideas and adjust your plan when your goal changes.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
