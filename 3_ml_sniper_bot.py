import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = yf.download("SPY", period="10y", interval="1d")

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Creating PRO Indicators
df['Daily_Return'] = df['Close'].pct_change()
df['Short_Trend_10d'] = df['Close'].rolling(window=10).mean()
df['Long_Trend_50d'] = df['Close'].rolling(window=50).mean()
df['Volatility'] = df['Close'].rolling(window=10).std()

delta = df['Close'].diff()
gain = delta.clip(lower=0).rolling(window=14).mean()
loss = -delta.clip(upper=0).rolling(window=14).mean()
rs = gain / loss
df['RSI'] = 100 - (100 / (1 + rs))
df['Volume_Change'] = df['Volume'].pct_change()

df = df.dropna()
df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
df = df[:-1]

train = df.iloc[:-500]
test = df.iloc[-500:].copy()

print("Training the Artificial Intelligence")
pro_predictors = ['Close', 'Daily_Return', 'Short_Trend_10d', 'Long_Trend_50d', 'Volatility', 'RSI', 'Volume_Change']
pro_model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)
pro_model.fit(train[pro_predictors], train['Target'])

# Exact probabilities (The Sniper)
test.loc[:, 'Probability_Up'] = pro_model.predict_proba(test[pro_predictors])[:, 1]

print("Simulating SMART portfolio (>60% Confidence + Hold)\n")
capital = 1000.0
fee = 0.001 
in_position = False
total_trades = 0

buy_threshold = 0.60 
sell_threshold = 0.50  

for i in range(len(test) - 1):
    prob_today = test['Probability_Up'].iloc[i]
    return_tomorrow = test['Daily_Return'].iloc[i + 1] 
    
    if prob_today >= buy_threshold and not in_position:
        capital = capital * (1 - fee) 
        in_position = True
        total_trades += 1
        
    elif prob_today < sell_threshold and in_position:
        capital = capital * (1 - fee) 
        in_position = False
        total_trades += 1
        
    if in_position:
        capital = capital * (1 + return_tomorrow)

if in_position:
    capital = capital * (1 - fee)

secure_buys = test[test['Probability_Up'] >= buy_threshold]
secure_precision = (secure_buys['Target'] == 1).mean() if len(secure_buys) > 0 else 0.0

print("-" * 55)
print(f"Days AI was >60% confident: {len(secure_buys)}")
print(f"Precision on 'secure' days: {secure_precision*100:.2f}%")
print(f"Times the bot paid a fee:   {total_trades}")
print(f"Final Capital:   €{capital:.2f} (Net Profit: €{capital - 1000:.2f})")
print("-" * 55)