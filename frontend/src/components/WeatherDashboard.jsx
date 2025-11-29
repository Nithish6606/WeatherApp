import React, { useState, useEffect } from 'react';
import { FaThermometerHalf, FaWind } from 'react-icons/fa';
import { WiHumidity } from 'react-icons/wi';
import styles from './WeatherDashboard.module.css';

const WeatherDashboard = () => {
    const [weatherData, setWeatherData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [location, setLocation] = useState(null);

    const fetchWeather = async (lat, lon) => {
        try {
            setLoading(true);
            setError(null);
            // Use native fetch to avoid Axios/CORS preflight issues for this public endpoint
            const response = await fetch(`/api/weather/current/?lat=${lat}&lon=${lon}`);

            if (!response.ok) {
                throw new Error(`Server Error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            setWeatherData(data);
        } catch (err) {
            console.error("Weather fetch error:", err);
            setError(`Failed to fetch weather data. ${err.message}`);
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
        return (
            <div className={styles.container}>
                <div className={styles.loadingContainer}>
                    <div className={styles.loadingText}>Locating your farm...</div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className={styles.container}>
                <div className={styles.errorContainer}>
                    <div className={styles.errorBox}>{error}</div>
                    <button onClick={handleRetry} className={styles.retryButton}>Retry</button>
                </div>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <div className={styles.dashboard}>
                <h2 className={styles.title}>Current Weather</h2>
                {weatherData && (
                    <div className={styles.card}>
                        <div className={styles.header}>
                            <span className={styles.source}>Source: {weatherData?.source}</span>
                        </div>

                        <div className={styles.mainInfo}>
                            <div className={styles.temperature}>
                                <FaThermometerHalf className={styles.tempIcon} />
                                {weatherData?.temp}°C
                            </div>
                            <div className={styles.condition}>{weatherData?.description}</div>
                        </div>

                        <div className={styles.detailsGrid}>
                            <div className={styles.detailItem}>
                                <div className={styles.icon}><WiHumidity /></div>
                                <div>
                                    <span className={styles.label}>Humidity</span>
                                    <div className={styles.value}>{weatherData?.humidity}%</div>
                                </div>
                            </div>
                            <div className={styles.detailItem}>
                                <div className={styles.icon}><FaWind /></div>
                                <div>
                                    <span className={styles.label}>Wind</span>
                                    <div className={styles.value}>{weatherData?.wind_speed} m/s</div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default WeatherDashboard;
