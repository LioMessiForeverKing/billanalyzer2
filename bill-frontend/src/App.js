import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import BillForm from './components/BillForm';
import BillDashboard from './components/BillDashboard';

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/" element={<BillForm />} />
                    <Route path="/dashboard" element={<BillDashboard />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;