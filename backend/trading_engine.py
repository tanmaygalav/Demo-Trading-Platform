from auth import get_user_data, update_user_data
import uuid
from datetime import datetime

class TradingEngine:
    def __init__(self):
        self.lot_size = 1000  # $10 per pip for mini lot
        
    def calculate_pnl(self, order_type, open_price, close_price, lot_size):
        if order_type == 'buy':
            return (close_price - open_price) * lot_size
        else:  # sell
            return (open_price - close_price) * lot_size
    
    def place_order(self, user_id, order_data):
        user_data = get_user_data(user_id)
        if not user_data:
            return {'success': False, 'error': 'User not found'}
        
        symbol = order_data['symbol']
        order_type = order_data['type']
        lot_size = order_data.get('lot_size', 1)
        stop_loss = order_data.get('stop_loss')
        take_profit = order_data.get('take_profit')
        current_price = order_data['current_price']
        
        # Check if user has enough balance
        required_margin = lot_size * self.lot_size * 0.01  # 1% margin
        if user_data['balance'] < required_margin:
            return {'success': False, 'error': 'Insufficient balance'}
        
        order = {
            'id': str(uuid.uuid4()),
            'symbol': symbol,
            'type': order_type,
            'lot_size': lot_size,
            'open_price': current_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'open_time': datetime.now().isoformat(),
            'status': 'open'
        }
        
        user_data['open_orders'].append(order)
        
        if not update_user_data(user_id, user_data):
            return {'success': False, 'error': 'Failed to place order'}
        
        return {'success': True, 'order': order}
    
    def close_order(self, user_id, order_id):
        user_data = get_user_data(user_id)
        if not user_data:
            return {'success': False, 'error': 'User not found'}
        
        # Find the order
        order_index = None
        order_to_close = None
        
        for i, order in enumerate(user_data['open_orders']):
            if order['id'] == order_id:
                order_index = i
                order_to_close = order
                break
        
        if order_index is None:
            return {'success': False, 'error': 'Order not found'}
        
        # Get current price (in real scenario, this would be from market data)
        # For demo, we'll use a placeholder - you should pass current price from frontend
        current_price = order_to_close['open_price']  # This should be updated
        
        # Calculate P&L
        pnl = self.calculate_pnl(
            order_to_close['type'],
            order_to_close['open_price'],
            current_price,
            order_to_close['lot_size'] * self.lot_size
        )
        
        # Update balance
        user_data['balance'] += pnl
        
        # Close order
        closed_order = order_to_close.copy()
        closed_order['close_price'] = current_price
        closed_order['close_time'] = datetime.now().isoformat()
        closed_order['status'] = 'closed'
        closed_order['pnl'] = pnl
        
        user_data['closed_orders'].append(closed_order)
        user_data['open_orders'].pop(order_index)
        
        if not update_user_data(user_id, user_data):
            return {'success': False, 'error': 'Failed to close order'}
        
        return {'success': True, 'pnl': pnl, 'balance': user_data['balance']}