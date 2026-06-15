import { useEffect, useState } from "react";
import { apiRequest, getToken } from "../api";
import Navbar from "../components/Navbar";

const MEAL_ICONS = {
  breakfast: "🌅",
  lunch: "☀️",
  dinner: "🌙",
  snacks: "🍎",
};

function getBmiClass(category) {
  const map = {
    Underweight: "badge-underweight",
    "Normal Weight": "badge-normal",
    Overweight: "badge-overweight",
    Obese: "badge-obese",
  };
  return map[category] || "badge-normal";
}

function calcBmiProgress(bmi) {
  const pct = Math.min(Math.max(((bmi - 10) / 30) * 100, 0), 100);
  const circumference = 2 * Math.PI * 52;
  return circumference - (pct / 100) * circumference;
}

function getImportanceClass(importance) {
  const map = { high: "importance-high", medium: "importance-medium", low: "importance-low" };
  return map[importance] || "importance-medium";
}

export default function DashboardScreen({ onNewProfile, onLogout, showToast }) {
  const [profile, setProfile] = useState(null);
  const [water, setWater] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploadingPhoto, setUploadingPhoto] = useState(false);
  const [regeneratingDiet, setRegeneratingDiet] = useState(false);

  // Edit Goal modal
  const [showEditGoal, setShowEditGoal] = useState(false);
  const [editGoalValue, setEditGoalValue] = useState("");
  const [editGoalLoading, setEditGoalLoading] = useState(false);

  // Edit Profile modal
  const [showEditProfile, setShowEditProfile] = useState(false);
  const [editProfileForm, setEditProfileForm] = useState({
    age: "", gender: "", height: "", weight: "", activity_level: "", goal: "", diet_type: "vegetarian",
  });
  const [editProfileLoading, setEditProfileLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        const [profileData, waterData] = await Promise.all([
          apiRequest("/health-profile"),
          apiRequest("/water-intake"),
        ]);
        setProfile(profileData);
        setWater(waterData);
      } catch (err) {
        showToast(err.message, "error");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [showToast]);

  // --- Edit Goal ---
  function openEditGoal() { setEditGoalValue(profile?.goal || ""); setShowEditGoal(true); }
  function closeEditGoal() { setShowEditGoal(false); setEditGoalValue(""); }

  async function handleGoalUpdate(e) {
    e.preventDefault();
    if (editGoalValue === profile.goal) { closeEditGoal(); return; }
    setEditGoalLoading(true);
    try {
      const updated = await apiRequest("/health-profile", { method: "PUT", body: JSON.stringify({ goal: editGoalValue }) });
      setProfile(updated);
      try { setWater(await apiRequest("/water-intake")); } catch {
        // Water refresh is optional after a goal-only update.
      }
      showToast("Goal updated successfully!", "success");
      closeEditGoal();
    } catch (err) { showToast(err.message, "error"); }
    finally { setEditGoalLoading(false); }
  }

  // --- Edit Profile ---
  function openEditProfile() {
    setEditProfileForm({
      age: profile?.age?.toString() || "", gender: profile?.gender || "",
      height: profile?.height?.toString() || "", weight: profile?.weight?.toString() || "",
      activity_level: profile?.activity_level || "", goal: profile?.goal || "",
      diet_type: profile?.diet_type || "vegetarian",
    });
    setShowEditProfile(true);
  }
  function closeEditProfile() { setShowEditProfile(false); }
  function updateEditField(field, value) { setEditProfileForm((prev) => ({ ...prev, [field]: value })); }

  async function handleProfileUpdate(e) {
    e.preventDefault();
    setEditProfileLoading(true);
    try {
      const payload = {
        age: parseInt(editProfileForm.age), gender: editProfileForm.gender,
        height: parseFloat(editProfileForm.height), weight: parseFloat(editProfileForm.weight),
        activity_level: editProfileForm.activity_level, goal: editProfileForm.goal,
        diet_type: editProfileForm.diet_type,
      };
      const updated = await apiRequest("/health-profile", { method: "PUT", body: JSON.stringify(payload) });
      setProfile(updated);
      try { setWater(await apiRequest("/water-intake")); } catch {
        // Water refresh is optional after profile edits.
      }
      showToast("Profile updated successfully!", "success");
      closeEditProfile();
    } catch (err) { showToast(err.message, "error"); }
    finally { setEditProfileLoading(false); }
  }



  // --- Diet Plan Regeneration ---
  async function handleRegenerateDiet() {
    setRegeneratingDiet(true);
    try {
      // Add a small artificial delay of 800ms to allow the animation to play
      await new Promise((resolve) => setTimeout(resolve, 800));
      const res = await apiRequest("/regenerate-diet", { method: "POST" });
      setProfile((prev) => ({
        ...prev,
        diet_plan: res.diet_plan,
      }));
      showToast("Generated a new diet plan variant! 🥗", "success");
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setRegeneratingDiet(false);
    }
  }

  // --- Profile Photo Upload/Delete ---
  async function handlePhotoUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("photo", file);

    setUploadingPhoto(true);
    try {
      const token = getToken();
      const response = await fetch("http://127.0.0.1:5000/profile-photo", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || "Failed to upload photo");
      }

      setProfile((prev) => ({
        ...prev,
        profile_photo: data.photo_url,
      }));
      showToast("Profile picture updated! 📸", "success");
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setUploadingPhoto(false);
    }
  }

  async function handlePhotoDelete() {
    if (!window.confirm("Are you sure you want to remove your profile photo?")) return;
    try {
      await apiRequest("/profile-photo", { method: "DELETE" });
      setProfile((prev) => ({
        ...prev,
        profile_photo: null,
      }));
      showToast("Profile picture removed.", "success");
    } catch (err) {
      showToast(err.message, "error");
    }
  }

  // --- Initials Helper ---
  function getInitials(name) {
    if (!name) return "U";
    return name.split(" ").map((n) => n[0]).join("").toUpperCase().slice(0, 2);
  }

  if (loading) {
    return (
      <div className="dashboard-screen">
        <Navbar onNewProfile={onNewProfile} onLogout={onLogout} showNewProfile={false} />
        <div className="dashboard-container" style={{ display: "flex", justifyContent: "center", paddingTop: "120px" }}>
          <div className="spinner" style={{ width: 40, height: 40, borderWidth: 3 }}></div>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="dashboard-screen">
        <Navbar onNewProfile={onNewProfile} onLogout={onLogout} showNewProfile={true} />
        <div className="dashboard-container" style={{ textAlign: "center", paddingTop: "120px" }}>
          <h2 style={{ color: "var(--text-secondary)", marginBottom: 16 }}>No health profile found</h2>
          <p style={{ color: "var(--text-muted)", marginBottom: 32 }}>Create your profile to see your dashboard</p>
          <button className="btn btn-primary" onClick={onNewProfile}><span>Create Profile</span></button>
        </div>
      </div>
    );
  }

  const ringOffset = calcBmiProgress(profile.bmi);
  const macros = profile.macros;
  const micros = profile.micronutrients;
  const report = profile.health_report;

  // Safe fallback calculation for water recommendations
  const recommendedLiters = water?.recommended_water_intake_liters ?? water?.recommended_water_intake ?? water?.target_liters ?? 2.0;
  const recommendedGlasses = Math.ceil(recommendedLiters / 0.25);


  return (
    <div className="dashboard-screen">
      <Navbar
        onNewProfile={onNewProfile}
        onLogout={onLogout}
        showNewProfile={false}
        profilePhoto={profile?.profile_photo}
        userName={profile?.user_name}
      />

      <div className="dashboard-container">
        <div className="dashboard-header animate-slide-up">
          <span className="eyebrow">Live nutrition cockpit</span>
          <h1>Your Health Dashboard</h1>
          <p>Here&apos;s your personalized health overview</p>
        </div>

        <section className="dashboard-hero glass-card animate-slide-up animate-slide-up-delay-1">
          <div className="hero-copy">
            <span className="hero-kicker">{profile.goal}</span>
            <h2>{profile.user_name ? `${profile.user_name}'s` : "Your"} daily plan is ready</h2>
            <p>
              Calories, hydration, macros, meal timing, and micronutrients are tuned to your latest profile.
            </p>
            <div className="hero-actions">
              <button className="btn btn-primary" onClick={handleRegenerateDiet} disabled={regeneratingDiet}>
                {regeneratingDiet ? <div className="spinner"></div> : <span>Refresh Diet Plan</span>}
              </button>
              <button className="btn btn-soft" onClick={openEditProfile}>
                <span>Fine Tune Profile</span>
              </button>
            </div>
          </div>
          <div className="hero-stats">
            <div className="hero-stat">
              <span>BMI</span>
              <strong>{profile.bmi}</strong>
              <small>{profile.category}</small>
            </div>
            <div className="hero-stat accent">
              <span>Calories</span>
              <strong>{profile.target_calories}</strong>
              <small>kcal/day</small>
            </div>
            <div className="hero-stat">
              <span>Water</span>
              <strong>{recommendedLiters}L</strong>
              <small>{recommendedGlasses} glasses</small>
            </div>
          </div>
        </section>

        {/* ======== Metrics Grid ======== */}
        <div className="metrics-grid">
          {/* BMI Card */}
          <div className="metric-card glass-card bmi-card animate-slide-up animate-slide-up-delay-1">
            <div className="metric-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M12 2a10 10 0 100 20 10 10 0 000-20z" /><path d="M12 6v6l4 2" /></svg></div>
            <div className="metric-label">BMI Score</div>
            <div className="metric-value">{profile.bmi}</div>
            <div className={`metric-badge ${getBmiClass(profile.category)}`}>{profile.category}</div>
            <div className="metric-ring">
              <svg viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="52" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="8" />
                <circle cx="60" cy="60" r="52" fill="none" stroke="url(#ring-grad)" strokeWidth="8" strokeLinecap="round" strokeDasharray="327" strokeDashoffset={ringOffset} transform="rotate(-90 60 60)" style={{ transition: "stroke-dashoffset 1.5s cubic-bezier(0.16, 1, 0.3, 1)" }} />
                <defs><linearGradient id="ring-grad" x1="0" y1="0" x2="1" y2="1"><stop stopColor="#34d399" /><stop offset="1" stopColor="#06b6d4" /></linearGradient></defs>
              </svg>
            </div>
          </div>

          {/* Calories Card */}
          <div className="metric-card glass-card calories-card animate-slide-up animate-slide-up-delay-2">
            <div className="metric-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M12 2c1 4 4 6 4 10a4 4 0 11-8 0c0-4 3-6 4-10z" /></svg></div>
            <div className="metric-label">Target Calories</div>
            <div className="metric-value">{profile.target_calories}</div>
            <div className="metric-sub">kcal / day</div>
            <div className="calorie-details">
              <div className="cal-detail"><span className="cal-detail-label">BMR</span><span className="cal-detail-value">{profile.bmr}</span></div>
              <div className="cal-detail"><span className="cal-detail-label">Maintenance</span><span className="cal-detail-value">{profile.maintenance_calories}</span></div>
            </div>
          </div>

          {/* Water Intake Recommendation Card */}
          <div className="metric-card glass-card water-card animate-slide-up animate-slide-up-delay-3">
            <div className="water-card-header">
              <div className="metric-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M12 2L6 12a6 6 0 1012 0L12 2z" /></svg></div>
              <div className="metric-label">Recommended Water</div>
            </div>
            <div className="metric-value">{water ? `${recommendedLiters} L` : "—"}</div>
            <div className="metric-sub">per day (~{recommendedGlasses} glasses)</div>
            <div style={{ marginTop: "16px", fontSize: "0.78rem", color: "var(--text-secondary)", lineHeight: "1.4" }}>
              Based on weight ({water?.weight || profile?.weight || "—"} kg) and BMI category ({water?.category || profile?.category || "—"}). Proper hydration supports calorie control and metabolism.
            </div>
          </div>
        </div>

        {/* ======== Macronutrient Breakdown ======== */}
        {macros && (
          <div className="macros-section glass-card animate-slide-up animate-slide-up-delay-3">
            <div className="section-header">
              <div className="section-title-group">
                <div className="section-icon section-icon-amber">🥩</div>
                <div>
                  <h2>Macronutrient Breakdown</h2>
                  <p className="section-subtitle">Daily intake based on your {profile.weight} kg body weight</p>
                </div>
              </div>
            </div>

            {/* Protein highlight */}
            <div className="protein-highlight">
              <div className="protein-main">
                <span className="protein-big">{macros.protein_g}g</span>
                <span className="protein-label">Protein / day</span>
              </div>
              <div className="protein-detail">
                <span className="protein-per-kg">{macros.protein_per_kg} g/kg</span>
                <span className="protein-note">of body weight</span>
              </div>
            </div>

            {/* Macro bars */}
            <div className="macro-bars">
              <div className="macro-bar-item">
                <div className="macro-bar-header">
                  <div className="macro-bar-info">
                    <span className="macro-dot macro-dot-protein"></span>
                    <span className="macro-bar-name">Protein</span>
                  </div>
                  <span className="macro-bar-value">{macros.protein_g}g <span className="macro-bar-pct">({macros.protein_pct}%)</span></span>
                </div>
                <div className="macro-bar-track">
                  <div className="macro-bar-fill macro-fill-protein" style={{ width: `${macros.protein_pct}%` }}></div>
                </div>
                <span className="macro-bar-cal">{macros.protein_calories} kcal</span>
              </div>

              <div className="macro-bar-item">
                <div className="macro-bar-header">
                  <div className="macro-bar-info">
                    <span className="macro-dot macro-dot-carbs"></span>
                    <span className="macro-bar-name">Carbohydrates</span>
                  </div>
                  <span className="macro-bar-value">{macros.carbs_g}g <span className="macro-bar-pct">({macros.carbs_pct}%)</span></span>
                </div>
                <div className="macro-bar-track">
                  <div className="macro-bar-fill macro-fill-carbs" style={{ width: `${macros.carbs_pct}%` }}></div>
                </div>
                <span className="macro-bar-cal">{macros.carbs_calories} kcal</span>
              </div>

              <div className="macro-bar-item">
                <div className="macro-bar-header">
                  <div className="macro-bar-info">
                    <span className="macro-dot macro-dot-fats"></span>
                    <span className="macro-bar-name">Fats</span>
                  </div>
                  <span className="macro-bar-value">{macros.fats_g}g <span className="macro-bar-pct">({macros.fats_pct}%)</span></span>
                </div>
                <div className="macro-bar-track">
                  <div className="macro-bar-fill macro-fill-fats" style={{ width: `${macros.fats_pct}%` }}></div>
                </div>
                <span className="macro-bar-cal">{macros.fats_calories} kcal</span>
              </div>
            </div>
          </div>
        )}

        {/* ======== Health Report ======== */}
        {report && (
          <div className="report-section glass-card animate-slide-up animate-slide-up-delay-3">
            <div className="section-header">
              <div className="section-title-group">
                <div className="section-icon section-icon-green">📊</div>
                <div>
                  <h2>Health Report</h2>
                  <p className="section-subtitle">Your personalized health analysis</p>
                </div>
              </div>
            </div>

            <div className="report-grid">
              <div className="report-card">
                <div className="report-card-icon">⚖️</div>
                <div className="report-card-label">Ideal Weight Range</div>
                <div className="report-card-value">{report.ideal_weight_range}</div>
              </div>
              <div className="report-card">
                <div className="report-card-icon">📍</div>
                <div className="report-card-label">Weight Status</div>
                <div className="report-card-value report-card-value-sm">{report.weight_status}</div>
              </div>
              <div className="report-card">
                <div className="report-card-icon">🔥</div>
                <div className="report-card-label">Calorie Strategy</div>
                <div className="report-card-value report-card-value-sm">{report.calorie_info}</div>
              </div>
              <div className="report-card">
                <div className="report-card-icon">📈</div>
                <div className="report-card-label">Expected Pace</div>
                <div className="report-card-value">{report.pace_info}</div>
              </div>
              <div className="report-card">
                <div className="report-card-icon">🧬</div>
                <div className="report-card-label">Est. Body Fat (Approx)</div>
                <div className="report-card-value">{report.body_fat_estimate}%</div>
              </div>
              <div className="report-card report-card-wide">
                <div className="report-card-icon">💡</div>
                <div className="report-card-label">Recommendations</div>
                <ul className="report-recommendations">
                  {report.recommendations.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* ======== Diet Plan ======== */}
        {profile.diet_plan && (
          <div className="diet-section glass-card animate-slide-up animate-slide-up-delay-3">
            <div className="diet-header">
              <div className="diet-title-group">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" width="24" height="24">
                  <path d="M18 8h1a4 4 0 010 8h-1M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8zM6 1v3M10 1v3M14 1v3" />
                </svg>
                <h2>Your Diet Plan</h2>
              </div>
              <div className="diet-goal-actions">
                <span className="diet-goal-badge">{profile.goal}</span>
                <button
                  className={`btn-regenerate-diet ${regeneratingDiet ? "loading" : ""}`}
                  onClick={handleRegenerateDiet}
                  title="Generate New Plan"
                  id="regenerate-diet-btn"
                  disabled={regeneratingDiet}
                >
                  <svg className={regeneratingDiet ? "spin" : ""} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="14" height="14">
                    <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 11-.57-8.38l5.67-5.67" />
                  </svg>
                  <span>{regeneratingDiet ? "Generating..." : "Regenerate"}</span>
                </button>
                <button className="btn-edit-goal" onClick={openEditGoal} title="Edit Goal" id="edit-goal-btn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="16" height="16"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" /><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" /></svg>
                  <span>Edit Goal</span>
                </button>
              </div>
            </div>
            <div className="meal-grid">
              {["breakfast", "lunch", "snacks", "dinner"].map((meal) => {
                const content = profile.diet_plan[meal];
                if (!content) return null;
                return (
                  <div className={`meal-card ${regeneratingDiet ? "regenerating" : ""}`} key={meal}>
                    <div className="meal-icon" aria-label={MEAL_ICONS[meal] ? meal : "meal"}>
                      {meal === "breakfast" ? "AM" : meal === "lunch" ? "NOON" : meal === "dinner" ? "PM" : "SNACK"}
                    </div>
                    <div className="meal-name">{meal}</div>
                    <div className="meal-content">{content}</div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ======== Micronutrients ======== */}
        {micros && micros.length > 0 && (
          <div className="micros-section glass-card animate-slide-up animate-slide-up-delay-4">
            <div className="section-header">
              <div className="section-title-group">
                <div className="section-icon section-icon-cyan">💊</div>
                <div>
                  <h2>Micronutrient Guide</h2>
                  <p className="section-subtitle">Essential vitamins & minerals for your BMI category: <strong>{profile.category}</strong></p>
                </div>
              </div>
            </div>

            <div className="micros-grid">
              {micros.map((m, i) => (
                <div className={`micro-card ${getImportanceClass(m.importance)}`} key={i}>
                  <div className="micro-card-top">
                    <span className="micro-name">{m.name}</span>
                    <span className={`micro-importance-badge ${getImportanceClass(m.importance)}`}>
                      {m.importance}
                    </span>
                  </div>
                  <div className="micro-amount">{m.amount}</div>
                  <div className="micro-note">{m.note}</div>
                  <div className="micro-sources">
                    <span className="micro-sources-label">Sources:</span> {m.sources}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ======== Profile Summary ======== */}
        <div className="profile-info-section glass-card animate-slide-up animate-slide-up-delay-4">
          <div className="profile-info-header">
            <h3>Profile Summary</h3>
            <button className="btn-edit-profile" onClick={openEditProfile} id="edit-profile-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="16" height="16"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" /><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" /></svg>
              <span>Edit Profile</span>
            </button>
          </div>
          <div className="profile-summary-content">
            <div className="profile-avatar-upload-zone">
              <div className="profile-avatar-large">
                {profile.profile_photo ? (
                  <img src={`http://127.0.0.1:5000${profile.profile_photo}`} alt={profile.user_name} />
                ) : (
                  <div className="avatar-large-initials">{getInitials(profile.user_name)}</div>
                )}
                <label className="avatar-upload-overlay" htmlFor="avatar-file-input">
                  {uploadingPhoto ? (
                    <div className="spinner-small"></div>
                  ) : (
                    <>
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="18" height="18">
                        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
                        <circle cx="12" cy="13" r="4" />
                      </svg>
                      <span>Upload</span>
                    </>
                  )}
                </label>
                <input
                  type="file"
                  id="avatar-file-input"
                  accept="image/*"
                  onChange={handlePhotoUpload}
                  style={{ display: "none" }}
                  disabled={uploadingPhoto}
                />
              </div>
              {profile.profile_photo && (
                <button className="btn-remove-avatar" onClick={handlePhotoDelete} title="Remove Photo">
                  Remove Photo
                </button>
              )}
              <div className="profile-user-details">
                <span className="profile-user-name">{profile.user_name}</span>
                <span className="profile-user-email">{profile.email}</span>
              </div>
            </div>

            <div className="profile-info-grid">
              <div className="info-item"><span className="info-label">Age</span><span className="info-value">{profile.age} yrs</span></div>
              <div className="info-item"><span className="info-label">Gender</span><span className="info-value">{profile.gender}</span></div>
              <div className="info-item"><span className="info-label">Height</span><span className="info-value">{profile.height} cm</span></div>
              <div className="info-item"><span className="info-label">Weight</span><span className="info-value">{profile.weight} kg</span></div>
              <div className="info-item"><span className="info-label">Activity</span><span className="info-value">{profile.activity_level}</span></div>
              <div className="info-item"><span className="info-label">Goal</span><span className="info-value">{profile.goal}</span></div>
              <div className="info-item"><span className="info-label">Diet</span><span className="info-value" style={{ textTransform: "capitalize" }}>{profile.diet_type || "vegetarian"}</span></div>
            </div>
          </div>
        </div>
      </div>

      {/* ========== Edit Goal Modal ========== */}
      {showEditGoal && (
        <div className="modal-overlay" onClick={closeEditGoal}>
          <div className="modal-content glass-card animate-scale-in" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" width="28" height="28"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7" /><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" /></svg></div>
              <h2>Change Your Goal</h2>
              <p>Update your fitness goal and we&apos;ll recalculate your nutrition plan</p>
            </div>
            <form onSubmit={handleGoalUpdate} className="modal-form">
              <div className="goal-options">
                {[
                  { value: "lose weight", label: "Lose Weight", icon: "🔥", desc: "Reduce daily intake by 500 kcal" },
                  { value: "maintain weight", label: "Maintain Weight", icon: "⚖️", desc: "Keep your current calorie balance" },
                  { value: "gain weight", label: "Gain Weight", icon: "💪", desc: "Increase daily intake by 500 kcal" },
                ].map((option) => (
                  <label key={option.value} className={`goal-option ${editGoalValue === option.value ? "goal-option-active" : ""}`} htmlFor={`goal-${option.value}`}>
                    <input type="radio" id={`goal-${option.value}`} name="goal" value={option.value} checked={editGoalValue === option.value} onChange={(e) => setEditGoalValue(e.target.value)} className="goal-radio" />
                    <span className="goal-option-icon">{option.icon}</span>
                    <div className="goal-option-text"><span className="goal-option-label">{option.label}</span><span className="goal-option-desc">{option.desc}</span></div>
                    <div className="goal-check"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" width="16" height="16"><path d="M20 6L9 17l-5-5" /></svg></div>
                  </label>
                ))}
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-cancel" onClick={closeEditGoal}>Cancel</button>
                <button type="submit" className="btn btn-primary" disabled={editGoalLoading || !editGoalValue}>
                  {editGoalLoading ? <div className="spinner"></div> : (<><span>Update Goal</span><svg className="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14M12 5l7 7-7 7" /></svg></>)}
                </button>
              </div>
            </form>
            <button className="modal-close" onClick={closeEditGoal} aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="20" height="20"><path d="M18 6L6 18M6 6l12 12" /></svg></button>
          </div>
        </div>
      )}

      {/* ========== Edit Profile Modal ========== */}
      {showEditProfile && (
        <div className="modal-overlay" onClick={closeEditProfile}>
          <div className="modal-content modal-content-wide glass-card animate-scale-in" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-icon modal-icon-green"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" width="28" height="28"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" /><circle cx="12" cy="7" r="4" /></svg></div>
              <h2>Edit Your Profile</h2>
              <p>Update your details and we&apos;ll recalculate everything</p>
            </div>
            <form onSubmit={handleProfileUpdate} className="modal-form">
              <div className="edit-form-grid">
                <div className="form-group"><label htmlFor="edit-age">Age</label><input type="number" id="edit-age" placeholder="25" min="1" max="120" value={editProfileForm.age} onChange={(e) => updateEditField("age", e.target.value)} required /></div>
                <div className="form-group"><label htmlFor="edit-gender">Gender</label><select id="edit-gender" value={editProfileForm.gender} onChange={(e) => updateEditField("gender", e.target.value)} required><option value="" disabled>Select</option><option value="male">Male</option><option value="female">Female</option></select></div>
                <div className="form-group"><label htmlFor="edit-height">Height <span className="unit">(cm)</span></label><input type="number" id="edit-height" placeholder="170" min="50" max="300" step="0.1" value={editProfileForm.height} onChange={(e) => updateEditField("height", e.target.value)} required /></div>
                <div className="form-group"><label htmlFor="edit-weight">Weight <span className="unit">(kg)</span></label><input type="number" id="edit-weight" placeholder="70" min="10" max="500" step="0.1" value={editProfileForm.weight} onChange={(e) => updateEditField("weight", e.target.value)} required /></div>
                <div className="form-group"><label htmlFor="edit-activity">Activity Level</label><select id="edit-activity" value={editProfileForm.activity_level} onChange={(e) => updateEditField("activity_level", e.target.value)} required><option value="" disabled>Select</option><option value="sedentary">Sedentary</option><option value="lightly active">Lightly Active</option><option value="moderately active">Moderately Active</option><option value="very active">Very Active</option><option value="extra active">Extra Active</option></select></div>
                <div className="form-group"><label htmlFor="edit-goal">Goal</label><select id="edit-goal" value={editProfileForm.goal} onChange={(e) => updateEditField("goal", e.target.value)} required><option value="" disabled>Select</option><option value="lose weight">Lose Weight</option><option value="maintain weight">Maintain Weight</option><option value="gain weight">Gain Weight</option></select></div>
                <div className="form-group"><label htmlFor="edit-diet">Diet Preference</label><select id="edit-diet" value={editProfileForm.diet_type} onChange={(e) => updateEditField("diet_type", e.target.value)} required><option value="vegetarian">Vegetarian 🥗</option><option value="non-vegetarian">Non-Vegetarian 🍗</option></select></div>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-cancel" onClick={closeEditProfile}>Cancel</button>
                <button type="submit" className="btn btn-primary" disabled={editProfileLoading}>
                  {editProfileLoading ? <div className="spinner"></div> : (<><span>Save Changes</span><svg className="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14M12 5l7 7-7 7" /></svg></>)}
                </button>
              </div>
            </form>
            <button className="modal-close" onClick={closeEditProfile} aria-label="Close"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="20" height="20"><path d="M18 6L6 18M6 6l12 12" /></svg></button>
          </div>
        </div>
      )}
    </div>
  );
}
