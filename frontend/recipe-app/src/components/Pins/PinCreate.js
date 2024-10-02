import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../services/api';


function PinCreate() {
    const { recipe_id } = useParams(); // Get recipe_id rom URL
    const [comment, setComment] = useState(''); // Hold the comment input
    const [error, setError] = useState(null); // Error handling
    const [success, setSuccess] = useState(null); // For success feedback

    // Handle form submit
    const handleSubmit = async(e) => {
        e.preventDefault();
        try {
            await api.post(`/recipes/${recipe_id}/pin`, { content: comment }); // Submit the comment
            setSuccess('Comment added successfully.');
            setComment(''); // Clear the comment input
        } catch (err) {
            setError('Failed to add comment/pin.');
        }
    };

    return (
        <div>
            <h3>Add a Comment</h3>
            {error && <p>{error}</p>}
            {success && <p>{success}</p>}
            <form onSubmit={handleSubmit}>
                <textarea name="comment" placeholder="Write your comment" value={comment} onChange={(e) => setComment(e.target.value)} />
                <button type="submit">Pin</button>
            </form>
        </div>
    );
}


export default PinCreate;