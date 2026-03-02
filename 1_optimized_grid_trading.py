import yfinance as yf
import pandas as pd

df = yf.download("NVDA", period="2y", interval="1h")

# Trend Filter: 60-hour SMA
if isinstance(df['Close'], pd.DataFrame):
    df['SMA_60'] = df['Close'].iloc[:, 0].rolling(window=60).mean()
else:
    df['SMA_60'] = df['Close'].rolling(window=60).mean()

df = df.dropna()

# Winning Configuration
investment_per_trade = 10  
take_profit = 0.020      
stop_loss = -0.025       
fee_percentage = 0.001   
max_capital_limit = 1000  

active_trades = [] 
successful_trades = 0
stop_loss_trades = 0
total_net_profit = 0

print("Starting 2-year simulation \n")

for date, data in df.iterrows():
    current_price = data['Close'].iloc[0] if isinstance(data['Close'], pd.Series) else data['Close']
    current_sma = data['SMA_60'].iloc[0] if isinstance(data['SMA_60'], pd.Series) else data['SMA_60']
    
    capital_at_risk = len(active_trades) * investment_per_trade
    
    # BUY (If trend is bullish)
    if capital_at_risk < max_capital_limit and current_price > current_sma:
        new_trade = {'buy_price': current_price, 'shares': investment_per_trade / current_price}
        active_trades.append(new_trade)
        total_net_profit -= (investment_per_trade * fee_percentage)
        
    # REVIEW
    remaining_trades = []
    for trade in active_trades:
        growth = (current_price - trade['buy_price']) / trade['buy_price']
        if growth >= take_profit:
            sell_value = trade['shares'] * current_price
            total_net_profit += (sell_value - investment_per_trade) - (sell_value * fee_percentage)
            successful_trades += 1
        elif growth <= stop_loss:
            sell_value = trade['shares'] * current_price
            total_net_profit += (sell_value - investment_per_trade) - (sell_value * fee_percentage)
            stop_loss_trades += 1
        else:
            remaining_trades.append(trade)
            
    active_trades = remaining_trades

print("-" * 55)
print("LONG-TERM BACKTEST RESULTS:")
print(f"SUCCESSFUL Trades: {successful_trades} | STOP LOSS Trades: {stop_loss_trades}")
print(f"TOTAL NET PROFIT: €{total_net_profit:.2f}")
print("-" * 55)