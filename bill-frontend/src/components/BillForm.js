import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './BillForm.css'; // Import the CSS file for styling

const BillForm = () => {
    const [congress, setCongress] = useState('');
    const [billNumber, setBillNumber] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:5000/fetch-bill', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ congress, bill_num: billNumber }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const billData = await response.json();
            console.log('API Response:', billData);
            navigate('/dashboard', { state: { billData, congressType: congress, summary: billData.summary, classification: billData.classification } }); // Pass classification
        } catch (error) {
            console.error('Error fetching bill data:', error);
            setError('Failed to fetch bill data. Please try again.');
        }
    };

    return (
        <div className="bill-form-container">
            <h1 className="bill-title">Bill Information Form</h1>
            <div className="container-wrapper">
                <div className="about-text">
                    <h2 className="about-title">About</h2>
                    <p>Recent observations have indicated a decline in general public awareness of bills passed in Congress. 
                        This trend is attributed by many to the overshadowing of some bills by others in greater popularity in 
                        the media and public interest. For Example, surveys by the Pew Research Center indicate that many Americans 
                        are not fully aware of government procedures and specific legislative actions. Furthermore, there is a lack 
                        of awareness among the public regarding which party endorses or proposes particular bills. To address this 
                        issue, we have developed a machine learning model to provide insights into the political leanings associated 
                        with each bill. The model, trained on historical bill data, achieves a relatively high accuracy of 67%. With 
                        the help of this model, we intend to foster greater public participation in the democratic process through 
                        increased awareness.</p>
                </div>
                <div className="main-content-container">
                    <div className="about-container">
                        <p>Enter the Congress number and Bill number to fetch the bill details.</p>
                    </div>
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <input
                                type="text"
                                value={congress}
                                onChange={(e) => setCongress(e.target.value)}
                                placeholder="Enter Congress Number"
                            />
                        </div>
                        <div className="form-group">
                            <input
                                type="text"
                                value={billNumber}
                                onChange={(e) => setBillNumber(e.target.value)}
                                placeholder="Enter Bill Number"
                            />
                        </div>
                        <button type="submit">Submit</button>
                    </form>
                    {error && <div style={{ color: 'red' }}>{error}</div>}
                </div>
            </div>
        </div>
    );
};

export default BillForm;