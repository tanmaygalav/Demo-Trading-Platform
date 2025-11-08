import pandas as pd
from datetime import datetime, timedelta
import random
import json

class DataFetcher:
    def __init__(self):
        # Realistic starting prices
        self.base_prices = {
            'XAUUSD': 1950.0,  # Gold around $1950
            'EURUSD': 1.0850   # EUR/USD around 1.0850
        }
        
        # Current prices that will evolve realistically
        self.current_prices = self.base_prices.copy()
        
        # Store historical trends for realistic movement
        self.trends = {
            'XAUUSD': {'direction': 1, 'strength': 0.3, 'volatility': 15},
            'EURUSD': {'direction': -1, 'strength': 0.1, 'volatility': 0.005}
        }
        
        # Market hours simulation (more activity during certain hours)
        self.market_hours = {
            'london_open': 8,   # 8 AM London
            'london_close': 16, # 4 PM London  
            'ny_open': 13,      # 1 PM London (8 AM NY)
            'ny_close': 21      # 9 PM London (4 PM NY)
        }

    def _get_market_activity(self, hour):
        """Simulate market activity based on time of day"""
        if self.market_hours['london_open'] <= hour <= self.market_hours['london_close']:
            return 1.5  # High activity during London hours
        elif self.market_hours['ny_open'] <= hour <= self.market_hours['ny_close']:
            return 2.0  # Highest activity during NY/London overlap
        else:
            return 0.5  # Low activity during Asian session

    def _calculate_price_movement(self, symbol, hour):
        """Calculate realistic price movement based on symbol and market conditions"""
        trend = self.trends[symbol]
        market_activity = self._get_market_activity(hour)
        
        # Base movement based on trend
        base_move = trend['direction'] * trend['strength'] * market_activity
        
        # Random component based on volatility
        random_move = random.gauss(0, trend['volatility'] * 0.1) * market_activity
        
        # Combine movements
        total_move = base_move + random_move
        
        # Ensure realistic bounds
        if symbol == 'XAUUSD':
            total_move = max(min(total_move, 20), -20)  # Max $20 move
        else:
            total_move = max(min(total_move, 0.02), -0.02)  # Max 2% move
            
        return total_move

    def generate_realistic_data(self, symbol, points=100, interval='1h'):
        """Generate completely realistic trading data"""
        data = []
        current_time = datetime.now() - timedelta(hours=points)
        current_price = self.base_prices[symbol]
        
        for i in range(points):
            hour = current_time.hour
            minute = current_time.minute
            
            # Calculate price movement
            price_move = self._calculate_price_movement(symbol, hour)
            
            # Update current price
            current_price += price_move
            
            # Ensure price doesn't go to unrealistic levels
            if symbol == 'XAUUSD':
                current_price = max(1800, min(2200, current_price))  # Gold between 1800-2200
            else:
                current_price = max(1.05, min(1.12, current_price))  # EUR/USD between 1.05-1.12
            
            # Create realistic OHLC data
            open_price = current_price
            high_price = current_price + abs(price_move) * random.uniform(0.5, 2.0)
            low_price = current_price - abs(price_move) * random.uniform(0.5, 2.0)
            close_price = current_price + random.uniform(-abs(price_move), abs(price_move))
            
            # Ensure high/low are logical
            high_price = max(open_price, close_price, high_price)
            low_price = min(open_price, close_price, low_price)
            
            # Volume based on market activity
            base_volume = 10000 if symbol == 'XAUUSD' else 50000
            market_activity = self._get_market_activity(hour)
            volume = int(base_volume * market_activity * random.uniform(0.8, 1.2))
            
            data.append({
                'timestamp': current_time.isoformat(),
                'open': round(open_price, 4),
                'high': round(high_price, 4),
                'low': round(low_price, 4),
                'close': round(close_price, 4),
                'volume': volume
            })
            
            # Move to next time period
            if interval == '1h':
                current_time += timedelta(hours=1)
            else:  # 1d
                current_time += timedelta(days=1)
        
        # Update current price for real-time queries
        self.current_prices[symbol] = close_price
        
        print(f"📊 Generated realistic demo data for {symbol}: {points} {interval} points")
        print(f"📈 Final price: {close_price:.4f}")
        
        return data

    def get_historical_data(self, symbol, period='5d', interval='1h'):
        """Get historical data - completely self-contained"""
        try:
            print(f"🎯 Generating historical data for {symbol} ({period}, {interval})")
            
            # Calculate number of points needed
            if interval == '1h':
                if period == '1d':
                    points = 24
                elif period == '5d':
                    points = 24 * 5
                else:  # 1mo
                    points = 24 * 30
            else:  # 1d
                if period == '1mo':
                    points = 30
                else:  # 3mo
                    points = 90
            
            data = self.generate_realistic_data(symbol, points, interval)
            return data
            
        except Exception as e:
            print(f"❌ Error in get_historical_data: {str(e)}")
            # Fallback to basic data
            return self.generate_realistic_data(symbol, 50, interval)

    def get_current_price(self, symbol):
        """Get current price with realistic evolution"""
        try:
            # Simulate small price movement from last known price
            current_price = self.current_prices[symbol]
            hour = datetime.now().hour
            
            # Small random walk
            if symbol == 'XAUUSD':
                change = random.uniform(-0.5, 0.5)
            else:
                change = random.uniform(-0.0005, 0.0005)
                
            # Apply market activity
            market_activity = self._get_market_activity(hour)
            change *= market_activity
            
            new_price = current_price + change
            
            # Keep within realistic bounds
            if symbol == 'XAUUSD':
                new_price = max(1800, min(2200, new_price))
            else:
                new_price = max(1.05, min(1.12, new_price))
            
            self.current_prices[symbol] = new_price
            
            print(f"🎯 Current {symbol} price: {new_price:.4f}")
            return new_price
            
        except Exception as e:
            print(f"❌ Error in get_current_price: {str(e)}")
            return self.base_prices[symbol]

    def get_data_at_date(self, symbol, target_date):
        """Get data for replay mode"""
        try:
            # For replay, we'll generate data based on the target date
            # This creates consistent but date-specific prices
            target_dt = datetime.fromisoformat(target_date.replace('Z', '+00:00'))
            
            # Use date to seed random but consistent price
            date_seed = hash(target_date) % 10000 / 10000  # 0-1 based on date
            
            if symbol == 'XAUUSD':
                base_price = 1800 + (date_seed * 400)  # 1800-2200 based on date
            else:
                base_price = 1.05 + (date_seed * 0.07)  # 1.05-1.12 based on date
            
            result = {
                'timestamp': target_date,
                'open': round(base_price - 0.5, 4),
                'high': round(base_price + 1.2, 4),
                'low': round(base_price - 1.2, 4),
                'close': round(base_price, 4)
            }
            
            print(f"🎯 Replay data for {symbol} on {target_date}: {result['close']:.4f}")
            return result
            
        except Exception as e:
            print(f"❌ Error in get_data_at_date: {str(e)}")
            return {
                'timestamp': target_date,
                'open': self.base_prices[symbol],
                'high': self.base_prices[symbol] + 1,
                'low': self.base_prices[symbol] - 1,
                'close': self.base_prices[symbol]
            }

    def update_trend(self, symbol, new_direction=None):
        """Allow trends to evolve over time for more realistic markets"""
        if new_direction is None:
            # Randomly evolve trend
            trend = self.trends[symbol]
            trend['direction'] *= random.choice([1, -1])  # Possibly reverse
            trend['strength'] = random.uniform(0.1, 0.5)  # Change strength
            trend['volatility'] = random.uniform(
                trend['volatility'] * 0.8, 
                trend['volatility'] * 1.2
            )
        
        print(f"📈 Updated {symbol} trend: {self.trends[symbol]}")