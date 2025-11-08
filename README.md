<img width="1893" height="912" alt="Screenshot 2025-11-08 121418" src="https://github.com/user-attachments/assets/dd0ca13e-6a62-4a07-9b20-3a6531daac6a" />
<img width="1899" height="928" alt="Screenshot 2025-11-08 124100" src="https://github.com/user-attachments/assets/650606c7-1113-467c-b0fc-70a65b870555" />

🌟 Features
📊 Trading Features
Real-time Charting: Interactive H1 charts for XAUUSD and EURUSD

Demo Trading: $10,000 virtual balance to practice trading

Backtesting: Historical data replay functionality

Order Management: Buy/Sell orders with stop loss and take profit

Portfolio Tracking: Real-time P&L and position management

🔧 Technical Features
Self-Contained Data: Realistic market simulation without external API dependencies

User Authentication: Secure login/registration system

JSON Storage: Cloud-based data persistence using JSONBin

Responsive Design: Modern UI that works on desktop and mobile

Realistic Simulation: Market hours, volatility, and trend simulation

🚀 Quick Start
Prerequisites
Python 3.8+

Modern web browser

JSONBin account (free)

Installation
Clone the repository

bash
git clone https://github.com/yourusername/trading-platform.git
cd trading-platform
Backend Setup

bash
cd backend
pip install -r requirements.txt
JSONBin Configuration

Create free account at JSONBin.io

Get your API Key and Bin ID

Create .env file:

env
JSONBIN_API_KEY=your_master_key_here
JSONBIN_BIN_ID=your_bin_id_here
Start Backend Server

bash
python app.py
Server runs on http://localhost:5000

Start Frontend Server

bash
cd frontend
python -m http.server 8000
Open http://localhost:8000 in your browser

🎯 Usage
Demo Accounts
Username: demo | Password: demo123

Username: test | Password: test123

Trading Interface
Chart Analysis: View H1 or daily charts for XAUUSD/EURUSD

Place Orders:

Click BUY/SELL buttons

Set lot size (default: 1.0)

Optional: Set stop loss and take profit

Manage Positions:

View open positions in real-time

Close positions to realize P&L

Backtesting: Use replay feature to test strategies on historical data

Trading Rules
Initial balance: $10,000

Lot size: $10 per pip (mini lots)

Margin requirement: 1%

Available pairs: XAUUSD (Gold), EURUSD

📁 Project Structure
text
trading-platform/
├── backend/
│   ├── app.py                 # Flask server & API routes
│   ├── auth.py               # User authentication
│   ├── trading_engine.py     # Order processing & P&L calculation
│   ├── data_fetcher.py       # Realistic market data simulation
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── index.html            # Main application
│   ├── css/
│   │   └── style.css         # Styling and responsive design
│   └── js/
│       ├── auth.js           # User authentication
│       ├── chart.js          # Chart initialization & management
│       └── trading.js        # Trading logic & order management
└── README.md
🔌 API Endpoints
Authentication
POST /api/login - User login

POST /api/register - User registration

POST /api/logout - User logout

Market Data
GET /api/data/{symbol} - Historical chart data

GET /api/current-price/{symbol} - Current price

POST /api/replay - Historical data replay

Trading
POST /api/place-order - Place new order

POST /api/close-order - Close existing order

GET /api/portfolio - User portfolio data

🛠 Technology Stack
Backend
Python 3.8+ - Core programming language

Flask - Web framework and API server

yfinance - Market data (fallback)

JSONBin - Cloud data storage

Frontend
Vanilla JavaScript - No framework dependencies

Chart.js - Interactive price charts

HTML5/CSS3 - Modern responsive design

Fetch API - HTTP requests

Data Simulation
Realistic price movement algorithms

Market hour simulation (London/NY sessions)

Volatility and trend modeling

OHLC data generation

💡 Trading Features in Detail
Order Types
Market Orders: Instant execution at current price

Stop Loss: Automatic position closing at specified price

Take Profit: Automatic profit taking at target price

Risk Management
Margin requirements enforcement

Balance and equity tracking

Real-time P&L calculation

Position size validation

Chart Features
Multiple timeframes (H1, D1)

Real-time price updates

Interactive tooltips

Responsive design

🔧 Development
Adding New Features
Backend API endpoints in app.py

Frontend components in respective JS files

Update trading engine for new order types

Test with demo accounts

Customizing Data Simulation
Modify data_fetcher.py to adjust:

Price volatility parameters

Market hour simulations

Trend strength and duration

Initial price levels

Styling Changes
Update frontend/css/style.css for:

Color schemes

Layout adjustments

Mobile responsiveness

🐛 Troubleshooting
Common Issues
Chart not loading

Check browser console for errors

Verify backend is running on port 5000

Ensure no ad blockers are blocking requests

Login failures

Verify JSONBin credentials in .env file

Check internet connection for JSONBin API access

Ensure user data structure is properly initialized

Price data issues

Application uses simulated data - no external dependencies required

Data is generated realistically with market simulations

Refresh the page to regenerate data if needed

Backend Logs
Check the Flask console for detailed error messages and data generation logs.

📊 Example Trading Session
javascript
// Example trade flow:
1. Login with demo credentials
2. Select XAUUSD and 1H timeframe
3. Analyze chart and current price ($1950.25)
4. Place BUY order with:
   - Lot Size: 1.0
   - Stop Loss: $1945.50
   - Take Profit: $1960.75
5. Monitor position in Open Positions panel
6. Close position manually or let SL/TP execute automatically
7. View P&L in Trade History
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🚀 Future Enhancements
Additional trading instruments

Advanced order types (limit orders, trailing stops)

Technical indicators on charts

Trading journal and analytics

Multi-timeframe analysis

Export trade history to CSV

📞 Support
For support and questions:

Open an issue on GitHub

Check the troubleshooting section above

Verify all prerequisites are met

Happy Trading! 🎯

Note: This is a demo platform for educational purposes. Practice responsible trading and risk management.
