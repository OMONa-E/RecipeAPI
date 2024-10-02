import './App.css';
import React from 'react';
import { BrowserRouter as Router, Router, Route, Routes } from 'react-router-dom';
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';
import Logout from './components/Auth/Logout';
import RecipeList from './components/Recipes/RecipeList';
import RecipeCreate from './components/Recipes/RecipeCreate';
import RecipeDetail from './components/Recipes/RecipeDetail';
import RecipeEdit from './components/Recipes/RecipeEdit';
import ProtectedRoute from './components/Auth/ProtectedRoute';



function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/logout" element={ <ProtectedRoute><Logout/></ProtectedRoute> } />
        <Route path="/recipes/create" element={ <ProtectedRoute><RecipeCreate/></ProtectedRoute> } />
        <Route path="/recipes" element={ <ProtectedRoute><RecipeList/></ProtectedRoute> } />
        <Route path="/recipes/:recipe_id" element={<ProtectedRoute><RecipeDetail/></ProtectedRoute> } />
        <Route path="/recipes/:recipe_id/edit" element={ <ProtectedRoute><RecipeEdit/></ProtectedRoute> } />
      </Routes>
    </Router>
  );
}

export default App;
