import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import WeatherDashboard from './components/WeatherDashboard';
// Imports removed

// Placeholder for Login/Register if they don't exist yet
const LoginPlaceholder = () => <div><h2>Login Page</h2></div>;
const RegisterPlaceholder = () => <div><h2>Register Page</h2></div>;

function App() {
    return (
        <Router>
            <AuthProvider>
                <div className="App">
                    <Routes>
                        <Route path="/login" element={<LoginPlaceholder />} />
                        <Route path="/register" element={<RegisterPlaceholder />} />
                        <Route
                            path="/"
                            element={
                                <ProtectedRoute>
                                    <WeatherDashboard />
                                </ProtectedRoute>
                            }
                        />
                    </Routes>
                </div>
            </AuthProvider>
        </Router>
    );
}

export default App;
