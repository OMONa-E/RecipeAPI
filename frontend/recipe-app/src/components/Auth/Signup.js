import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';


function Signup() {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        role: '',
        allergies: '',
        dislikes: '',
        hard_to_get: '',
        family_size: 0,
        aveg_intake_person: 0
    });
    const [error, setError] = useState(null);
    const navigate = useNavigate();


    const handleSignup = async(e) => {
        e.preventDefault();
        try {
            await api.post('/auth/users', formData);
            navigate('/login'); // Redirect to login page after successful signup
        } catch (err) {
            setError('Sigup failed. Please try again.');
        }
    };

    
    return (
        <div>
            <h2>Signup</h2>
            {error && <p>{error}</p>}
            <form onSubmit={handleSignup}>
                <input type="text" placeholder="Username" value={formData.username} onChange={(e) => setFormData({ ...formData, username: e.target.value })} required />

                <input type="password" placeholder="Password" value={formData.password} onChange={(e) => setFormData({ ...formData, password: e.target.value })} required />

                <input type="text" placeholder="Role" value={formData.role} onChange={(e) => setFormData({ ...formData, role: e.target.value })} />

                <input type="text" placeholder="Allergies" value={formData.allergies} onChange={(e) => setFormData({ ...formData, allergies: e.target.value })} />

                <input type="text" placeholder="Dislikes" value={formData.dislikes} onChange={(e) => setFormData({ ...formData, dislikes: e.target.value })} />

                <input type="number" placeholder="Family Size" value={formData.family_size} onChange={(e) => setFormData({ ...formData, family_size: e.target.value })} />
                
                <input type="number" placeholder="Average intake per person" value={formData.aveg_intake_person} onChange={(e) => setFormData({ ...formData, aveg_intake_person: e.target.value })} />
                <button type="submit">Signup</button>
            </form>
        </div>
    );
}


export default Signup;