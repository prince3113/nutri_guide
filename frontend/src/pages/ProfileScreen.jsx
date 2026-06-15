import { useState } from "react";
import { apiRequest } from "../api";
import Navbar from "../components/Navbar";

export default function ProfileScreen({ onProfileCreated, onLogout, showToast }) {
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    age: "",
    gender: "",
    height: "",
    weight: "",
    activity_level: "",
    goal: "",
    diet_type: "vegetarian",
  });

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        age: parseInt(form.age),
        gender: form.gender,
        height: parseFloat(form.height),
        weight: parseFloat(form.weight),
        activity_level: form.activity_level,
        goal: form.goal,
        diet_type: form.diet_type,
      };

      await apiRequest("/health-profile", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      showToast("Health profile created!", "success");
      onProfileCreated();
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="profile-screen">
      <Navbar onLogout={onLogout} />

      <div className="profile-container">
        <div className="profile-header animate-slide-up">
          <span className="eyebrow">Personal setup</span>
          <h1>Build Your Health Profile</h1>
          <p>Tell us about yourself and we&apos;ll create your personalized nutrition plan</p>
        </div>

        <div className="profile-preview-strip animate-slide-up animate-slide-up-delay-1">
          <div className="preview-pill active">
            <span className="preview-mark">01</span>
            Body metrics
          </div>
          <div className="preview-pill">
            <span className="preview-mark">02</span>
            Activity rhythm
          </div>
          <div className="preview-pill">
            <span className="preview-mark">03</span>
            Meal preference
          </div>
        </div>

        <form
          className="glass-card profile-form animate-slide-up animate-slide-up-delay-2"
          onSubmit={handleSubmit}
        >
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="profile-age">Age</label>
              <input
                type="number"
                id="profile-age"
                placeholder="25"
                min="1"
                max="120"
                value={form.age}
                onChange={(e) => updateField("age", e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="profile-gender">Gender</label>
              <select
                id="profile-gender"
                value={form.gender}
                onChange={(e) => updateField("gender", e.target.value)}
                required
              >
                <option value="" disabled>Select</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="profile-height">Height <span className="unit">(cm)</span></label>
              <input
                type="number"
                id="profile-height"
                placeholder="170"
                min="50"
                max="300"
                step="0.1"
                value={form.height}
                onChange={(e) => updateField("height", e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="profile-weight">Weight <span className="unit">(kg)</span></label>
              <input
                type="number"
                id="profile-weight"
                placeholder="70"
                min="10"
                max="500"
                step="0.1"
                value={form.weight}
                onChange={(e) => updateField("weight", e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="profile-activity">Activity Level</label>
              <select
                id="profile-activity"
                value={form.activity_level}
                onChange={(e) => updateField("activity_level", e.target.value)}
                required
              >
                <option value="" disabled>Select</option>
                <option value="sedentary">Sedentary</option>
                <option value="lightly active">Lightly Active</option>
                <option value="moderately active">Moderately Active</option>
                <option value="very active">Very Active</option>
                <option value="extra active">Extra Active</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="profile-goal">Goal</label>
              <select
                id="profile-goal"
                value={form.goal}
                onChange={(e) => updateField("goal", e.target.value)}
                required
              >
                <option value="" disabled>Select</option>
                <option value="lose weight">Lose Weight</option>
                <option value="maintain weight">Maintain Weight</option>
                <option value="gain weight">Gain Weight</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="profile-diet">Diet Preference</label>
              <select
                id="profile-diet"
                value={form.diet_type}
                onChange={(e) => updateField("diet_type", e.target.value)}
                required
              >
                <option value="vegetarian">Vegetarian</option>
                <option value="non-vegetarian">Non-Vegetarian</option>
              </select>
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
            {loading ? <div className="spinner"></div> : (
              <>
                <span>Generate My Plan</span>
                <svg className="btn-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
