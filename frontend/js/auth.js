const API_BASE = 'http://localhost:5000/api';

class AuthManager {
    constructor() {
        this.currentUser = null;
        this.initEventListeners();
        this.checkExistingSession();
    }

    initEventListeners() {
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.login();
        });

        document.getElementById('register-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.register();
        });

        document.getElementById('show-register').addEventListener('click', () => {
            this.showScreen('register-screen');
        });

        document.getElementById('show-login').addEventListener('click', () => {
            this.showScreen('login-screen');
        });

        document.getElementById('logout-btn').addEventListener('click', () => {
            this.logout();
        });
    }

    async checkExistingSession() {
        try {
            const response = await fetch(`${API_BASE}/portfolio`, {
                credentials: 'include'
            });
            
            if (response.ok) {
                const data = await response.json();
                this.currentUser = data;
                this.showTradingScreen();
            }
        } catch (error) {
            console.log('No existing session');
        }
    }

    async login() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const messageEl = document.getElementById('auth-message');

        try {
            const response = await fetch(`${API_BASE}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser = data.user;
                this.showTradingScreen();
                messageEl.textContent = '';
            } else {
                messageEl.textContent = data.error;
                messageEl.className = 'error';
            }
        } catch (error) {
            messageEl.textContent = 'Login failed. Please try again.';
            messageEl.className = 'error';
        }
    }

    async register() {
        const username = document.getElementById('reg-username').value;
        const password = document.getElementById('reg-password').value;
        const messageEl = document.getElementById('reg-message');

        try {
            const response = await fetch(`${API_BASE}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser = data.user;
                this.showTradingScreen();
                messageEl.textContent = '';
            } else {
                messageEl.textContent = data.error;
                messageEl.className = 'error';
            }
        } catch (error) {
            messageEl.textContent = 'Registration failed. Please try again.';
            messageEl.className = 'error';
        }
    }

    async logout() {
        try {
            await fetch(`${API_BASE}/logout`, {
                method: 'POST',
                credentials: 'include'
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.currentUser = null;
            this.showScreen('login-screen');
        }
    }

    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.add('hidden');
        });
        document.getElementById(screenId).classList.remove('hidden');
    }

    showTradingScreen() {
        this.showScreen('trading-screen');
        document.getElementById('user-welcome').textContent = `Welcome, ${this.currentUser.username}!`;
        this.updateBalance();
        
        // Initialize trading components
        if (window.chartManager) {
            window.chartManager.loadChartData();
        }
        if (window.tradingManager) {
            window.tradingManager.loadPortfolio();
        }
    }

    updateBalance() {
        if (this.currentUser) {
            document.getElementById('user-balance').textContent = 
                `Balance: $${this.currentUser.balance.toFixed(2)}`;
        }
    }
}

// Initialize auth manager when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.authManager = new AuthManager();
});