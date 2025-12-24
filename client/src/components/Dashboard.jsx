import { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import '../index.css';

const Dashboard = () => {
    const { token, logout, user } = useContext(AuthContext);
    const navigate = useNavigate();
    const [profile, setProfile] = useState(null);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    // Dashboard State for new models
    const [lifestyleResult, setLifestyleResult] = useState(null);
    const [syntheticResult, setSyntheticResult] = useState(null);
    const [syntheticInput, setSyntheticInput] = useState({
        stress_level: 5, sleep_hours: 7, daily_steps: 8000, water_intake: 2, hrv: 60, age: 30, bmi: 25
    });
    const [simLoading, setSimLoading] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            if (!token) return;
            try {
                const [profRes, histRes] = await Promise.allSettled([
                    axios.get('http://localhost:8000/profile/', { headers: { Authorization: `Bearer ${token}` } }),
                    axios.get('http://localhost:8000/profile/history', { headers: { Authorization: `Bearer ${token}` } })
                ]);

                if (profRes.status === 'fulfilled' && profRes.value.data) {
                    setProfile(profRes.value.data);
                }
                if (histRes.status === 'fulfilled' && histRes.value.data) {
                    setHistory(histRes.value.data);
                }
            } catch (err) {
                console.error("Dashboard data fetch error", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [token, lifestyleResult]); // Refresh history if lifestyle result updates

    const handleLifestylePredict = async () => {
        if (!profile) return;
        try {
            const res = await axios.post('http://localhost:8000/predict/lifestyle', {
                age: profile.age,
                gender: profile.gender === 'Male' ? 2 : 1, // 1:Women, 2:Men
                height: profile.height,
                weight: profile.weight,
                ap_hi: 120, // Default normal if not measured
                ap_lo: 80,
                cholesterol: 1, // Default
                gluc: profile.glucose,
                smoke: profile.smoke,
                alco: profile.alco,
                active: profile.active
            }, { headers: { Authorization: `Bearer ${token}` } });
            setLifestyleResult(res.data);
        } catch (err) {
            alert("Lifestyle prediction failed: " + err.message);
        }
    };

    const handleSyntheticPredict = async () => {
        setSimLoading(true);
        try {
            const res = await axios.post('http://localhost:8000/predict/synthetic', syntheticInput);
            setSyntheticResult(res.data);
        } catch (err) {
            alert("Simulation failed");
        } finally {
            setSimLoading(false);
        }
    };

    if (loading) return <div className="container">Loading Dashboard...</div>;

    const lastAcutePrediction = history.find(h => h.model_type === 'acute');

    return (
        <div className="container" style={{ maxWidth: '1000px' }}>
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <div>
                    <h2>Welcome, {user?.full_name}</h2>
                    <p style={{ marginTop: '0.5rem', color: '#aaa' }}>Multi-Model Cardiac Health Dashboard</p>
                </div>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <button onClick={() => navigate('/profile')} style={{ background: '#0f3460', color: 'white', padding: '0.5rem 1rem', border: 'none', cursor: 'pointer' }}>
                        {profile ? 'Edit Profile' : 'Create Profile'}
                    </button>
                    <button onClick={logout} style={{ background: 'transparent', border: '1px solid #e94560', padding: '0.5rem 1rem', color: '#e94560', cursor: 'pointer' }}>Logout</button>
                </div>
            </header>

            {!profile && <div className="error-message" style={{ marginBottom: '2rem', textAlign: 'center' }}>
                ⚠️ You must complete your profile to use the prediction models.
            </div>}

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>

                {/* CARD 1: ACUTE RISK (UCI) */}
                <div className="model-card" style={{ background: '#16213e', padding: '1.5rem', borderRadius: '12px', borderTop: `4px solid ${lastAcutePrediction && lastAcutePrediction.risk_probability > 0.5 ? '#e94560' : '#4caf50'}` }}>
                    <h3>❤️ Acute Heart Attack Risk</h3>
                    <p style={{ fontSize: '0.9rem', color: '#888', marginBottom: '1rem' }}>Deep Neural Network (UCI Data)</p>

                    {lastAcutePrediction ? (
                        <div style={{ textAlign: 'center', margin: '1rem 0' }}>
                            <div style={{
                                fontSize: '1.1rem',
                                fontWeight: 'bold',
                                color: lastAcutePrediction.risk_probability > 0.5 ? '#e94560' : '#4caf50',
                                marginBottom: '0.5rem',
                                padding: '0.5rem',
                                border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '8px'
                            }}>
                                {lastAcutePrediction.risk_label}
                            </div>
                            <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{(lastAcutePrediction.risk_probability * 100).toFixed(1)}% Risk</p>
                            <small>{new Date(lastAcutePrediction.timestamp).toLocaleDateString()}</small>
                        </div>
                    ) : (
                        <p style={{ textAlign: 'center', padding: '1rem' }}>No assessment yet.</p>
                    )}

                    <button
                        onClick={() => navigate('/predict')}
                        disabled={!profile}
                        className="predict-btn"
                        style={{ width: '100%', opacity: !profile ? 0.5 : 1 }}
                    >
                        Check Acute Risk
                    </button>
                </div>

                {/* CARD 2: LONG-TERM LIFESTYLE */}
                <div className="model-card" style={{ background: '#16213e', padding: '1.5rem', borderRadius: '12px', borderTop: '4px solid #4caf50' }}>
                    <h3>🏃 Long-Term Health</h3>
                    <p style={{ fontSize: '0.9rem', color: '#888', marginBottom: '1rem' }}>Lifestyle Factors (Cardio Data)</p>

                    {lifestyleResult ? (
                        <div style={{ textAlign: 'center', margin: '1rem 0' }}>
                            <div style={{
                                fontSize: '1.1rem',
                                fontWeight: 'bold',
                                color: lifestyleResult.risk_probability > 0.5 ? '#e94560' : '#4caf50',
                                marginBottom: '0.5rem',
                                padding: '0.5rem',
                                border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '8px'
                            }}>
                                {lifestyleResult.risk_label}
                            </div>
                            <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{(lifestyleResult.risk_probability * 100).toFixed(1)}% Risk</p>
                        </div>
                    ) : (
                        <div style={{ padding: '1rem', textAlign: 'center', color: '#aaa' }}>
                            Ready to analyze based on your profile.
                        </div>
                    )}

                    <button
                        onClick={() => navigate('/predict/lifestyle')}
                        disabled={!profile}
                        className="predict-btn"
                        style={{ width: '100%', background: '#4caf50', opacity: !profile ? 0.5 : 1 }}
                    >
                        Predict Long-Term Risk
                    </button>
                </div>

                {/* CARD 3: SYNTHETIC SIMULATION */}
                <div className="model-card" style={{ background: '#16213e', padding: '1.5rem', borderRadius: '12px', borderTop: '4px solid #00bcd4' }}>
                    <h3>🧪 Experimental Sim</h3>
                    <p style={{ fontSize: '0.9rem', color: '#888', marginBottom: '1rem' }}>Synthetic Data Simulation</p>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', marginBottom: '1rem' }}>
                        <label>Stress (1-10) <input type="number" value={syntheticInput.stress_level} onChange={e => setSyntheticInput({ ...syntheticInput, stress_level: e.target.value })} style={{ width: '100%' }} /></label>
                        <label>Sleep (Hrs) <input type="number" value={syntheticInput.sleep_hours} onChange={e => setSyntheticInput({ ...syntheticInput, sleep_hours: e.target.value })} style={{ width: '100%' }} /></label>
                    </div>

                    {syntheticResult && (
                        <div style={{ textAlign: 'center', margin: '1rem 0', padding: '0.5rem', background: 'rgba(0,0,0,0.2)', borderRadius: '8px' }}>
                            <strong>Score: {(syntheticResult.risk_probability * 100).toFixed(1)}</strong>
                        </div>
                    )}

                    <button
                        onClick={handleSyntheticPredict}
                        className="predict-btn"
                        style={{ width: '100%', background: '#00bcd4' }}
                    >
                        {simLoading ? 'Simulating...' : 'Run Simulation'}
                    </button>
                </div>

            </div>

            {/* History Table */}
            <div style={{ marginTop: '3rem' }}>
                <h3>Global History</h3>
                {history.length === 0 ? <p>No history found.</p> : (
                    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
                        <thead>
                            <tr style={{ borderBottom: '1px solid #0f3460', textAlign: 'left' }}>
                                <th style={{ padding: '0.5rem' }}>Date</th>
                                <th style={{ padding: '0.5rem' }}>Model</th>
                                <th style={{ padding: '0.5rem' }}>Risk Level</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map(item => (
                                <tr key={item.id} style={{ borderBottom: '1px solid #16213e' }}>
                                    <td style={{ padding: '0.5rem' }}>{new Date(item.timestamp).toLocaleDateString()}</td>
                                    <td style={{ padding: '0.5rem', textTransform: 'capitalize' }}>{item.model_type || 'Acute'}</td>
                                    <td style={{ padding: '0.5rem', color: item.risk_label.includes('High') ? '#e94560' : '#4caf50' }}>{item.risk_label}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
