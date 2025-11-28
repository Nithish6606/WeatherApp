import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        primary_location: ''
    });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.confirmPassword) {
            setError("Passwords don't match");
            return;
        }

        try {
            await api.post('auth/register/', {
                username: formData.username,
                email: formData.email,
                password: formData.password,
                primary_location: formData.primary_location
            });
            navigate('/login');
        } catch (err) {
            console.error('Registration failed:', err);
            setError(err.response?.data?.detail || 'Registration failed. Please try again.');
        }
    };

    return (
        <div style={styles.container}>
            <div style={styles.card}>
                <h2 style={styles.title}>Register</h2>
                {error && <div style={styles.error}>{error}</div>}
                <form onSubmit={handleSubmit} style={styles.form}>
                    <div style={styles.inputGroup}>
                        <label style={styles.label}>Username</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            style={styles.input}
                            required
                        />
                    </div>
                    <div style={styles.inputGroup}>
                        <label style={styles.label}>Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            style={styles.input}
                            required
                        />
                    </div>
                    <div style={styles.inputGroup}>
                        <label style={styles.label}>Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            style={styles.input}
                            required
                        />
                    </div>
                    <div style={styles.inputGroup}>
                        <label style={styles.label}>Confirm Password</label>
                        <input
                            type="password"
                            name="confirmPassword"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            style={styles.input}
                            required
                        />
                    </div>
                    <div style={styles.inputGroup}>
                        <label style={styles.label}>Primary Location (City)</label>
                        <input
                            type="text"
                            name="primary_location"
                            value={formData.primary_location}
                            onChange={handleChange}
                            style={styles.input}
                            placeholder="e.g., London"
                        />
                    </div>
                    <button type="submit" style={styles.button}>Register</button>
                </form>
                <p style={styles.footer}>
                    Already have an account? <Link to="/login" style={styles.link}>Login</Link>
                </p>
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#f0f2f5',
        padding: '2rem 0',
    },
    card: {
        backgroundColor: 'white',
        padding: '2rem',
        borderRadius: '8px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        width: '100%',
        maxWidth: '400px',
    },
    title: {
        textAlign: 'center',
        marginBottom: '1.5rem',
        color: '#333',
    },
    error: {
        backgroundColor: '#fee2e2',
        color: '#dc2626',
        padding: '0.75rem',
        borderRadius: '4px',
        marginBottom: '1rem',
        textAlign: 'center',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
    },
    inputGroup: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem',
    },
    label: {
        fontSize: '0.875rem',
        fontWeight: '500',
        color: '#4b5563',
    },
    input: {
        padding: '0.75rem',
        borderRadius: '4px',
        border: '1px solid #d1d5db',
        fontSize: '1rem',
    },
    button: {
        backgroundColor: '#2563eb',
        color: 'white',
        padding: '0.75rem',
        borderRadius: '4px',
        border: 'none',
        fontSize: '1rem',
        fontWeight: '500',
        cursor: 'pointer',
        marginTop: '0.5rem',
    },
    footer: {
        textAlign: 'center',
        marginTop: '1.5rem',
        fontSize: '0.875rem',
        color: '#6b7280',
    },
    link: {
        color: '#2563eb',
        textDecoration: 'none',
    },
};

export default Register;
