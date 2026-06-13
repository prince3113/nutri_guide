import { useState } from "react";

export default function FoodScanner({ showToast }) {
  const [imagePreview, setImagePreview] = useState(null);
  const [base64Image, setBase64Image] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  function handleImageChange(e) {
    const file = e.target.files[0];
    if (!file) return;

    // Preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
      setBase64Image(reader.result);
      setResult(null); // Clear previous result
    };
    reader.readAsDataURL(file);
  }

  async function handleScan() {
    if (!base64Image) return;

    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      const response = await fetch("http://127.0.0.1:5000/recognize-food", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ image: base64Image }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || "Failed to analyze image");
      }

      setResult(data);
      showToast("Food analyzed successfully!", "success");
    } catch (err) {
      showToast(err.message, "error");
    } finally {
      setLoading(false);
    }
  }

  function handleClear() {
    setImagePreview(null);
    setBase64Image(null);
    setResult(null);
  }

  function getRatingClass(rating) {
    const map = {
      healthy: "badge-normal",
      moderate: "badge-overweight",
      unhealthy: "badge-obese",
    };
    return map[rating?.toLowerCase()] || "badge-normal";
  }

  return (
    <div className="food-scanner-section glass-card animate-slide-up animate-slide-up-delay-3">
      <div className="section-header">
        <div className="section-title-group">
          <div className="section-icon section-icon-amber">📸</div>
          <div>
            <h2>AI Food Scanner</h2>
            <p className="section-subtitle">Upload a food photo to estimate calories and macronutrients instantly</p>
          </div>
        </div>
      </div>

      <div className="scanner-layout">
        {/* Upload Zone */}
        <div className="scanner-upload-zone">
          {!imagePreview ? (
            <label className="upload-box-label" htmlFor="food-image-input">
              <div className="upload-box-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" width="48" height="48">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
                  <circle cx="12" cy="13" r="4" />
                </svg>
              </div>
              <span className="upload-box-text">Take a picture or upload photo of your meal</span>
              <span className="upload-box-sub">Supports PNG, JPG, JPEG</span>
              <input
                type="file"
                id="food-image-input"
                accept="image/*"
                onChange={handleImageChange}
                style={{ display: "none" }}
              />
            </label>
          ) : (
            <div className="scanner-preview-container">
              <img src={imagePreview} alt="Food preview" className="scanner-preview-image" />
              {loading && <div className="scan-bar-animation"></div>}
              
              {!loading && (
                <div className="scanner-preview-actions">
                  <button className="btn btn-primary" onClick={handleScan}>
                    <span>Analyze Food</span>
                  </button>
                  <button className="btn btn-cancel" onClick={handleClear}>
                    Remove
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Results Area */}
        <div className="scanner-results-zone">
          {loading && (
            <div className="scanner-loading">
              <div className="spinner"></div>
              <p>Scanning food image and estimating nutrition...</p>
            </div>
          )}

          {!loading && !result && (
            <div className="scanner-placeholder">
              <div className="placeholder-icon">🤖</div>
              <p>Nutrition analysis will appear here after scanning your food photo.</p>
            </div>
          )}

          {!loading && result && (
            <div className="scanner-result-card animate-scale-in">
              <div className="result-header">
                <div>
                  <h3 className="result-food-name">{result.food_name}</h3>
                  <span className={`metric-badge ${getRatingClass(result.health_rating)}`}>
                    {result.health_rating || "moderate"}
                  </span>
                </div>
                <div className="result-calories">
                  <span className="cal-val">{result.estimated_calories}</span>
                  <span className="cal-unit">kcal</span>
                </div>
              </div>

              <p className="result-description">{result.description}</p>

              <div className="result-details-grid">
                <div className="res-detail">
                  <span className="res-detail-label">Serving Size</span>
                  <span className="res-detail-value">{result.serving_size || "1 serving"}</span>
                </div>
                <div className="res-detail">
                  <span className="res-detail-label">Health Tip</span>
                  <span className="res-detail-value font-italic">&ldquo;{result.tips}&rdquo;</span>
                </div>
              </div>

              <div className="scanner-macro-breakdown">
                <h4>Macronutrient Estimation</h4>
                <div className="scanner-macros-grid">
                  <div className="scan-macro-item protein">
                    <span className="macro-label">Protein</span>
                    <span className="macro-val">{result.estimated_protein_g}g</span>
                    <div className="scan-macro-bar">
                      <div
                        className="scan-macro-fill scan-protein-fill"
                        style={{ width: `${Math.min((result.estimated_protein_g / 50) * 100, 100)}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="scan-macro-item carbs">
                    <span className="macro-label">Carbs</span>
                    <span className="macro-val">{result.estimated_carbs_g}g</span>
                    <div className="scan-macro-bar">
                      <div
                        className="scan-macro-fill scan-carbs-fill"
                        style={{ width: `${Math.min((result.estimated_carbs_g / 100) * 100, 100)}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="scan-macro-item fats">
                    <span className="macro-label">Fats</span>
                    <span className="macro-val">{result.estimated_fats_g}g</span>
                    <div className="scan-macro-bar">
                      <div
                        className="scan-macro-fill scan-fats-fill"
                        style={{ width: `${Math.min((result.estimated_fats_g / 40) * 100, 100)}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <button className="btn btn-ghost btn-full mt-16" onClick={handleClear}>
                Scan Another Item
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
