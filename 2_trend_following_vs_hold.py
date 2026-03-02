import yfinance as yf
import pandas as pd

df = yf.download("NVDA", period="2y", interval="1h")

# Moving Averages (Fast 50, Slow 200)
if isinstance(df['Close'], pd.DataFrame):
    df['Fast_SMA'] = df['Close'].iloc[:, 0].rolling(window=50).mean()
    df['Slow_SMA'] = df['Close'].iloc[:, 0].rolling(window=200).mean()
    initial_price = df['Close'].iloc[0, 0]
    final_price = df['Close'].iloc[-1, 0]
else:
    df['Fast_SMA'] = df['Close'].rolling(window=50).mean()
    df['Slow_SMA'] = df['Close'].rolling(window=200).mean()
    initial_price = df['Close'].iloc[0]
    final_price = df['Close'].iloc[-1]

df = df.dropna()

initial_capital = 1000
current_capital = initial_capital
purchased_shares = 0
fee_percentage = 0.001 
in_position = False
completed_trades = 0

print("Starting Trend Bot\n")

for date, data in df.iterrows():
    current_price = data['Close'].iloc[0] if isinstance(data['Close'], pd.Series) else data['Close']
    fast_sma = data['Fast_SMA'].iloc[0] if isinstance(data['Fast_SMA'], pd.Series) else data['Fast_SMA']
    slow_sma = data['Slow_SMA'].iloc[0] if isinstance(data['Slow_SMA'], pd.Series) else data['Slow_SMA']
    
    # Bullish crossover (All in)
    if not in_position and fast_sma > slow_sma:
        purchased_shares = (current_capital * (1 - fee_percentage)) / current_price
        current_capital = 0.0 
        in_position = True
        
    # Bearish crossover (Sell all)
    elif in_position and fast_sma < slow_sma:
        current_capital = (purchased_shares * current_price) * (1 - fee_percentage)
        purchased_shares = 0
        in_position = False
        completed_trades += 1

bot_portfolio_value = (purchased_shares * final_price) if in_position else current_capital

# Buy & Hold
buy_and_hold_shares = (initial_capital * (1 - fee_percentage)) / initial_price
buy_and_hold_value = buy_and_hold_shares * final_price

print("-" * 55)
print(f"Bot Trades Completed: {completed_trades}")
print(f"FINAL TREND BOT VALUE: €{bot_portfolio_value:.2f}")
print(f"FINAL 'BUY & HOLD' VALUE: €{buy_and_hold_value:.2f}")
print("-" * 55)