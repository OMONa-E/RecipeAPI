import React, { useEffect, useState } from 'react';
import api from '../../services/api';
import { Link } from 'react-router-dom';



function RecipeList() {
    const [recipes, setRecipes] = useState([]);

    useEffect(
        () => {
            const fetchRecipes = async() => {
                try {
                    const response = await api.get('/recipes');
                    setRecipes(response.data)
                } catch (err) {
                    console.error('Failed to fetch recipes:', err);
                }
            };
            fetchRecipes();
        }, []
    );

    return (
        <div>
            <h2>Recipes</h2>
            <ul>
                {
                    recipes.map(
                        (recipe) => (
                            <li key={recipe.id}>
                                <Link to={`/recipes/${recipe.id}`}>{recipe.name}</Link> {/* Link to detail page */}                                
                            </li>
                        )
                    )
                }
            </ul>
        </div>
    )
}


export default RecipeList;