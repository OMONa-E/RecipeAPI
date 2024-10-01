import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';



function Logout() {
    const navigate = useNavigate();

    useEffect(
        () => {
            const logout = async() => {
                try {
                    await api.post('/auth/logout');
                    localStorage.removeItem('token'); // Clear the token
                    navigate('/login') // Redirect to login 
                } catch(err) {
                    console.error('Logout failed:', err);
                }
            };
            
            logout();
        }, [navigate]
    );

    return (
        <div>Logging out.....</div>
    );
}


export default Logout;