import { useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import '../index.css';

const Profile = () => {
    const { token } = useContext(AuthContext);
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [formData, setFormData] = useState({
        age: 30,
        gender: 'Male',
        height: 170,
        weight: 70,
        medical_conditions: '',
        stress_level: 5,
        glucose: 1,
        smoke: 0,
        alco: 0,
        active: 1
    });

    useEffect(() => {
        const fetchProfile = async () => {
            if (!token) return;
            try {
                const res = await axios.get('http://localhost:8000/profile/', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                if (res.data) {
                    setFormData({
                        age: res.data.age,
                        gender: res.data.gender,
                        height: res.data.height,
                        weight: res.data.weight,
                        medical_conditions: res.data.medical_conditions || '',
                        stress_level: res.data.stress_level,
                        glucose: res.data.glucose || 1,
                        smoke: res.data.smoke || 0,
                        alco: res.data.alco || 0,
                        active: res.data.active || 1
                    });
                }
            } catch (err) {
                console.log("No profile found or error fetching", err);
            } finally {
                setLoading(false);
            }
        };
        fetchProfile();
    }, [token]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:8000/profile/', formData, {
                headers: { Authorization: `Bearer ${token}` }
            });
            alert('Profile saved successfully!');
            navigate('/dashboard');
        } catch (err) {
            console.error(err);
            alert('Failed to save profile.');
        }
    };

    if (loading) return <div className="container">Loading...</div>;

    return (
        <div className="container" style={{ maxWidth: '600px' }}>
            <header>
                <h2>My Health Profile</h2>
                <p>Complete for Accurate Multi-Model Predictions</p>
            </header>
            <form onSubmit={handleSubmit} className="risk-form">
                <div className="form-grid">
                    <div className="input-group">
                        <label>Age</label>
                        <input name="age" type="number" value={formData.age} onChange={handleChange} required />
                    </div>

                    <div className="input-group">
                        <label>Gender</label>
                        <select name="gender" value={formData.gender} onChange={handleChange}>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                        </select>
                    </div>

                    <div className="input-group">
                        <label>Height (cm)</label>
                        <input name="height" type="number" value={formData.height} onChange={handleChange} required />
                    </div>

                    <div className="input-group">
                        <label>Weight (kg)</label>
                        <input name="weight" type="number" value={formData.weight} onChange={handleChange} required />
                    </div>

                    <div className="input-group">
                        <label>Stress Level (1-10)</label>
                        <input name="stress_level" type="number" min="1" max="10" value={formData.stress_level} onChange={handleChange} required />
                    </div>

                    <div className="input-group">
                        <label>Glucose Level</label>
                        <select name="glucose" value={formData.glucose} onChange={handleChange}>
                            <option value={1}>Normal</option>
                            <option value={2}>Above Normal</option>
                            <option value={3}>Well Above Normal</option>
                        </select>
                    </div>

                    <div className="input-group">
                        <label>Smoking Status</label>
                        <select name="smoke" value={formData.smoke} onChange={handleChange}>
                            <option value={0}>Non-Smoker</option>
                            <option value={1}>Smoker</option>
                        </select>
                    </div>

                    <div className="input-group">
                        <label>Alcohol Intake</label>
                        <select name="alco" value={formData.alco} onChange={handleChange}>
                            <option value={0}>No / Rare</option>
                            <option value={1}>Regular</option>
                        </select>
                    </div>

                    <div className="input-group">
                        <label>Physical Activity</label>
                        <select name="active" value={formData.active} onChange={handleChange}>
                            <option value={1}>Active</option>
                            <option value={0}>Inactive</option>
                        </select>
                    </div>
                </div>

                <div className="input-group" style={{ marginTop: '1rem' }}>
                    <label>Medical Conditions (Optional)</label>
                    <textarea
                        name="medical_conditions"
                        value={formData.medical_conditions}
                        onChange={handleChange}
                        placeholder="e.g. Diabetes, Hypertension..."
                        style={{ width: '100%', padding: '0.8rem', background: '#16213e', color: 'white', border: '1px solid #0f3460' }}
                    />
                </div>

                <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
                    <button type="submit" className="predict-btn">Save Profile</button>
                    <button type="button" onClick={() => navigate('/dashboard')} style={{ background: 'transparent', border: '1px solid #e94560', color: '#e94560', padding: '1rem', cursor: 'pointer', flex: 1 }}>Cancel</button>
                </div>
            </form>
        </div>
    );
};

export default Profile;
