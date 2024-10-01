import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();


    const handleLogin = async(e) => {
        e.preventDefault();
        try {
            const response = await api.post('/auth/login', {username, password});
            localStorage.setItem('token', response.data.access_token); // Save JWT token
            navigate('/recipes'); // Redirect to recipe list page
        } catch(err) {
            setError('Invalid username or password');
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {error && <p>{error}</p>}
            <form onSubmit={handleLogin}>
                <input type='text' placeholder='Username' value={username} onChange={(e) => setUsername(e.target.value)} required/>
                <input type='password' placeholder='Password' value={password} onChange={(e) => setPassword(e.target.value)} required/>
                <button type='submit'>Login</button>
            </form>
        </div>
    );
}


export default Login;