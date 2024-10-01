import './App.css';
import React from 'react';
import { BrowserRouter as Router, Router, Route, Routes } from 'react-router-dom';
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';
import Logout from './components/Auth/Logout';
import RecipeList from './components/Recipes/RecipeList';



function App() {
  return (
    <Router>
      <Routes>
        <Route path='/login' element={<Login/>} />
        <Route path='/signup' element={<Signup/>} />
        <Route path='/logout' element={<Logout/>} />
        <Route path='/recipes' element={<RecipeList/>} />
        {/* TODO: Add more routes */}
      </Routes>
    </Router>
  );
}

export default App;
