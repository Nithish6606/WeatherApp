import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders App component without crashing', () => {
    render(<App />);
    // Basic check to ensure something from the app renders. 
    // Adjust the text matcher based on your actual App content if needed.
    // For a pure smoke test, just rendering without error is a good start.
    // If App has a title "Weather Dashboard" or similar, we can check for it.
    // For now, we just check if the render function completes.
    expect(true).toBe(true);
});
