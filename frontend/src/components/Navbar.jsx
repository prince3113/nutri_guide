export default function Navbar({ onNewProfile, onLogout, showNewProfile = false, profilePhoto = null, userName = null }) {
  function getInitials(name) {
    if (!name) return "U";
    return name.split(" ").map((n) => n[0]).join("").toUpperCase().slice(0, 2);
  }

  const API_BASE = "http://127.0.0.1:5000";

  return (
    <nav className="top-nav">
      <div className="nav-brand">
        <svg viewBox="0 0 48 48" fill="none" width="28" height="28">
          <path
            d="M24 4C20 4 12 8 12 20C12 28 16 36 24 44C32 36 36 28 36 20C36 8 28 4 24 4Z"
            fill="url(#leaf-nav)"
            opacity="0.9"
          />
          <path
            d="M24 12V36M18 18C20 20 22 22 24 24M30 18C28 20 26 22 24 24"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <defs>
            <linearGradient id="leaf-nav" x1="12" y1="4" x2="36" y2="44">
              <stop stopColor="#34d399" />
              <stop offset="1" stopColor="#059669" />
            </linearGradient>
          </defs>
        </svg>
        <span>NutriGuide</span>
      </div>
      <div className="nav-actions">
        {showNewProfile && (
          <button className="btn-ghost" onClick={onNewProfile}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="18" height="18">
              <path d="M12 4v16m8-8H4" />
            </svg>
            New Profile
          </button>
        )}
        <button className="btn-ghost" onClick={onLogout}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="18" height="18">
            <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" />
          </svg>
          Logout
        </button>
        {(userName || profilePhoto) && (
          <div className="nav-avatar-container" title={userName}>
            {profilePhoto ? (
              <img src={`${API_BASE}${profilePhoto}`} alt={userName} className="nav-avatar" />
            ) : (
              <div className="nav-avatar nav-avatar-initials">{getInitials(userName)}</div>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}
