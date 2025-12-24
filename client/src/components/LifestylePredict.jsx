import { useState, useEffect, useContext } from 'react'
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import '../index.css'

function LifestylePredict() {
    const { token } = useContext(AuthContext);
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        age: 30, // Years
        gender: 2, // 1:Women, 2:Men (Cardio encoding)
        height: 175,
        weight: 75,
        ap_hi: 120,
        ap_lo: 80,
        cholesterol: 1, // 1:Normal, 2:High, 3:Very High
        gluc: 1, // 1:Normal, 2:High, 3:Very High
        smoke: 0,
        alco: 0,
        active: 1,
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
                            gender: profile.gender === 'Male' ? 2 : 1, // Convert
                            height: profile.height,
                            weight: profile.weight,
                            cholesterol: 1, // Default as profile doesn't store these detailed tiers yet
                            gluc: profile.glucose === 'Normal' ? 1 : profile.glucose === 'High' ? 2 : 3, // Approx mapping
                            smoke: profile.smoke === 'Smoker' ? 1 : 0,
                            alco: profile.alco === 'Yes' ? 1 : 0,
                            active: profile.active === 'Active' ? 1 : 0
                        }));
                    }
                }
            } catch (err) {
                console.error("Failed to load profile", err);
            }
        };
        fetchProfileData();
    }, [token]);

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
            const response = await fetch('http://localhost:8000/predict/lifestyle', {
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
                    style={{ position: 'absolute', left: 0, top: '50%', transform: 'translateY(-50%)', background: 'transparent', border: 'none', color: '#4caf50', cursor: 'pointer' }}
                >
                    &larr; Back to Dashboard
                </button>
                <h1 style={{ color: '#4caf50' }}>Long-Term Health Prediction</h1>
                <p>Cardiovascular Lifestyle Analysis</p>
            </header>

            <main>
                <form onSubmit={handleSubmit} className="risk-form" style={{ borderColor: '#4caf50' }}>
                    <div className="form-grid">
                        <div className="input-group">
                            <label>Age (Years)</label>
                            <input type="number" name="age" value={formData.age} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Gender (1:F, 2:M)</label>
                            <select name="gender" value={formData.gender} onChange={handleChange}>
                                <option value={1}>Female</option>
                                <option value={2}>Male</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Height (cm)</label>
                            <input type="number" name="height" value={formData.height} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Weight (kg)</label>
                            <input type="number" name="weight" value={formData.weight} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Systolic BP (ap_hi)</label>
                            <input type="number" name="ap_hi" value={formData.ap_hi} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Diastolic BP (ap_lo)</label>
                            <input type="number" name="ap_lo" value={formData.ap_lo} onChange={handleChange} />
                        </div>

                        <div className="input-group">
                            <label>Cholesterol (1:Norm, 2:Hi, 3:V.Hi)</label>
                            <select name="cholesterol" value={formData.cholesterol} onChange={handleChange}>
                                <option value={1}>Normal</option>
                                <option value={2}>Above Normal</option>
                                <option value={3}>Well Above Normal</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Glucose (1:Norm, 2:Hi, 3:V.Hi)</label>
                            <select name="gluc" value={formData.gluc} onChange={handleChange}>
                                <option value={1}>Normal</option>
                                <option value={2}>Above Normal</option>
                                <option value={3}>Well Above Normal</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Smoking</label>
                            <select name="smoke" value={formData.smoke} onChange={handleChange}>
                                <option value={0}>No</option>
                                <option value={1}>Yes</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Alcohol Intake</label>
                            <select name="alco" value={formData.alco} onChange={handleChange}>
                                <option value={0}>No</option>
                                <option value={1}>Yes</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label>Physical Activity</label>
                            <select name="active" value={formData.active} onChange={handleChange}>
                                <option value={0}>No</option>
                                <option value={1}>Yes</option>
                            </select>
                        </div>

                        <div className="input-group phone-group">
                            <label>Phone (Optional)</label>
                            <input type="text" name="phone_number" value={formData.phone_number} onChange={handleChange} placeholder="+1234567890" />
                        </div>

                    </div>

                    <button type="submit" disabled={loading} className="predict-btn" style={{ background: '#4caf50' }}>
                        {loading ? 'Analyzing...' : 'Predict Lifestyle Risk'}
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
                        <p className="disclaimer">Note: This is an AI prediction and not a medical diagnosis.</p>
                    </div>
                )}

                {error && <div className="error-message">{error}</div>}
            </main>
        </div>
    )
}

export default LifestylePredict
