import React, { useState } from 'react';
import './App.css'; // Import the CSS file

function App() {
    const [passage, setPassage] = useState('');
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/answer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ passage, question }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            setAnswer(data.answer);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="app-container">
            <h1 className="app-title">Question Answering System</h1>
            <form className="app-form" onSubmit={handleSubmit}>
                <textarea
                    className="app-textarea"
                    value={passage}
                    onChange={(e) => setPassage(e.target.value)}
                    placeholder="Enter passage"
                />
                <input
                    className="app-input"
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question"
                />
                <button className="app-button" type="submit">Get Answer</button>
            </form>
            {answer && <div className="app-answer">Answer: {answer}</div>}
        </div>
    );
}

export default App;

