import React from "react";
import { Navigate } from "react-router-dom";


// Component to protect routes that require authentication
const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('token') // Check if JWT token exists
    return token ? children : <Navigate to={`/login`} /> // If not logged in, redirect to login
}


export default ProtectedRoute;