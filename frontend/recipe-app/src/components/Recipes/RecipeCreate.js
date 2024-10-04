import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';



function RecipeCreate() {
    // State variable to store input data 
    const [formData, setFormData] = useState(
        {
            name: '',
            ingredients: '', // To be JSON string later
            instructions: '',
            category: '' 
        }        
    );
    const [error, setError] = useState(null); // Error handling
    const navigate = useNavigate(); // Redirect to another after submit

    // Form submission handler
    const handleSubmit = async(e) => {
        e.preventDefault();
        
        try {
            // Convert the ingredients into JSON format
            const ingredientsJson = JSON.parse(formData.ingredients); 
            const payload = {
                ...formData,
                ingredients: ingredientsJson // Send JSON object 
            };

            await api.post('/recipes', payload); // Make POST request to create the recipe
            navigate('/recipes'); // Redirect to recipe list page after successful creation - GET
        } catch (err) {
            setError('Failed to create recipe. Ensure ingredients are in valid JSON format.');
        }
    };

    // Handle input changes
    const handleChange = (e) => {
        setFormData(
            {
                ...formData,
                [e.target.name]: e.target.value
            }
        );
    };

    return (
        <div>
            <h2>Create Recipe</h2>
            {error && <p>{error}</p>} {/* Display error */}
            <form onSubmit={handleSubmit}>
                <input type="text" name="name" placeholder="Recipe Name" value={formData.name} onChange={handleChange} required />
                
                <input type="text" name="category" placeholder="Category (e.g., Dessert, Breakfast)" value={formData.category} onChange={handleChange} />
                
                <textarea name="ingredients" placeholder='Ingredients (JSON format e.g {"flour": {"quantity": 0, "cost": 0.0}})' value={formData.ingredients} onChange={handleChange} required />
                
                <textarea name="instructions" placeholder="Instructions" value={formData.instructions} onChange={handleChange} required />
                <button type="submit">Create Recipe</button>
            </form>
        </div>
    );
}


export default RecipeCreate;