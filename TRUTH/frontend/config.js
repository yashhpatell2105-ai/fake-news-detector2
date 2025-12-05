// TRUTH Frontend Configuration
// Update this URL when deploying the backend to a remote server

// Local development (Flask running on localhost:5000)
// window.API_BASE = 'http://localhost:5000/api';

// Production (Render backend example)
window.API_BASE = 'https://truth-backend.onrender.com/api'; // REPLACE WITH YOUR RENDER BACKEND URL

// Fallback: if not set, use relative URL (only works if frontend & backend are on same domain)
if (!window.API_BASE) {
    window.API_BASE = '/api';
}
