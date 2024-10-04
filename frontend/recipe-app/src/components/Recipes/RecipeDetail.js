import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../services/api';
import PinCreate from '../Pins/PinCreate';



function RecipeDetail() {
    const { recipe_id } = useParams(); // Extract recipe_id from URL params
    const [recipe, setRecipe] = useState(null); // Holds the recipe data
    const [error, setError] = useState(null); // Error handler
    const navigate = useNavigate(); // Handle redirect

    // Fetch recipe details on component mount
    useEffect(
        () => {
            const fetchRecipe = async() => {
                try {
                    const response = await api.get(`/recipes/${recipe_id}`);
                    setRecipe(response.data); // Store the rcipe data in state
                } catch(err) {
                    setError('Failed to fetch recipe.');
                }
            };
            fetchRecipe(); // Call the functionto fetch data
        }, [recipe_id]
    );

    // Handle dlete recipe
    const handleDelete = async() => {
        if (window.confirm('Are you sure you want to delete this recipe?')) {
            try {
                await api.delete(`/recipes/${recipe_id}`);
                navigate(`/recipes`) // redirect to recipe list after deletion
            } catch (err) {
                setError('Failed to dlete the recipe.');
            }
        }
    };

    if (error) {
        return <p>{error}</p>; // Display error message
    }

    if (!recipe) {
        return <p>Loading....</p>; // Show a loading message untill the recipe is fetched
    }

    return (
        <div>
            <h2>{recipe.name}</h2>
            <p><strong>Category:</strong> {recipe.category}</p>
            <p><strong>Ingredients:</strong></p>
            <ul>
                {
                    Object.entries(recipe.ingredients).map(
                        ([item, details]) => (
                            <li key={item}>{item}: {details.quantity} - cost: {details.cost}units</li>
                        )
                    )
                }
            </ul>
            <p><strong>Instructions:</strong> {recipe.instructions}</p>
            <p><strong>Total Cost:</strong> {recipe.total_cost_ingred}units</p>
            <br></br>
            {/* Delete button */}
            <button onClick={handleDelete}>Delete Recipe</button>
            <br></br>
            <hr></hr>
            <br></br>
            {/* Pin/Comment section */}
            <h3>Pins</h3>
            <PinCreate />
        </div>
    );
}


export default RecipeDetail;