import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const BillForm = () => {
    const [billNumber, setBillNumber] = useState(''); // bill number input state
    const [billData, setBillData] = useState(null); // fetched bill data state
    const navigate = useNavigate();

    // handle input change (allow typing in textbox)
    const handleInputChange = (e) => {
        setBillNumber(e.target.value);
    };

    // handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`/api/bill/${billNumber}`); // get bill data from API
            const text = await response.text(); // Get raw response text
            const data = JSON.parse(text); // Parse JSON
            setBillData(data);
            console.log('Navigating to dashboard with data:', data); // Log data before navigating
            navigate('/dashboard', { state: { billData: data } }); // Navigate to dashboard page with bill data
        } catch (error) {
            console.error('Error fetching bill data:', error);
        }
    };

    // Front page styling
    return (
        <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
            <h1>Bill Stance Classification</h1>
            <p>
                Enter a bill number to fetch its details and classify its stance as Republican, Democratic, or Middle.
            </p>
            <img src="placeholder-image-url.jpg" alt="Placeholder" style={{ width: '100%', height: 'auto' }} />
            <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
                <label>
                    Bill Number:
                    <input
                        type="text"
                        value={billNumber}
                        onChange={handleInputChange}
                        style={{ marginLeft: '10px', padding: '5px' }}
                    />
                </label>
                <button type="submit" style={{ marginLeft: '10px', padding: '5px 10px' }}>
                    Submit
                </button>
            </form>
        </div>
    );
};

export default BillForm;