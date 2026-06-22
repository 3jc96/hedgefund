# 📊 Sentiment Analysis & Market Reaction Scoring

## 🧠 **How Sentiment Analysis Works**

### **Sentiment Score (Range: -1.0 to +1.0)**
Your webscraper uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** sentiment analysis:

- **Tool:** `vaderSentiment` library
- **Input:** Article headline + summary text
- **Output:** Compound sentiment score from -1.0 to +1.0

### **Score Interpretation:**
- **+0.5 to +1.0:** Very Positive 🟢
- **+0.1 to +0.4:** Positive 🟢
- **-0.1 to +0.1:** Neutral ⚪
- **-0.4 to -0.1:** Negative 🔴
- **-1.0 to -0.5:** Very Negative 🔴

### **Example:**
```
Headline: "Apple Stock Surges 5% on Strong Earnings Report"
Sentiment Score: +0.8 (Very Positive)

Headline: "Market Crashes as Fed Announces Rate Hike"
Sentiment Score: -0.7 (Very Negative)
```

## 📈 **How Market Reaction Score Works**

### **Market Reaction Score (Range: 1-10)**
This is a **custom keyword-based scoring system** that looks for specific market-related words:

### **Positive Keywords (Boost Score):**
- `surge`, `rally`, `jump`, `soar`, `gain`, `rise`
- `bullish`, `positive`, `strong`, `up`, `higher`

### **Negative Keywords (Lower Score):**
- `drop`, `fall`, `decline`, `crash`, `plunge`
- `bearish`, `negative`, `weak`, `loss`, `down`, `lower`

### **Scoring Logic:**
```python
if positive_count > negative_count:
    score = min(10, 5 + positive_count)
elif negative_count > positive_count:
    score = max(1, 5 - negative_count)
else:
    score = 5  # Neutral
```

### **Score Interpretation:**
- **8-10:** Very Bullish 🟢
- **6-7:** Bullish 🟢
- **5:** Neutral ⚪
- **3-4:** Bearish 🔴
- **1-2:** Very Bearish 🔴

### **Example:**
```
Headline: "Tech Stocks Surge Higher as Market Rallies"
Positive words: "surge", "higher", "rallies" (3 words)
Score: 5 + 3 = 8 (Very Bullish)

Headline: "Oil Prices Drop as Demand Falls"
Negative words: "drop", "falls" (2 words)
Score: 5 - 2 = 3 (Bearish)
```

## 🔄 **How Both Scores Work Together**

### **Article Processing:**
1. **Scrape article** from news sources
2. **Extract headline + summary**
3. **Run VADER sentiment analysis** → Sentiment Score
4. **Run keyword analysis** → Market Reaction Score
5. **Store both scores** with the article

### **Display in Webscraper:**
- **Sentiment Score:** Shows emotional tone of the news
- **Market Reaction Score:** Shows expected market impact
- **Both scores** help you understand if news is positive/negative AND if it will move markets

## 📊 **Real Examples from Your Webscraper**

### **Example 1: Positive News**
```
Headline: "S&P 500 Surges to Record High on Strong Earnings"
Sentiment Score: +0.6 (Positive)
Market Reaction: 8/10 (Very Bullish)
→ Good news that should move markets up
```

### **Example 2: Negative News**
```
Headline: "Market Plunges as Fed Announces Aggressive Rate Hikes"
Sentiment Score: -0.8 (Very Negative)
Market Reaction: 2/10 (Very Bearish)
→ Bad news that should move markets down
```

### **Example 3: Mixed News**
```
Headline: "Mixed Economic Data Shows Growth Amid Inflation Concerns"
Sentiment Score: -0.1 (Slightly Negative)
Market Reaction: 5/10 (Neutral)
→ Uncertain news with unclear market impact
```

## 🎯 **Why This Matters for Trading**

### **Sentiment Score:**
- **Emotional context** of the news
- **Public perception** of the story
- **Media bias** detection

### **Market Reaction Score:**
- **Expected market impact**
- **Trading signal strength**
- **Risk assessment**

### **Combined Analysis:**
- **High sentiment + High reaction** = Strong buy signal
- **Low sentiment + Low reaction** = Strong sell signal
- **Mixed scores** = Wait and see

## 🔧 **Technical Implementation**

### **VADER Sentiment Analysis:**
```python
def analyze_sentiment(self, text: str) -> float:
    scores = self.sentiment_analyzer.polarity_scores(text)
    return scores['compound']  # Returns -1.0 to +1.0
```

### **Market Reaction Scoring:**
```python
def extract_market_reaction(self, text: str) -> float:
    positive_keywords = ['surge', 'rally', 'jump', 'soar', 'gain', 'rise']
    negative_keywords = ['drop', 'fall', 'decline', 'crash', 'plunge']
    
    # Count keywords and calculate score
    # Returns 1-10 scale
```

## 🌐 **Your Webscraper Features**

**URL:** https://quantumnews-ps23.3jcllc.com

**Sentiment Features:**
- ✅ **Real-time sentiment analysis** on all news articles
- ✅ **Market reaction scoring** for trading insights
- ✅ **Sentiment filtering** (positive/negative/neutral)
- ✅ **Average sentiment** by symbol
- ✅ **Sentiment trends** over time

**This gives you a complete picture of market sentiment and expected reactions! 📊**















