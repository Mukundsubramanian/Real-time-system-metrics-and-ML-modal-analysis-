document.addEventListener('DOMContentLoaded', () => {
    // Initialize charts
    const charts = {
        cpu: Plotly.newPlot('cpu-chart', []),
        gpu: Plotly.newPlot('gpu-chart', []),
        memory: Plotly.newPlot('memory-chart', []),
        network: Plotly.newPlot('network-chart', []),
        anomaly: Plotly.newPlot('anomaly-chart', [])
    };

    // Function to update charts
    async function updateCharts() {
        try {
            const response = await fetch('/api/metrics');
            const data = await response.json();
            
            // Update CPU chart
            const cpuData = [{
                x: data.timestamps,
                y: data.cpu,
                type: 'scatter'
            }];
            Plotly.update('cpu-chart', cpuData, {});

            // Update GPU chart
            const gpuData = [{
                x: data.timestamps,
                y: data.gpu,
                type: 'scatter'
            }];
            Plotly.update('gpu-chart', gpuData, {});

            // Update memory chart
            const memoryData = [{
                x: data.timestamps,
                y: data.memory,
                type: 'scatter'
            }];
            Plotly.update('memory-chart', memoryData, {});

            // Update network chart
            const networkData = [{
                x: data.timestamps,
                y: data.data_in,
                name: 'Data In',
                type: 'scatter'
            }, {
                x: data.timestamps,
                y: data.data_out,
                name: 'Data Out',
                type: 'scatter'
            }];
            Plotly.update('network-chart', networkData, {});

            // Update anomaly chart
            const anomalyData = [{
                x: data.timestamps,
                y: data.anomaly_scores,
                type: 'scatter'
            }];
            Plotly.update('anomaly-chart', anomalyData, {});
        } catch (error) {
            console.error('Error updating metrics:', error);
        }
    }

    // Fetch and update data periodically
    setInterval(async () => {
        try {
            const response = await fetch('/api/metrics');
            const data = await response.json();
            updateCharts(data);
        } catch (error) {
            console.error('Error updating metrics:', error);
        }
    }, 5000);
    updateCharts();
}); 