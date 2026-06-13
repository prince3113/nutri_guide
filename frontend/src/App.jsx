import { useState, useCallback } from "react";
import { getToken, clearToken } from "./api";
import BackgroundOrbs from "./components/BackgroundOrbs";
import Toast from "./components/Toast";
import AuthScreen from "./pages/AuthScreen";
import ProfileScreen from "./pages/ProfileScreen";
import DashboardScreen from "./pages/DashboardScreen";

function App() {
  const [screen, setScreen] = useState(getToken() ? "dashboard" : "auth");
  const [toast, setToast] = useState({ message: "", type: "info" });

  const showToast = useCallback((message, type = "info") => {
    setToast({ message, type });
  }, []);

  const clearToast = useCallback(() => {
    setToast({ message: "", type: "info" });
  }, []);

  function handleLogin() {
    setScreen("dashboard");
  }

  function handleLogout() {
    clearToken();
    setScreen("auth");
    showToast("Logged out successfully", "info");
  }

  function handleProfileCreated() {
    setScreen("dashboard");
  }

  function handleNewProfile() {
    setScreen("profile");
  }

  return (
    <>
      <BackgroundOrbs />

      {screen === "auth" && (
        <AuthScreen onLogin={handleLogin} showToast={showToast} />
      )}

      {screen === "profile" && (
        <ProfileScreen
          onProfileCreated={handleProfileCreated}
          onLogout={handleLogout}
          showToast={showToast}
        />
      )}

      {screen === "dashboard" && (
        <DashboardScreen
          onNewProfile={handleNewProfile}
          onLogout={handleLogout}
          showToast={showToast}
        />
      )}

      <Toast message={toast.message} type={toast.type} onClose={clearToast} />
    </>
  );
}

export default App;
