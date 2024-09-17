import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar,
Cell } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
const generateData = (iterations) => {
return Array.from({ length: iterations }, (_, i) => ({
iteration: i + 1,
loss: Math.max(0, 1 - i * 0.01 + Math.random() * 0.1),
accuracy: Math.min(1, i * 0.01 + Math.random() * 0.1),
valLoss: Math.max(0, 1.1 - i * 0.009 + Math.random() * 0.15),
valAccuracy: Math.min(1, i * 0.009 + Math.random() * 0.15),
learningRate: 0.001 * Math.pow(0.95, Math.floor(i / 10)),
}));
};
const generateConfusionMatrix = () => {
return [
{ name: 'True Negative', value: Math.floor(Math.random() * 100) },
{ name: 'False Positive', value: Math.floor(Math.random() * 20) },
{ name: 'False Negative', value: Math.floor(Math.random() * 20) },
{ name: 'True Positive', value: Math.floor(Math.random() * 100) },
];
};
const MLMetricsDashboard = () => {
const [data, setData] = useState([]);
const [iterations, setIterations] = useState(100);
const [confusionMatrix, setConfusionMatrix] = useState([]);
const [selectedMetric, setSelectedMetric] = useState('loss');
useEffect(() => {
setData(generateData(iterations));
setConfusionMatrix(generateConfusionMatrix());
}, [iterations]);
const metricColors = {
loss: '#8884d8',
accuracy: '#82ca9d',
valLoss: '#ffc658',
valAccuracy: '#ff8042',
learningRate: '#8dd1e1',
};
return (
<div className="p-4 max-w-6xl mx-auto">
<h1 className="text-2xl font-bold mb-4">ML Model Training Dashboard</h1>
<Tabs defaultValue="metrics" className="w-full mb-4">
<TabsList>
<TabsTrigger value="metrics">Metrics</TabsTrigger>
<TabsTrigger value="confusion">Confusion Matrix</TabsTrigger>
</TabsList>
<TabsContent value="metrics">
<div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
<Card>
<CardHeader>
<CardTitle>Training Metrics</CardTitle>
</CardHeader>
<CardContent>
<ResponsiveContainer width="100%" height={300}>
<LineChart data={data}>
<CartesianGrid strokeDasharray="3 3" />
<XAxis dataKey="iteration" />
<YAxis />
<Tooltip />
<Legend />
<Line type="monotone" dataKey="loss" stroke={metricColors.loss} name="Loss" />
<Line type="monotone" dataKey="accuracy" stroke={metricColors.accuracy}
name="Accuracy" />
</LineChart>
</ResponsiveContainer>
</CardContent>
</Card>
<Card>
<CardHeader>
<CardTitle>Validation Metrics</CardTitle>
</CardHeader>
<CardContent>
<ResponsiveContainer width="100%" height={300}>
<LineChart data={data}>
<CartesianGrid strokeDasharray="3 3" />
<XAxis dataKey="iteration" />
<YAxis />
<Tooltip />
<Legend />
<Line type="monotone" dataKey="valLoss" stroke={metricColors.valLoss} name="Validation
Loss" />
<Line type="monotone" dataKey="valAccuracy" stroke={metricColors.valAccuracy}
name="Validation Accuracy" />
</LineChart>
</ResponsiveContainer>
</CardContent>
</Card>
</div>
<Card>
<CardHeader>
<CardTitle>Learning Rate</CardTitle>
</CardHeader>
<CardContent>
<ResponsiveContainer width="100%" height={200}>
<LineChart data={data}>
<CartesianGrid strokeDasharray="3 3" />
<XAxis dataKey="iteration" />
<YAxis />
<Tooltip />
<Legend />
<Line type="monotone" dataKey="learningRate" stroke={metricColors.learningRate} />
</LineChart>
</ResponsiveContainer>
</CardContent>
</Card>
<Card className="mt-4">
<CardHeader>
<CardTitle>Log Visualization</CardTitle>
</CardHeader>
<CardContent>
<Select onValueChange={setSelectedMetric} defaultValue={selectedMetric}>
<SelectTrigger className="w-[180px] mb-2">
<SelectValue placeholder="Select metric" />
</SelectTrigger>
<SelectContent>
<SelectItem value="loss">Loss</SelectItem>
<SelectItem value="accuracy">Accuracy</SelectItem>
<SelectItem value="valLoss">Validation Loss</SelectItem>
<SelectItem value="valAccuracy">Validation Accuracy</SelectItem>
<SelectItem value="learningRate">Learning Rate</SelectItem>
</SelectContent>
</Select>
<div className="bg-gray-100 p-4 rounded-md h-40 overflow-y-auto">
{data.map((item, index) => (
<div key={index} className="text-sm">
Iteration {item.iteration}: {selectedMetric} = {item[selectedMetric].toFixed(6)}
</div>
))}
</div>
</CardContent>
</Card>
</TabsContent>
<TabsContent value="confusion">
<Card>
<CardHeader>
<CardTitle>Confusion Matrix</CardTitle>
</CardHeader>
<CardContent>
<ResponsiveContainer width="100%" height={300}>
<BarChart data={confusionMatrix} layout="vertical">
<CartesianGrid strokeDasharray="3 3" />
<XAxis type="number" />
<YAxis dataKey="name" type="category" />
<Tooltip />
<Legend />
<Bar dataKey="value" fill="#8884d8">
{confusionMatrix.map((entry, index) => (
<Cell key={`cell-${index}`} fill={index % 2 === 0 ? '#82ca9d' : '#8884d8'} />
))}
</Bar>
</BarChart>
</ResponsiveContainer>
</CardContent>
</Card>
</TabsContent>
</Tabs>
<div className="mt-4">
<label htmlFor="iterations" className="block text-sm font-medium text-gray-700">
Number of Iterations:
</label>
<input
type="number"
id="iterations"
value={iterations}
onChange={(e) => setIterations(Number(e.target.value))}
className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300
focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
/>
</div>
</div>
);
};
export default MLMetricsDashboard;
