import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../services/api';



function RecipeEdit() {
    const { recipe_id } = useParams(); // Get the recipe_id from URL
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

    // Fetch the existing recipe data when component loads
    useEffect(
        () => {
            const fetchRecipe = async() => {
                try {
                    const response = await api.get(`/recipes/${recipe_id}`);
                    const recipe = response.data;
                    setFormData( // prepopulate our form
                        {
                            name: recipe.name,
                            ingredients: JSON.stringify(recipe.ingredients, null, 2),
                            instructions: recipe.instructions,
                            category: recipe.category
                        }
                    );
                } catch (err) {
                    setError('Failed to load recipe data.');
                }
            };
            fetchRecipe();
        }, [recipe_id]
    );

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

            await api.put(`/recipes/${recipe_id}`, payload); // Make PUT request to update the recipe
            navigate(`/recipes/${recipe_id}`); // Redirect to recipe detail page after successful upadate - GET
        } catch (err) {
            setError('Failed to update recipe. Ensure ingredients are in valid JSON format.');
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

    if (error) {
        return <p>{error}</p>
    }

    return (
        <div>
            <h2>Edit Recipe</h2>
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


export default RecipeEdit;