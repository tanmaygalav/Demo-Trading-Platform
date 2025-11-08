from flask import Flask, request, jsonify, session
from flask_cors import CORS
import yfinance as yf
from datetime import datetime, timedelta
import json
from auth import authenticate_user, create_user, get_user_data, update_user_data
from trading_engine import TradingEngine
from data_fetcher import DataFetcher

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production
CORS(app, supports_credentials=True)

# Initialize components
data_fetcher = DataFetcher()
trading_engine = TradingEngine()

# Available symbols
SYMBOLS = {
    'XAUUSD': 'GC=F',  # Gold
    'EURUSD': 'EURUSD=X'  # EUR/USD
}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate_user(username, password)
    if user:
        session['user_id'] = username
        return jsonify({'success': True, 'user': user})
    else:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    result = create_user(username, password)
    if result['success']:
        session['user_id'] = username
        return jsonify({'success': True, 'user': result['user']})
    else:
        return jsonify({'success': False, 'error': result['error']}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'success': True})

@app.route('/api/data/<symbol>', methods=['GET'])
def get_data(symbol):
    if symbol not in ['XAUUSD', 'EURUSD']:
        return jsonify({'error': 'Invalid symbol'}), 400
    
    period = request.args.get('period', '5d')
    interval = request.args.get('interval', '1h')
    
    try:
        data = data_fetcher.get_historical_data(symbol, period, interval)
        return jsonify(data)
    except Exception as e:
        print(f"Error in /api/data: {str(e)}")
        # Return demo data even if there's an error
        demo_data = data_fetcher.generate_realistic_data(symbol, 50, interval)
        return jsonify(demo_data)

@app.route('/api/current-price/<symbol>', methods=['GET'])
def get_current_price(symbol):
    if symbol not in ['XAUUSD', 'EURUSD']:
        return jsonify({'error': 'Invalid symbol'}), 400
    
    try:
        price = data_fetcher.get_current_price(symbol)
        return jsonify({'price': price})
    except Exception as e:
        print(f"Error in /api/current-price: {str(e)}")
        # Always return a price, even if there's an error
        fallback_price = data_fetcher.base_prices.get(symbol, 1000.0)
        return jsonify({'price': fallback_price})

@app.route('/api/place-order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    user_id = session['user_id']
    
    try:
        result = trading_engine.place_order(user_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/close-order', methods=['POST'])
def close_order():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    user_id = session['user_id']
    
    try:
        result = trading_engine.close_order(user_id, data['order_id'])
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    user_data = get_user_data(user_id)
    
    return jsonify({
        'balance': user_data.get('balance', 10000),
        'open_orders': user_data.get('open_orders', []),
        'closed_orders': user_data.get('closed_orders', [])
    })

@app.route('/api/replay', methods=['POST'])
def replay_data():
    data = request.json
    symbol = data.get('symbol')
    date = data.get('date')
    
    if symbol not in SYMBOLS:
        return jsonify({'error': 'Invalid symbol'}), 400
    
    try:
        replay_data = data_fetcher.get_data_at_date(SYMBOLS[symbol], date)
        return jsonify(replay_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)