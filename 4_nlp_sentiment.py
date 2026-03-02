import yfinance as yf
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()

company = "AAPL" 
print(f"Searching for BREAKING NEWS about {company}")
ticker = yf.Ticker(company)
news_items = ticker.news

if not news_items:
    print("Wow, no recent news for this company today.")
else:
    total_score = 0
    valid_news = 0 
    
    for item in news_items:
        headline = item.get('title')
        if not headline and 'content' in item:
            headline = item['content'].get('title')
            
        if not headline or not isinstance(headline, str):
            continue
            
        score = sia.polarity_scores(headline)['compound']
        total_score += score
        valid_news += 1
        
        status = "POSITIVE" if score > 0.15 else "NEGATIVE" if score < -0.15 else "NEUTRAL"
        clean_headline = headline.replace('\n', ' ')
        print(f"{status:<12} | {score:>10.4f} | {clean_headline[:50]}...")
        
    print("-" * 80)
    if valid_news > 0:
        average = total_score / valid_news
        print(f"TODAY'S AVERAGE SCORE: {average:.4f}")
        
        if average > 0.15:
            print("🤖 Verdict: Market is OPTIMISTIC. Look for BUYS!")
        elif average < -0.15:
            print("🤖 Verdict: Market is FEARFUL. Prepare SELLS!")
        else:
            print("🤖 Verdict: Market is BORING. Hold cash.")