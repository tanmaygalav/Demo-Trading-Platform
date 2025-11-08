class TradingManager {
    constructor() {
        this.currentPrice = 0;
        this.openPositions = [];
        this.initEventListeners();
    }

    initEventListeners() {
        // Buy/Sell buttons
        document.querySelectorAll('.buy-btn, .sell-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const type = e.target.dataset.type;
                this.placeOrder(type);
            });
        });

        // Periodically update prices and portfolio
        setInterval(() => {
            this.updateCurrentPrice();
            this.loadPortfolio();
        }, 5000);
    }

    async updateCurrentPrice() {
        // This would be called from chart manager in real implementation
        // For now, we'll rely on the chart manager to update the price display
    }

    async placeOrder(type) {
        if (!window.authManager.currentUser) {
            alert('Please login first');
            return;
        }

        const symbol = document.getElementById('symbol-select').value;
        const lotSize = parseFloat(document.getElementById('lot-size').value);
        const stopLoss = document.getElementById('stop-loss').value ? 
            parseFloat(document.getElementById('stop-loss').value) : null;
        const takeProfit = document.getElementById('take-profit').value ? 
            parseFloat(document.getElementById('take-profit').value) : null;
        
        const currentPrice = parseFloat(document.getElementById('current-price').textContent);

        try {
            const response = await fetch(`${API_BASE}/place-order`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    symbol,
                    type,
                    lot_size: lotSize,
                    stop_loss: stopLoss,
                    take_profit: takeProfit,
                    current_price: currentPrice
                })
            });

            const data = await response.json();

            if (data.success) {
                alert(`Order placed successfully!`);
                this.loadPortfolio();
                window.authManager.updateBalance();
            } else {
                alert(`Order failed: ${data.error}`);
            }
        } catch (error) {
            console.error('Error placing order:', error);
            alert('Order failed. Please try again.');
        }
    }

    async closeOrder(orderId) {
        try {
            const response = await fetch(`${API_BASE}/close-order`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ order_id: orderId })
            });

            const data = await response.json();

            if (data.success) {
                alert(`Order closed! P&L: $${data.pnl.toFixed(2)}`);
                this.loadPortfolio();
                window.authManager.updateBalance();
            } else {
                alert(`Close order failed: ${data.error}`);
            }
        } catch (error) {
            console.error('Error closing order:', error);
            alert('Failed to close order. Please try again.');
        }
    }

    async loadPortfolio() {
        if (!window.authManager.currentUser) return;

        try {
            const response = await fetch(`${API_BASE}/portfolio`, {
                credentials: 'include'
            });

            if (response.ok) {
                const data = await response.json();
                this.displayOpenPositions(data.open_orders);
                this.displayTradeHistory(data.closed_orders);
                window.authManager.currentUser.balance = data.balance;
                window.authManager.updateBalance();
            }
        } catch (error) {
            console.error('Error loading portfolio:', error);
        }
    }

    displayOpenPositions(positions) {
        const container = document.getElementById('open-positions');
        
        if (positions.length === 0) {
            container.innerHTML = '<p>No open positions</p>';
            return;
        }

        container.innerHTML = positions.map(position => `
            <div class="position-item ${position.type}">
                <div class="position-header">
                    <span class="position-symbol">${position.symbol}</span>
                    <span class="position-type ${position.type}">${position.type.toUpperCase()}</span>
                </div>
                <div class="position-details">
                    <div>Size: ${position.lot_size}</div>
                    <div>Open: $${position.open_price.toFixed(4)}</div>
                    <div>SL: ${position.stop_loss ? '$' + position.stop_loss.toFixed(4) : '-'}</div>
                    <div>TP: ${position.take_profit ? '$' + position.take_profit.toFixed(4) : '-'}</div>
                </div>
                <button class="close-btn" onclick="window.tradingManager.closeOrder('${position.id}')">
                    Close Position
                </button>
            </div>
        `).join('');
    }

    displayTradeHistory(history) {
        const container = document.getElementById('trade-history');
        
        if (history.length === 0) {
            container.innerHTML = '<p>No trade history</p>';
            return;
        }

        // Show last 10 trades
        const recentHistory = history.slice(-10).reverse();
        
        container.innerHTML = recentHistory.map(trade => {
            const pnlClass = trade.pnl >= 0 ? 'positive' : 'negative';
            return `
                <div class="history-item ${trade.type}">
                    <div class="position-header">
                        <span class="position-symbol">${trade.symbol}</span>
                        <span class="position-type ${trade.type}">${trade.type.toUpperCase()}</span>
                    </div>
                    <div class="position-details">
                        <div>Size: ${trade.lot_size}</div>
                        <div>Open: $${trade.open_price.toFixed(4)}</div>
                        <div>Close: $${trade.close_price.toFixed(4)}</div>
                        <div class="pnl ${pnlClass}">P&L: $${trade.pnl.toFixed(2)}</div>
                    </div>
                </div>
            `;
        }).join('');
    }
}

// Initialize trading manager when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.tradingManager = new TradingManager();
});