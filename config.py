# Configuration file for API keys
# Set ALPHA_VANTAGE_API_KEY in Render dashboard or a local .env file.

import os

# Alpha Vantage API Configuration
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", "demo")

# API Rate Limiting
ALPHA_VANTAGE_RATE_LIMIT = 5  # requests per minute (free tier)
REQUEST_DELAY = 12  # seconds between requests (60 seconds / 5 requests)

# Market Data Symbols - 3 main indexes + WTI + VIX
MARKET_SYMBOLS = [
    'SPY',     # S&P 500 ETF
    'QQQ',     # NASDAQ ETF
    'DIA',     # DOW ETF
    'USO',     # WTI Oil ETF
    'VXX'      # VIX ETF
]

# Fallback data (when APIs fail)
FALLBACK_DATA = {
    '^GSPC': {'price': 6300.00, 'change': 50.00, 'changePercent': 0.80},
    '^IXIC': {'price': 20400.00, 'change': 150.00, 'changePercent': 0.74},
    '^DJI': {'price': 42400.00, 'change': 300.00, 'changePercent': 0.71},
    'CL=F': {'price': 62.00, 'change': -1.50, 'changePercent': -2.36},
    'BZ=F': {'price': 66.00, 'change': -1.25, 'changePercent': -1.86},
    'NG=F': {'price': 2.20, 'change': 0.10, 'changePercent': 4.76},
    '^VIX': {'price': 15.00, 'change': -0.50, 'changePercent': -3.23},
    '^TNX': {'price': 4.40, 'change': 0.05, 'changePercent': 1.15}
}
