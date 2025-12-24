import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import '../index.css';

const Signup = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        full_name: '',
        phone_number: ''
    });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await axios.post('http://localhost:8000/auth/signup', formData);
            alert('Account created! Please login.');
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.detail || 'Signup failed.');
        }
    };

    return (
        <div className="container" style={{ maxWidth: '400px' }}>
            <header>
                <h2>Sign Up</h2>
            </header>
            <form onSubmit={handleSubmit} className="risk-form">
                <div className="input-group">
                    <label>Full Name</label>
                    <input name="full_name" value={formData.full_name} onChange={handleChange} required />
                </div>
                <div className="input-group">
                    <label>Email</label>
                    <input name="email" type="email" value={formData.email} onChange={handleChange} required />
                </div>
                <div className="input-group">
                    <label>Phone (Optional)</label>
                    <input name="phone_number" value={formData.phone_number} onChange={handleChange} />
                </div>
                <div className="input-group">
                    <label>Password</label>
                    <input name="password" type="password" value={formData.password} onChange={handleChange} required />
                </div>

                {error && <div className="error-message">{error}</div>}

                <button type="submit" className="predict-btn">Sign Up</button>
                <p style={{ textAlign: 'center', marginTop: '1rem' }}>
                    Already have an account? <Link to="/login" style={{ color: '#e94560' }}>Login</Link>
                </p>
            </form>
        </div>
    );
};

export default Signup;
