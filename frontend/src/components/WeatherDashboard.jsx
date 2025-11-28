import React, { useState, useEffect } from 'react';
import api from '../services/api';

const WeatherDashboard = () => {
    const [weatherData, setWeatherData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [location, setLocation] = useState(null);

    const fetchWeather = async (lat, lon) => {
        try {
            setLoading(true);
            setError(null);
            // Endpoint: GET /weather/current/?lat={lat}&lon={lon}
            // Note: The task said GET /weather/?lat... but previous steps defined /api/weather/current/
            // I will use the correct endpoint defined in urls.py: weather/current/
            const response = await api.get(`weather/current/?lat=${lat}&lon=${lon}`);
            setWeatherData(response.data);
        } catch (err) {
            console.error(err);
            setError('Failed to fetch weather data. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (!navigator.geolocation) {
            setError('Geolocation is not supported by your browser');
            setLoading(false);
            return;
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                setLocation({ lat: latitude, lon: longitude });
                fetchWeather(latitude, longitude);
            },
            (err) => {
                console.error(err);
                setError('Location access required for local weather');
                setLoading(false);
            }
        );
    }, []);

    const handleRetry = () => {
        setLoading(true);
        setError(null);
        if (!navigator.geolocation) {
            setError('Geolocation is not supported by your browser');
            setLoading(false);
            return;
        }
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                setLocation({ lat: latitude, lon: longitude });
                fetchWeather(latitude, longitude);
            },
            (err) => {
                console.error(err);
                setError('Location access required for local weather');
                setLoading(false);
            }
        );
    };

    if (loading) {
        return <div style={styles.container}>Locating your farm...</div>;
    }

    if (error) {
        return (
            <div style={styles.container}>
                <p style={styles.error}>{error}</p>
                <button onClick={handleRetry} style={styles.button}>Retry</button>
            </div>
        );
    }

    return (
        <div style={styles.dashboard}>
            <h2>Current Weather</h2>
            {weatherData && (
                <div style={styles.card}>
                    <p><strong>Source:</strong> {weatherData?.source}</p>
                    <p><strong>Temperature:</strong> {weatherData?.temp}°C</p>
                    <p><strong>Humidity:</strong> {weatherData?.humidity}%</p>
                    <p><strong>Wind Speed:</strong> {weatherData?.wind_speed} m/s</p>
                    <p><strong>Condition:</strong> {weatherData?.description}</p>
                </div>
            )}
        </div>
    );
};

const styles = {
    container: {
        padding: '20px',
        textAlign: 'center',
        fontFamily: 'Arial, sans-serif',
    },
    dashboard: {
        padding: '20px',
        maxWidth: '600px',
        margin: '0 auto',
        fontFamily: 'Arial, sans-serif',
    },
    card: {
        border: '1px solid #ddd',
        borderRadius: '8px',
        padding: '20px',
        marginTop: '20px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        backgroundColor: '#f9f9f9',
    },
    error: {
        color: '#d32f2f',
        marginBottom: '10px',
        fontWeight: 'bold',
    },
    button: {
        padding: '10px 20px',
        backgroundColor: '#1976d2',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px',
    }
};

export default WeatherDashboard;
