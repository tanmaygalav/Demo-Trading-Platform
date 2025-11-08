import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

JSONBIN_API_KEY = os.getenv('JSONBIN_API_KEY', 'your-jsonbin-api-key')
JSONBIN_BIN_ID = os.getenv('JSONBIN_BIN_ID', 'your-jsonbin-bin-id')

def get_bin_data():
    headers = {
        'X-Master-Key': JSONBIN_API_KEY,
        'X-Bin-Meta': 'false'
    }
    
    response = requests.get(
        f'https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}/latest',
        headers=headers
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        # Return empty structure if bin doesn't exist
        return {'users': {}}

def update_bin_data(data):
    headers = {
        'X-Master-Key': JSONBIN_API_KEY,
        'Content-Type': 'application/json'
    }
    
    response = requests.put(
        f'https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}',
        headers=headers,
        data=json.dumps(data)
    )
    
    return response.status_code == 200

def authenticate_user(username, password):
    data = get_bin_data()
    users = data.get('users', {})
    
    user = users.get(username)
    if user and user.get('password') == password:
        return {
            'username': username,
            'balance': user.get('balance', 10000),
            'open_orders': user.get('open_orders', []),
            'closed_orders': user.get('closed_orders', [])
        }
    return None

def create_user(username, password):
    data = get_bin_data()
    users = data.get('users', {})
    
    if username in users:
        return {'success': False, 'error': 'Username already exists'}
    
    users[username] = {
        'password': password,
        'balance': 10000,
        'open_orders': [],
        'closed_orders': []
    }
    
    data['users'] = users
    if update_bin_data(data):
        return {
            'success': True,
            'user': {
                'username': username,
                'balance': 10000,
                'open_orders': [],
                'closed_orders': []
            }
        }
    else:
        return {'success': False, 'error': 'Failed to create user'}

def get_user_data(username):
    data = get_bin_data()
    users = data.get('users', {})
    return users.get(username, {})

def update_user_data(username, user_data):
    data = get_bin_data()
    users = data.get('users', {})
    users[username] = user_data
    data['users'] = users
    return update_bin_data(data)