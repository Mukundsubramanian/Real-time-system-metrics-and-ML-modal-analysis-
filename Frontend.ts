import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from
'recharts';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
const generateMetricsData = () => {
return {
timestamp: new Date().toISOString(),
cpu: Math.random() * 100,
memory: Math.random() * 100,
disk: Math.random() * 100,
};
};
const generateLogEntry = () => {
const actions = ['Started', 'Stopped', 'Restarted', 'Updated', 'Errored'];
const services = ['Web Server', 'Database', 'Cache', 'Worker', 'Scheduler'];
const action = actions[Math.floor(Math.random() * actions.length)];
const service = services[Math.floor(Math.random() * services.length)];
return `${new Date().toISOString()} - ${action} ${service}`;
};
const SystemMetricsAndLog = () => {
const [metricsData, setMetricsData] = useState([]);
const [logEntries, setLogEntries] = useState([]);
useEffect(() => {
const interval = setInterval(() => {
setMetricsData(prevData => [...prevData.slice(-20), generateMetricsData()]);
setLogEntries(prevEntries => [...prevEntries.slice(-5), generateLogEntry()]);
}, 1000);
return () => clearInterval(interval);
}, []);
return (
<div className="p-4 space-y-4">
<Card>
<CardHeader>System Metrics</CardHeader>
<CardContent>
<ResponsiveContainer width="100%" height={300}>
<LineChart data={metricsData}>
<CartesianGrid strokeDasharray="3 3" />
<XAxis dataKey="timestamp" />
<YAxis />
<Tooltip />
<Line type="monotone" dataKey="cpu" stroke="#8884d8" name="CPU" />
<Line type="monotone" dataKey="memory" stroke="#82ca9d" name="Memory" />
<Line type="monotone" dataKey="disk" stroke="#ffc658" name="Disk" />
</LineChart>
</ResponsiveContainer>
</CardContent>
</Card>
<Card>
<CardHeader>Live Log</CardHeader>
<CardContent>
<div className="bg-gray-100 p-4 rounded-lg">
{logEntries.map((entry, index) => (
<div key={index} className="mb-2 p-2 bg-white rounded shadow">
{entry}
</div>
))}
</div>
</CardContent>
</Card>
</div>
);
};
export default SystemMetricsAndLog;