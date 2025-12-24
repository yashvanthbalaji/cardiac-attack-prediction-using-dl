import { useState, useEffect, useContext } from 'react'
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import '../index.css'

function Home() {
    const { token } = useContext(AuthContext);
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        age: 55,
        sex: 1,
        cp: 0,
        trestbps: 140,
        chol: 240,
        fbs: 0,
        restecg: 1,
        thalach: 150,
        exang: 0,
        oldpeak: 1.5,
        slope: 1,
        ca: 0,
        thal: 2,
        stress_level: 5,
        bmi: 25.0,
        phone_number: ""
    })

    const [result, setResult] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    // Pre-fill from profile
    useEffect(() => {
        const fetchProfileData = async () => {
            if (!token) return;
            try {
                const response = await fetch('http://localhost:8000/profile/', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    const profile = await response.json();
                    if (profile) {
                        setFormData(prev => ({
                            ...prev,
                            age: profile.age,
                            sex: profile.gender === 'Male' ? 1 : 0,
                            stress_level: profile.stress_level,
                            bmi: profile.bmi
                        }));
                    } else {
                        // Strict requirement: Profile mandatory
                        alert("Please complete your profile first.");
                        navigate('/dashboard');
                    }
                }
            } catch (err) {
                console.error("Failed to load profile for pre-fill", err);
            }
        };
        fetchProfileData();
    }, [token, navigate]);

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData(prev => ({
            ...prev,
            [name]: name === 'phone_number' ? value : Number(value)
        }))
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setResult(null)

        try {
            const response = await fetch('http://localhost:8000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData),
            })

            if (!response.ok) {
                throw new Error('Prediction failed')
            }

            const data = await response.json()
            setResult(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="container">
            <header style={{ position: 'relative' }}>
                <button
                    onClick={() => navigate('/dashboard')}
                    style={{ position: 'absolute', left: 0, top: '50%', transform: 'translateY(-50%)', background: 'transparent', border: 'none', color: '#e94560', cursor: 'pointer' }}
                >
                    &larr; Back to Dashboard
                </button>
                <h1>Cardiac Attack Prediction</h1>
                <p>AI-Powered Heart Health Analysis</p>
            </header>

            <main>
                <form onSubmit={handleSubmit} className="risk-form">
                    <div className="form-grid">
                        <div className="input-group">
                            <label>Age</label>
                            <input type="number" name="age" value={formData.age} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Sex (0:F, 1:M)</label>
                            <select name="sex" value={formData.sex} onChange={handleChange}>
                                <option value={0}>Female</option>
                                <option value={1}>Male</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Chest Pain Type (0-3)</label>
                            <select name="cp" value={formData.cp} onChange={handleChange}>
                                <option value={0}>Typical Angina</option>
                                <option value={1}>Atypical Angina</option>
                                <option value={2}>Non-anginal Pain</option>
                                <option value={3}>Asymptomatic</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Resting BP (mm Hg)</label>
                            <input type="number" name="trestbps" value={formData.trestbps} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Cholesterol (mg/dl)</label>
                            <input type="number" name="chol" value={formData.chol} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Fasting BS &gt; 120 (1:T, 0:F)</label>
                            <select name="fbs" value={formData.fbs} onChange={handleChange}>
                                <option value={0}>False</option>
                                <option value={1}>True</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Resting ECG (0-2)</label>
                            <select name="restecg" value={formData.restecg} onChange={handleChange}>
                                <option value={0}>Normal</option>
                                <option value={1}>ST-T Wave Abnormality</option>
                                <option value={2}>Left Ventricular Hypertrophy</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Max Heart Rate</label>
                            <input type="number" name="thalach" value={formData.thalach} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Exercise Angina (0:No, 1:Yes)</label>
                            <select name="exang" value={formData.exang} onChange={handleChange}>
                                <option value={0}>No</option>
                                <option value={1}>Yes</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Oldpeak (ST depression)</label>
                            <input type="number" step="0.1" name="oldpeak" value={formData.oldpeak} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Slope (0-2)</label>
                            <select name="slope" value={formData.slope} onChange={handleChange}>
                                <option value={0}>Upsloping</option>
                                <option value={1}>Flat</option>
                                <option value={2}>Downsloping</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Major Vessels (0-4)</label>
                            <input type="number" name="ca" value={formData.ca} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Thalassemia (0-3)</label>
                            <select name="thal" value={formData.thal} onChange={handleChange}>
                                <option value={0}>Unknown</option>
                                <option value={1}>Normal</option>
                                <option value={2}>Fixed Defect</option>
                                <option value={3}>Reversable Defect</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Stress Level (1-10)</label>
                            <input type="number" name="stress_level" value={formData.stress_level} onChange={handleChange} min="1" max="10" />
                        </div>

                        <div className="input-group">
                            <label>BMI</label>
                            <input type="number" step="0.1" name="bmi" value={formData.bmi} onChange={handleChange} />
                        </div>

                        <div className="input-group phone-group">
                            <label>Phone for Alerts (Optional)</label>
                            <input type="text" name="phone_number" value={formData.phone_number} onChange={handleChange} placeholder="+1234567890" />
                        </div>

                    </div>

                    <button type="submit" disabled={loading} className="predict-btn">
                        {loading ? 'Analyzing...' : 'Predict Risk'}
                    </button>
                </form>

                {result && (
                    <div className={`result-card ${result.risk_probability > 0.5 ? 'high-risk' : 'low-risk'}`}
                        style={{
                            borderTop: `6px solid ${result.risk_probability > 0.8 ? '#b71c1c' :
                                    result.risk_probability > 0.5 ? '#e94560' :
                                        result.risk_probability > 0.2 ? '#ff9800' : '#4caf50'
                                }`
                        }}
                    >
                        <h2>Prediction Result</h2>
                        <div className="risk-score">
                            <span>Risk Percentage:</span>
                            <strong>{(result.risk_probability * 100).toFixed(1)}%</strong>
                        </div>
                        <div className="risk-label" style={{ fontSize: '1.1rem', marginTop: '1rem', lineHeight: '1.4' }}>
                            {result.risk_label}
                        </div>
                        {result.alert_sent && (
                            <div className="sms-alert">
                                ⚠️ SMS Alert Sent to {formData.phone_number}
                            </div>
                        )}
                        <p className="disclaimer">Note: This is an AI prediction and not a medical diagnosis.</p>
                    </div>
                )}

                {error && <div className="error-message">{error}</div>}
            </main>
        </div>
    )
}

export default Home
