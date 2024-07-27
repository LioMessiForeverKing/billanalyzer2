import React from 'react';
import { useLocation } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import './BillDashboard.css'; // Import the CSS file

const COLORS = ['url(#democratGradient)', 'url(#republicanGradient)', 'url(#independentGradient)']; // Colors for pie chart

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
        <div className="dashboard-container">
            <div className="title-container">
                <h2 className="dashboard-title">{title}</h2>
            </div>
            <div className="container-wrapper">
                <div className="chart-container">
                    <PieChart width={400} height={400}>
                        <defs>
                            <linearGradient id="democratGradient" x1="0" y1="0" x2="1" y2="0">
                                <stop offset="0%" stopColor="#03E4DF" />
                                <stop offset="100%" stopColor="#0090FF" />
                            </linearGradient>
                            <linearGradient id="republicanGradient" x1="0" y1="0" x2="1" y2="0">
                                <stop offset="0%" stopColor="#a81b23" />
                                <stop offset="100%" stopColor="#ff3741" />
                            </linearGradient>
                            <linearGradient id="independentGradient" x1="0" y1="0" x2="1" y2="0">
                                <stop offset="0%" stopColor="#0EF691" />
                                <stop offset="100%" stopColor="#089B5C" />
                            </linearGradient>
                        </defs>
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
                <div className="summary-container">
                    <h2 className="summary-title">Summary</h2>
                    {/* Summary content will be added here */}
                </div>
            </div>
        </div>
    );
};

export default BillDashboard;