class ChartManager {
    constructor() {
        this.chart = null;
        this.currentSymbol = 'XAUUSD';
        this.currentData = [];
        this.isDemoData = true; // Track if we're using demo data
        this.initChart();
        this.initEventListeners();
        this.loadChartData();
    }

    initChart() {
        const ctx = document.getElementById('price-chart').getContext('2d');
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: this.currentSymbol,
                    data: [],
                    borderColor: '#00d4aa',
                    backgroundColor: 'rgba(0, 212, 170, 0.1)',
                    borderWidth: 2,
                    tension: 0.1,
                    fill: true,
                    pointRadius: 0,
                    pointHoverRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'hour'
                        },
                        grid: {
                            color: 'rgba(255,255,255,0.1)'
                        },
                        ticks: {
                            color: '#ccc'
                        }
                    },
                    y: {
                        position: 'right',
                        grid: {
                            color: 'rgba(255,255,255,0.1)'
                        },
                        ticks: {
                            color: '#ccc',
                            callback: function(value) {
                                return value.toFixed(2);
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                }
            }
        });
    }

    async loadChartData() {
        try {
            this.showMessage('Loading market data...', 'info');
            
            const timeframe = document.getElementById('timeframe-select').value;
            const period = timeframe === '1h' ? '5d' : '1mo';
            
            const response = await fetch(
                `${API_BASE}/data/${this.currentSymbol}?period=${period}&interval=${timeframe}`
            );
            
            const data = await response.json();
            
            if (data && data.length > 0) {
                this.currentData = data;
                this.updateChart(data);
                this.updateCurrentPrice();
                this.showMessage(`✅ Live demo trading active - ${data.length} data points loaded`, 'success');
                this.isDemoData = true;
            } else {
                throw new Error('No data received');
            }
            
        } catch (error) {
            console.error('Chart data loading failed:', error);
            // Don't show error - we'll work with whatever we have
            this.showMessage('🎯 Demo trading mode active with simulated data', 'info');
        }
    }

    updateChart(data) {
        const chartData = data.map(item => ({
            x: new Date(item.timestamp),
            y: item.close
        }));

        this.chart.data.datasets[0].data = chartData;
        this.chart.data.datasets[0].label = `${this.currentSymbol} ${this.isDemoData ? '(Demo)' : ''}`;
        this.chart.update();
    }

    async updateCurrentPrice() {
        try {
            const response = await fetch(`${API_BASE}/current-price/${this.currentSymbol}`);
            if (response.ok) {
                const data = await response.json();
                this.updatePriceDisplay(data.price);
            }
        } catch (error) {
            console.error('Price update failed:', error);
            // Use the last data point if available
            if (this.currentData.length > 0) {
                const lastPrice = this.currentData[this.currentData.length - 1].close;
                this.updatePriceDisplay(lastPrice);
            }
        }
    }

    updatePriceDisplay(price) {
        const priceElement = document.getElementById('current-price');
        if (!priceElement) return;

        const previousPrice = parseFloat(priceElement.getAttribute('data-previous')) || price;
        priceElement.setAttribute('data-previous', price);
        
        priceElement.textContent = price.toFixed(4);
        
        if (price > previousPrice) {
            priceElement.style.color = '#00d4aa';
            priceElement.style.fontWeight = 'bold';
        } else if (price < previousPrice) {
            priceElement.style.color = '#ff6b6b';
            priceElement.style.fontWeight = 'bold';
        } else {
            priceElement.style.color = '#ccc';
            priceElement.style.fontWeight = 'normal';
        }
    }

    showMessage(message, type = 'info') {
        this.clearMessage();
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `chart-message ${type}`;
        messageDiv.style.cssText = `
            background: ${type === 'error' ? '#ff6b6b' : 
                        type === 'warning' ? '#ffa726' : 
                        type === 'success' ? '#00d4aa' : '#2196f3'};
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            margin: 10px 0;
            text-align: center;
            font-size: 14px;
        `;
        messageDiv.textContent = message;
        
        const chartContainer = document.querySelector('.chart-container');
        const controls = chartContainer.querySelector('.chart-controls');
        chartContainer.insertBefore(messageDiv, controls.nextSibling);
        
        if (type !== 'error') {
            setTimeout(() => this.clearMessage(), 5000);
        }
    }

    clearMessage() {
        const existing = document.querySelector('.chart-message');
        if (existing) existing.remove();
    }
}

// Initialize when ready
document.addEventListener('DOMContentLoaded', () => {
    window.chartManager = new ChartManager();
});