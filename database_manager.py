import sqlite3
from datetime import datetime

def init_database():
    """Creates a local database file to track cash and portfolio over time."""
    conn = sqlite3.connect('trading_history.db')
    cursor = conn.cursor()
    
    # Create table to log portfolio value balance over time
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolio_history (
            timestamp TEXT PRIMARY KEY,
            total_equity REAL,
            cash_balance REAL,
            open_pl REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_balance(equity, cash, pl):
    """Saves financial status to database and prints terminal metrics."""
    conn = sqlite3.connect('trading_history.db')
    cursor = conn.cursor()
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT OR REPLACE INTO portfolio_history (timestamp, total_equity, cash_balance, open_pl)
        VALUES (?, ?, ?, ?)
    ''', (current_timestamp, equity, cash, pl))
    
    conn.commit()
    conn.close()

    # Print comma-separated metrics
    print(f'💵 Available Cash: ${cash:,.2f}')
    print(f'📈 Total Portfolio Value: ${equity:,.2f}')
    print(f'📊 Open Trade P&L: ${pl:,.2f}')
