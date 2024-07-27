import React from 'react';
import { useLocation } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';

const COLORS = ['#0088FE', '#FF8042', '#00C49F']; // Colors for pie chart

const BillDashboard = () => {
    const location = useLocation(); // access location object
    const { billData } = location.state || { billData: null };

    console.log('BillDashboard location.state:', location.state); // Log location state
    console.log('BillDashboard billData:', billData); // Log billData

    if (!billData) {
        return <div>No data available</div>; // display message when no data is available
    }

    const { title, stance } = billData; // destruct bill data

    // prep data for pie chart
    const data = [
        { name: 'Democrat', value: stance.democrat },
        { name: 'Republican', value: stance.republican },
        { name: 'Independent', value: stance.independent },
    ];

    // styling of dashboard
    return (
        <div style={{ marginTop: '20px' }}>
            <h2>{title}</h2>
            <PieChart width={400} height={400}>
                <Pie
                    data={data}
                    cx={200}
                    cy={200}
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                >
                    {data.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
                <Tooltip />
                <Legend />
            </PieChart>
        </div>
    );
};

export default BillDashboard;