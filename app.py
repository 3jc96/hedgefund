#!/usr/bin/env python3
"""
Quantum Capital News Webscraper
Multi-source news aggregation with live market data
"""

import os
import uuid
from pathlib import Path
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List
import random
from urllib.parse import quote_plus

import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import feedparser

try:
    from config import ALPHA_VANTAGE_API_KEY, MARKET_SYMBOLS, REQUEST_DELAY
except ImportError:
    ALPHA_VANTAGE_API_KEY = "demo"
    MARKET_SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']
    REQUEST_DELAY = 12

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-local-secret-change-me')
CORS(app)

DATA_DIR = Path(os.environ.get('DATA_DIR', Path(__file__).parent / 'data'))
DATA_DIR.mkdir(parents=True, exist_ok=True)
FX_REQUESTS_FILE = DATA_DIR / 'fx_requests.jsonl'

ADMIN_TOKEN = os.environ.get('IBKR_ADMIN_TOKEN', 'dev-admin-token')

YF_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
}


class NewsScraper:
    """News scraper using multiple reliable sources"""

    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

        # Default portfolio so the app shows news immediately on first load
        self.portfolio = {
            'stocks': ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'META', 'AMZN'],
            'commodities': ['CL=F', 'GC=F', 'NG=F']
        }

        # Company name strings used to build Google News search queries
        self.company_names = {
            'AAPL': 'Apple AAPL stock',
            'MSFT': 'Microsoft MSFT stock',
            'GOOGL': 'Alphabet Google GOOGL stock',
            'AMZN': 'Amazon AMZN stock',
            'TSLA': 'Tesla TSLA stock',
            'META': 'Meta Facebook META stock',
            'NVDA': 'NVIDIA NVDA stock',
            'JPM': 'JPMorgan Chase JPM stock',
            'BAC': 'Bank of America BAC stock',
            'WMT': 'Walmart WMT stock',
            'JNJ': 'Johnson Johnson JNJ stock',
            'V': 'Visa V stock',
            'XOM': 'ExxonMobil XOM stock',
            'PG': 'Procter Gamble PG stock',
            'NFLX': 'Netflix NFLX stock',
            'DIS': 'Disney DIS stock',
            'PYPL': 'PayPal PYPL stock',
            'INTC': 'Intel INTC stock',
            'AMD': 'AMD semiconductor stock',
            'CRM': 'Salesforce CRM stock',
        }

        # Commodity queries for Google News
        self.commodity_names = {
            'GC=F': 'gold prices futures market',
            'SI=F': 'silver prices futures market',
            'CL=F': 'crude oil WTI prices OPEC',
            'HG=F': 'copper prices futures market',
            'NG=F': 'natural gas prices storage',
            'ZC=F': 'corn prices futures crop',
            'ZW=F': 'wheat prices futures crop',
            'ZS=F': 'soybeans prices futures crop',
            'SB=F': 'sugar prices futures market',
            'KC=F': 'coffee prices futures market',
            'BZ=F': 'Brent crude oil prices',
        }

        # EIA series configuration
        self.eia_api_key = os.environ.get('EIA_API_KEY', 'demo')
        self.eia_base_url = 'https://api.eia.gov/v2'
        self.eia_series = {
            'CL=F': {'name': 'Crude Oil'},
            'NG=F': {'name': 'Natural Gas'},
            'GC=F': {'name': 'Gold'},
        }

        # In-memory cache
        self.article_cache: Dict[str, List] = {}
        self.cache_timestamp: Dict[str, float] = {}
        self.eia_cache: Dict = {}
        self.eia_cache_timestamp: Dict[str, float] = {}
        self.cache_duration = 300       # 5 min for news
        self.eia_cache_duration = 3600  # 1 hr for EIA

    # ── Symbol management ─────────────────────────────────────────────────────

    def add_symbol(self, symbol: str, category: str = 'stocks') -> bool:
        if category not in self.portfolio:
            self.portfolio[category] = []
        if symbol.upper() not in self.portfolio[category]:
            self.portfolio[category].append(symbol.upper())
            return True
        return False

    def remove_symbol(self, symbol: str, category: str = 'stocks') -> bool:
        if category in self.portfolio and symbol.upper() in self.portfolio[category]:
            self.portfolio[category].remove(symbol.upper())
            return True
        return False

    def get_portfolio(self) -> Dict:
        return self.portfolio

    # ── Sentiment helpers ─────────────────────────────────────────────────────

    def analyze_sentiment(self, text: str) -> float:
        try:
            return self.sentiment_analyzer.polarity_scores(text)['compound']
        except Exception:
            return 0.0

    def extract_market_reaction(self, text: str) -> float:
        positive_kw = ['surge', 'rally', 'jump', 'soar', 'gain', 'rise', 'bullish', 'beat',
                       'record', 'up', 'higher', 'breakout', 'upgrade', 'strong', 'positive']
        negative_kw = ['drop', 'fall', 'decline', 'crash', 'plunge', 'bearish', 'miss',
                       'loss', 'down', 'lower', 'downgrade', 'warning', 'weak', 'negative']
        text_lower = text.lower()
        pos = sum(1 for w in positive_kw if w in text_lower)
        neg = sum(1 for w in negative_kw if w in text_lower)
        if pos > neg:
            return min(10.0, 5 + pos)
        elif neg > pos:
            return max(1.0, 5 - neg)
        return 5.0

    def _clean_html(self, text: str) -> str:
        try:
            return BeautifulSoup(text, 'html.parser').get_text()
        except Exception:
            return text

    def _make_article(self, symbol: str, entry, source: str) -> Dict:
        headline = entry.get('title', '')
        summary = self._clean_html(entry.get('summary', headline))[:500]
        link = entry.get('link', '')
        pub_date = datetime.now()
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                pub_date = datetime(*entry.published_parsed[:6])
            except Exception:
                pass
        text = headline + ' ' + summary
        return {
            'symbol': symbol,
            'headline': headline,
            'summary': summary,
            'source': source,
            'url': link,
            'published_date': pub_date.isoformat(),
            'sentiment_score': self.analyze_sentiment(text),
            'market_reaction_score': self.extract_market_reaction(text),
        }

    # ── Google News RSS (primary source) ─────────────────────────────────────

    def scrape_google_news(self, query: str, symbol: str, limit: int = 10) -> List[Dict]:
        """Fetch articles from Google News RSS — free, no API key, very reliable."""
        articles = []
        try:
            url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                try:
                    src_info = getattr(entry, 'source', None)
                    source = (src_info.get('title') if isinstance(src_info, dict) else None) or 'Google News'
                    articles.append(self._make_article(symbol, entry, source))
                except Exception:
                    continue
        except Exception as e:
            logger.error(f"Google News error ({query}): {e}")
        return articles

    # ── Yahoo Finance RSS ─────────────────────────────────────────────────────

    def scrape_yahoo_finance_news(self, symbol: str) -> List[Dict]:
        """Fetch from Yahoo Finance RSS then supplement with Google News."""
        articles = []
        try:
            url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                try:
                    articles.append(self._make_article(symbol, entry, 'Yahoo Finance'))
                except Exception:
                    continue
        except Exception as e:
            logger.error(f"Yahoo Finance RSS error ({symbol}): {e}")

        # Supplement with Google News for richer coverage
        query = self.company_names.get(symbol, f'{symbol} stock market')
        articles.extend(self.scrape_google_news(query, symbol, limit=8))

        # Deduplicate by headline prefix
        seen: set = set()
        unique = []
        for a in articles:
            key = a['headline'][:80].lower()
            if key not in seen:
                seen.add(key)
                unique.append(a)
        return unique

    # ── Commodity news ────────────────────────────────────────────────────────

    def scrape_commodity_news(self, symbol: str) -> List[Dict]:
        """Fetch commodity news from Google News + OilPrice for energy."""
        query = self.commodity_names.get(symbol, symbol.replace('=F', '').lower() + ' commodity price')
        articles = self.scrape_google_news(query, symbol, limit=12)

        if symbol in ['CL=F', 'NG=F', 'BZ=F']:
            try:
                feed = feedparser.parse("https://oilprice.com/rss/main")
                kw = ['oil', 'gas', 'crude', 'opec', 'energy', 'petroleum', 'lng', 'brent', 'wti', 'barrel']
                for entry in feed.entries[:15]:
                    try:
                        headline = entry.get('title', '')
                        summary = self._clean_html(entry.get('summary', headline))
                        if any(k in (headline + summary).lower() for k in kw):
                            articles.append(self._make_article(symbol, entry, 'OilPrice.com'))
                    except Exception:
                        continue
            except Exception as e:
                logger.debug(f"OilPrice RSS error: {e}")

        seen: set = set()
        unique = []
        for a in articles:
            key = a['headline'][:80].lower()
            if key not in seen:
                seen.add(key)
                unique.append(a)
        return unique

    # ── General finance news ──────────────────────────────────────────────────

    def scrape_general_finance_news(self) -> List[Dict]:
        """Fetch market-wide financial news from CNBC, MarketWatch Pulse, and AP."""
        articles = []
        sources = [
            ('https://www.cnbc.com/id/100003114/device/rss/rss.html', 'CNBC'),
            ('https://www.cnbc.com/id/10000664/device/rss/rss.html', 'CNBC Markets'),
            ('https://feeds.marketwatch.com/marketwatch/marketpulse', 'MarketWatch'),
            ('https://apnews.com/hub/financial-markets/rss.xml', 'AP Markets'),
        ]
        for feed_url, source_name in sources:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:8]:
                    try:
                        articles.append(self._make_article('MARKET', entry, source_name))
                    except Exception:
                        continue
            except Exception as e:
                logger.debug(f"General news error ({source_name}): {e}")
        return articles

    # ── Per-symbol and aggregated news ────────────────────────────────────────

    def scrape_news_for_symbol(self, symbol: str) -> List[Dict]:
        cache_key = f"symbol_{symbol}"
        now = time.time()
        if cache_key in self.article_cache and now - self.cache_timestamp.get(cache_key, 0) < self.cache_duration:
            return self.article_cache[cache_key]
        if symbol in self.portfolio.get('commodities', []):
            articles = self.scrape_commodity_news(symbol)
        else:
            articles = self.scrape_yahoo_finance_news(symbol)
        self.article_cache[cache_key] = articles
        self.cache_timestamp[cache_key] = now
        return articles

    def scrape_all_news(self) -> Dict[str, List[Dict]]:
        all_news: Dict[str, List] = {}
        for category, symbols in self.portfolio.items():
            all_news[category] = []
            for symbol in symbols:
                all_news[category].extend(self.scrape_news_for_symbol(symbol))
                time.sleep(0.5)
        all_news['general'] = self.scrape_general_finance_news()
        return all_news

    def get_articles_for_symbol(self, symbol: str = None, limit: int = 50) -> List[Dict]:
        if symbol:
            return self.scrape_news_for_symbol(symbol)[:limit]
        all_articles: List[Dict] = []
        for sym_list in self.portfolio.values():
            for sym in sym_list:
                all_articles.extend(self.scrape_news_for_symbol(sym))
        all_articles.extend(self.scrape_general_finance_news())
        all_articles.sort(key=lambda x: x.get('published_date', ''), reverse=True)
        return all_articles[:limit]

    # ── EIA data ──────────────────────────────────────────────────────────────

    def get_eia_data(self, symbol: str) -> Dict:
        if symbol not in self.eia_series:
            return {"error": "No EIA data available for this symbol"}
        cache_key = f"eia_{symbol}"
        now = time.time()
        if cache_key in self.eia_cache and now - self.eia_cache_timestamp.get(cache_key, 0) < self.eia_cache_duration:
            return self.eia_cache[cache_key]
        try:
            name = self.eia_series[symbol]['name']
            eia_data: Dict = {
                'symbol': symbol, 'name': name,
                'last_updated': datetime.now().isoformat(),
                'data': {}, 'sentiment': 'neutral', 'sentiment_score': 0.0,
                'summary': '', 'market_impact': 'neutral'
            }
            has_real_data = False

            if symbol == 'CL=F':
                url = (f"{self.eia_base_url}/petroleum/stoc/wstk/data/"
                       f"?api_key={self.eia_api_key}&frequency=weekly&data[0]=value"
                       f"&facets[product][]=WCESTUS1&sort[0][column]=period"
                       f"&sort[0][direction]=desc&offset=0&length=5")
                try:
                    resp = requests.get(url, timeout=10)
                    if resp.status_code == 200:
                        rows = resp.json().get('response', {}).get('data', [])
                        if rows:
                            has_real_data = True
                            eia_data['data'] = {
                                'latest_value': rows[0]['value'],
                                'latest_date': rows[0]['period'],
                                'previous_value': rows[1]['value'] if len(rows) > 1 else None,
                                'previous_date': rows[1]['period'] if len(rows) > 1 else None,
                                'change': None, 'change_percent': None,
                            }
                except Exception:
                    pass

            elif symbol == 'NG=F':
                url = (f"{self.eia_base_url}/natural-gas/stor/wkly/data/"
                       f"?api_key={self.eia_api_key}&frequency=weekly&data[0]=value"
                       f"&facets[series][]=NW2_EPG0_SWO_R48_BCF&sort[0][column]=period"
                       f"&sort[0][direction]=desc&offset=0&length=5")
                try:
                    resp = requests.get(url, timeout=10)
                    if resp.status_code == 200:
                        rows = resp.json().get('response', {}).get('data', [])
                        if rows:
                            has_real_data = True
                            eia_data['data'] = {
                                'latest_value': rows[0]['value'],
                                'latest_date': rows[0]['period'],
                                'previous_value': rows[1]['value'] if len(rows) > 1 else None,
                                'previous_date': rows[1]['period'] if len(rows) > 1 else None,
                                'change': None, 'change_percent': None,
                            }
                except Exception:
                    pass

            if not has_real_data:
                eia_data['data'] = self._get_mock_eia_data(symbol)
                eia_data['note'] = "Using estimated data (set EIA_API_KEY env var for live data)"

            d = eia_data['data']
            if d.get('latest_value') is not None and d.get('previous_value') is not None:
                latest = float(d['latest_value'])
                prev = float(d['previous_value'])
                change = latest - prev
                pct = (change / prev * 100) if prev else 0
                d['change'] = round(change, 2)
                d['change_percent'] = round(pct, 2)
                eia_data.update(self._analyze_eia_sentiment(symbol, change, pct, latest, prev))

            eia_data['reports'] = {
                'weekly': ('https://www.eia.gov/naturalgas/weekly/' if symbol == 'NG=F'
                           else 'https://www.eia.gov/petroleum/weekly/'),
                'monthly': ('https://www.eia.gov/naturalgas/monthly/' if symbol == 'NG=F'
                            else 'https://www.eia.gov/petroleum/monthly/'),
            }
            self.eia_cache[cache_key] = eia_data
            self.eia_cache_timestamp[cache_key] = now
            return eia_data
        except Exception as e:
            logger.error(f"EIA error ({symbol}): {e}")
            return {"symbol": symbol, "error": str(e)}

    def _get_mock_eia_data(self, symbol: str) -> Dict:
        today = datetime.now()
        if symbol == 'CL=F':
            latest = round(random.uniform(420, 450), 1)
            prev = round(latest + random.uniform(-15, 15), 1)
            ref = today - timedelta(days=(today.weekday() - 2) % 7)
            return {
                'latest_value': latest, 'latest_date': ref.strftime('%Y-%m-%d'),
                'previous_value': prev, 'previous_date': (ref - timedelta(7)).strftime('%Y-%m-%d'),
                'unit': 'million barrels', 'description': 'U.S. Crude Oil Inventories',
                'report_day': 'Wednesday', 'report_time': '10:30 AM ET',
            }
        elif symbol == 'NG=F':
            latest = round(random.uniform(2800, 3200), 0)
            prev = round(latest + random.uniform(-100, 100), 0)
            ref = today - timedelta(days=(today.weekday() - 3) % 7)
            return {
                'latest_value': latest, 'latest_date': ref.strftime('%Y-%m-%d'),
                'previous_value': prev, 'previous_date': (ref - timedelta(7)).strftime('%Y-%m-%d'),
                'unit': 'billion cubic feet', 'description': 'U.S. Natural Gas Storage',
                'report_day': 'Thursday', 'report_time': '10:30 AM ET',
            }
        return {'latest_value': None, 'previous_value': None,
                'latest_date': today.strftime('%Y-%m-%d'), 'unit': 'unknown'}

    def _analyze_eia_sentiment(self, symbol: str, change: float, pct: float, latest: float, prev: float) -> Dict:
        if symbol == 'CL=F':
            if change > 5:
                return {'sentiment': 'bearish', 'sentiment_score': max(-1.0, -pct / 20),
                        'summary': f"Crude inventories +{abs(change):.1f}M bbl ({pct:.1f}%) — bearish supply build.",
                        'market_impact': 'negative'}
            elif change < -5:
                return {'sentiment': 'bullish', 'sentiment_score': min(1.0, -pct / 20),
                        'summary': f"Crude inventories -{abs(change):.1f}M bbl ({abs(pct):.1f}%) — bullish demand draw.",
                        'market_impact': 'positive'}
        elif symbol == 'NG=F':
            if change > 50:
                return {'sentiment': 'bearish', 'sentiment_score': max(-1.0, -pct / 15),
                        'summary': f"Nat gas storage +{abs(change):.0f}B cf — bearish storage build.",
                        'market_impact': 'negative'}
            elif change < -50:
                return {'sentiment': 'bullish', 'sentiment_score': min(1.0, -pct / 15),
                        'summary': f"Nat gas storage -{abs(change):.0f}B cf — bullish storage draw.",
                        'market_impact': 'positive'}
        return {'sentiment': 'neutral', 'sentiment_score': 0.0,
                'summary': f"Change: {change:.2f} ({pct:.1f}%) — within normal range.",
                'market_impact': 'neutral'}


# ── App init ───────────────────────────────────────────────────────────────────

news_scraper = NewsScraper()

# Server-side market data cache — avoids hammering Yahoo Finance
_market_data_cache: Dict = {}
_market_data_ts: float = 0.0
_MARKET_CACHE_TTL = 180  # seconds (3 minutes)

QUESTION_BANK = [
    {
        'id': 'ev_dice',
        'prompt': 'What is the expected value of a fair 6-sided die?',
        'hint': None,
        'expected': 3.5,
        'dp': 1,
    },
    {
        'id': 'var_portfolio_10_norm',
        'prompt': 'Portfolio of 10 i.i.d. N(0,1) positions. Compute 99% one-day VaR (z = 2.33). Answer to 1 dp.',
        'hint': 'Portfolio SD = sqrt(n); VaR99% = z × SD.',
        'expected': round(2.33 * (10 ** 0.5), 1),
        'dp': 1,
    },
    {
        'id': 'min_var_hedge',
        'prompt': 'Given Cov(S,F)=6.0, Var(F)=5.0. Compute minimum-variance hedge ratio h*. Answer to 1 dp.',
        'hint': 'h* = Cov(S,F) / Var(F).',
        'expected': round(6.0 / 5.0, 1),
        'dp': 1,
    },
]


def _pick_question():
    q = random.choice(QUESTION_BANK)
    session['qa_id'] = q['id']
    return q


def _get_question_by_id(qid):
    return next((q for q in QUESTION_BANK if q['id'] == qid), None)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    if not session.get('passed_gate'):
        return redirect(url_for('qa_gate'))
    return render_template('index.html')


@app.route('/qa', methods=['GET', 'POST'])
def qa_gate():
    if request.method == 'POST':
        answer = (request.form.get('answer') or '').strip()
        q = _get_question_by_id(session.get('qa_id')) or _pick_question()
        normalized = answer.replace(',', '.')
        is_correct = False
        try:
            val = float(normalized)
            if round(val, q.get('dp', 1)) == q['expected']:
                is_correct = True
        except Exception:
            is_correct = normalized == str(q['expected'])
        if is_correct:
            session['passed_gate'] = True
            return redirect(url_for('index'))
        return render_template('qa.html', error=f"{answer} 你妹", previous_answer=answer,
                               redirect_to_google=True, prompt=q['prompt'], hint=q.get('hint'))
    q = _pick_question()
    return render_template('qa.html', prompt=q['prompt'], hint=q.get('hint'))


@app.route('/fresh')
def fresh():
    return render_template('index.html')


@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "portfolio_size": sum(len(v) for v in news_scraper.portfolio.values()),
        "cache_articles": sum(len(v) for v in news_scraper.article_cache.values()),
    })


@app.route('/api/portfolio')
def get_portfolio():
    return jsonify(news_scraper.get_portfolio())


@app.route('/api/portfolio/add', methods=['POST'])
def add_symbol():
    data = request.get_json()
    if not data or 'symbol' not in data:
        return jsonify({"error": "Symbol is required"}), 400
    symbol = data['symbol']
    category = data.get('category', 'stocks')
    if news_scraper.add_symbol(symbol, category):
        return jsonify({"message": f"Added {symbol} to {category}", "success": True})
    return jsonify({"error": f"{symbol} already exists in {category}"}), 400


@app.route('/api/portfolio/remove', methods=['POST'])
def remove_symbol():
    data = request.get_json()
    if not data or 'symbol' not in data:
        return jsonify({"error": "Symbol is required"}), 400
    symbol = data['symbol']
    category = data.get('category', 'stocks')
    if news_scraper.remove_symbol(symbol, category):
        return jsonify({"message": f"Removed {symbol} from {category}", "success": True})
    return jsonify({"error": f"{symbol} not found in {category}"}), 400


@app.route('/api/news')
def get_news():
    symbol = request.args.get('symbol')
    limit = int(request.args.get('limit', 20))
    return jsonify(news_scraper.get_articles_for_symbol(symbol, limit))


@app.route('/api/eia/<symbol>')
def get_eia_data(symbol):
    return jsonify(news_scraper.get_eia_data(symbol))


@app.route('/api/eia')
def get_all_eia_data():
    result = {}
    for sym in news_scraper.portfolio.get('commodities', []):
        if sym in news_scraper.eia_series:
            result[sym] = news_scraper.get_eia_data(sym)
    return jsonify(result)


@app.route('/api/news/scrape', methods=['POST'])
def trigger_scrape():
    try:
        news_scraper.article_cache.clear()
        news_scraper.cache_timestamp.clear()
        all_news = news_scraper.scrape_all_news()
        total = sum(len(v) for v in all_news.values())
        return jsonify({"message": f"Scraping complete. Found {total} articles.", "success": True, "articles_found": total})
    except Exception as e:
        logger.error(f"Scrape error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/market-data')
def get_market_data():
    """
    Real-time quotes via yfinance (handles Yahoo Finance auth automatically).
    Results are server-cached for 3 minutes to avoid rate-limiting.
    Returns S&P 500, NASDAQ, DOW, WTI Oil, Gold, VIX, 10Y Treasury, Bitcoin.
    """
    global _market_data_cache, _market_data_ts
    now = time.time()
    if _market_data_cache and now - _market_data_ts < _MARKET_CACHE_TTL:
        return jsonify({"market_data": _market_data_cache,
                        "timestamp": datetime.now().isoformat(),
                        "cached": True})

    symbol_map = {
        'SP500':  '^GSPC',
        'NASDAQ': '^IXIC',
        'DOW':    '^DJI',
        'WTI':    'CL=F',
        'GOLD':   'GC=F',
        'VIX':    '^VIX',
        'TNX':    '^TNX',
        'BTC':    'BTC-USD',
    }

    market_data = {k: {'status': 'no_data', 'symbol': v} for k, v in symbol_map.items()}

    try:
        import yfinance as yf
        for label, sym in symbol_map.items():
            try:
                ticker = yf.Ticker(sym)
                info   = ticker.fast_info
                price  = info.last_price
                prev   = info.previous_close
                if price is None or price == 0:
                    market_data[label] = {'status': 'no_data', 'symbol': sym}
                    continue
                change = float(price) - float(prev) if prev else 0.0
                pct    = (change / float(prev) * 100) if prev else 0.0
                market_data[label] = {
                    'price': round(float(price), 3),
                    'change': round(change, 3),
                    'changePercent': round(pct, 3),
                    'status': 'success',
                    'symbol': sym,
                }
            except Exception as e:
                logger.debug(f"yfinance error for {sym}: {e}")
                market_data[label] = {'status': 'error', 'error': str(e), 'symbol': sym}
    except ImportError:
        # Fallback to raw HTTP if yfinance not installed
        for idx, (label, sym) in enumerate(symbol_map.items()):
            if idx > 0:
                time.sleep(0.4)
            try:
                url = f"https://query2.finance.yahoo.com/v8/finance/chart/{sym}?interval=1m&range=1d"
                resp = requests.get(url, headers=YF_HEADERS, timeout=12)
                if resp.status_code == 200:
                    result = (resp.json().get('chart', {}).get('result') or [None])[0]
                    if result:
                        meta   = result.get('meta', {})
                        price  = float(meta.get('regularMarketPrice') or meta.get('chartPreviousClose') or 0)
                        prev   = float(meta.get('previousClose') or meta.get('chartPreviousClose') or price)
                        change = price - prev
                        pct    = (change / prev * 100) if prev else 0
                        market_data[label] = {'price': round(price, 3), 'change': round(change, 3),
                                              'changePercent': round(pct, 3), 'status': 'success', 'symbol': sym}
                else:
                    market_data[label] = {'status': 'error', 'error': f'HTTP {resp.status_code}', 'symbol': sym}
            except Exception as e:
                market_data[label] = {'status': 'error', 'error': str(e), 'symbol': sym}

    # Cache successful results; return stale on total failure
    successful = {k: v for k, v in market_data.items() if v.get('status') == 'success'}
    if successful:
        _market_data_cache = market_data
        _market_data_ts = now
    elif _market_data_cache:
        return jsonify({"market_data": _market_data_cache, "timestamp": datetime.now().isoformat(),
                        "cached": True, "stale": True})

    return jsonify({"market_data": market_data, "timestamp": datetime.now().isoformat()})


@app.route('/api/calendar')
def get_calendar_events():
    """
    Upcoming economic reports, FOMC meetings, and earnings events.
    All dates are dynamically computed so they never go stale.
    """
    try:
        today = datetime.now().date()
        year = today.year
        events = []

        # Monthly economic reports for the next 4 months
        for offset in range(0, 4):
            y = year
            m = today.month + offset
            if m > 12:
                m -= 12
                y += 1

            # NFP: first Friday
            first_day = datetime(y, m, 1)
            days_to_friday = (4 - first_day.weekday()) % 7
            first_friday = first_day + timedelta(days=days_to_friday)
            events.append({
                'title': 'Jobs Report (NFP)', 'type': 'economic',
                'date': first_friday.strftime('%Y-%m-%d'), 'time': '8:30 AM ET',
                'description': 'Non-farm payrolls & unemployment rate',
                'impact': 'High', 'source': 'Bureau of Labor Statistics',
            })

            # CPI ~12th
            events.append({
                'title': 'CPI Report', 'type': 'economic',
                'date': f'{y}-{m:02d}-12', 'time': '8:30 AM ET',
                'description': 'Consumer Price Index — inflation measure',
                'impact': 'High', 'source': 'Bureau of Labor Statistics',
            })

            # PPI ~13th
            events.append({
                'title': 'PPI Report', 'type': 'economic',
                'date': f'{y}-{m:02d}-13', 'time': '8:30 AM ET',
                'description': 'Producer Price Index — wholesale inflation',
                'impact': 'Medium', 'source': 'Bureau of Labor Statistics',
            })

            # Retail Sales ~17th
            events.append({
                'title': 'Retail Sales', 'type': 'economic',
                'date': f'{y}-{m:02d}-17', 'time': '8:30 AM ET',
                'description': 'Monthly consumer spending report',
                'impact': 'Medium', 'source': 'Census Bureau',
            })

        # GDP quarterly (advance releases)
        for gdp_m, gdp_d, label in [(4, 30, 'Q1'), (7, 30, 'Q2'), (10, 30, 'Q3')]:
            gdp_y = year if gdp_m >= today.month else year + 1
            events.append({
                'title': f'GDP Advance ({label})', 'type': 'economic',
                'date': f'{gdp_y}-{gdp_m:02d}-{gdp_d:02d}', 'time': '8:30 AM ET',
                'description': f'Gross Domestic Product — advance estimate for {label}',
                'impact': 'High', 'source': 'Bureau of Economic Analysis',
            })

        # FOMC meetings 2026
        fomc_2026 = [
            '2026-01-29', '2026-03-18', '2026-04-29', '2026-06-10',
            '2026-07-29', '2026-09-16', '2026-10-28', '2026-12-16',
        ]
        for decision_date in fomc_2026:
            events.append({
                'title': 'FOMC Meeting', 'type': 'fomc',
                'date': decision_date, 'time': '2:00 PM ET',
                'description': 'Federal Reserve interest rate decision',
                'impact': 'High', 'source': 'Federal Reserve',
            })
            minutes_date = (datetime.strptime(decision_date, '%Y-%m-%d') + timedelta(weeks=3)).strftime('%Y-%m-%d')
            events.append({
                'title': 'FOMC Minutes', 'type': 'fomc',
                'date': minutes_date, 'time': '2:00 PM ET',
                'description': 'Detailed minutes from FOMC meeting',
                'impact': 'Medium', 'source': 'Federal Reserve',
            })

        # Earnings calendar 2026 (Q2 July–Aug + Q3 Oct–Nov)
        earnings_2026 = [
            ('JPM Earnings',   '2026-07-14', '7:00 AM ET',  'JPMorgan Chase Q2 2026',   'JPMorgan Chase'),
            ('GS Earnings',    '2026-07-15', '7:30 AM ET',  'Goldman Sachs Q2 2026',    'Goldman Sachs'),
            ('NFLX Earnings',  '2026-07-16', '4:00 PM ET',  'Netflix Q2 2026',           'Netflix'),
            ('TSLA Earnings',  '2026-07-22', '4:30 PM ET',  'Tesla Q2 2026',             'Tesla Inc.'),
            ('MSFT Earnings',  '2026-07-23', '4:30 PM ET',  'Microsoft Q4 FY2026',       'Microsoft Corp.'),
            ('GOOGL Earnings', '2026-07-24', '4:30 PM ET',  'Alphabet Q2 2026',          'Alphabet Inc.'),
            ('META Earnings',  '2026-07-29', '4:30 PM ET',  'Meta Platforms Q2 2026',    'Meta Platforms'),
            ('AAPL Earnings',  '2026-07-31', '4:30 PM ET',  'Apple Q3 FY2026',           'Apple Inc.'),
            ('AMZN Earnings',  '2026-08-01', '4:30 PM ET',  'Amazon Q2 2026',            'Amazon.com Inc.'),
            ('NVDA Earnings',  '2026-08-27', '4:30 PM ET',  'NVIDIA Q2 FY2027',          'NVIDIA Corp.'),
            ('JPM Earnings',   '2026-10-13', '7:00 AM ET',  'JPMorgan Chase Q3 2026',    'JPMorgan Chase'),
            ('TSLA Earnings',  '2026-10-21', '4:30 PM ET',  'Tesla Q3 2026',             'Tesla Inc.'),
            ('MSFT Earnings',  '2026-10-22', '4:30 PM ET',  'Microsoft Q1 FY2027',       'Microsoft Corp.'),
            ('GOOGL Earnings', '2026-10-23', '4:30 PM ET',  'Alphabet Q3 2026',          'Alphabet Inc.'),
            ('META Earnings',  '2026-10-28', '4:30 PM ET',  'Meta Platforms Q3 2026',    'Meta Platforms'),
            ('AAPL Earnings',  '2026-10-29', '4:30 PM ET',  'Apple Q4 FY2026',           'Apple Inc.'),
            ('AMZN Earnings',  '2026-10-30', '4:30 PM ET',  'Amazon Q3 2026',            'Amazon.com Inc.'),
            ('NVDA Earnings',  '2026-11-19', '4:30 PM ET',  'NVIDIA Q3 FY2027',          'NVIDIA Corp.'),
        ]
        for title, date, time_et, desc, source in earnings_2026:
            events.append({
                'title': title, 'type': 'earnings',
                'date': date, 'time': time_et,
                'description': desc, 'impact': 'High', 'source': source,
            })

        future = [e for e in events if e['date'] >= today.isoformat()]
        future.sort(key=lambda x: x['date'])

        return jsonify({
            "events": future,
            "timestamp": datetime.now().isoformat(),
            "total_events": len(future),
        })
    except Exception as e:
        logger.error(f"Calendar error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/news/summary')
def get_news_summary():
    try:
        articles = news_scraper.get_articles_for_symbol(limit=50)
        if not articles:
            return jsonify({"message": "No articles found"})
        total = len(articles)
        avg_sentiment = sum(a['sentiment_score'] for a in articles) / total
        avg_reaction = sum(a['market_reaction_score'] for a in articles) / total
        symbol_stats: Dict = {}
        for a in articles:
            sym = a['symbol']
            if sym not in symbol_stats:
                symbol_stats[sym] = {'count': 0, 'avg_sentiment': 0.0, 'avg_market_reaction': 0.0}
            symbol_stats[sym]['count'] += 1
            symbol_stats[sym]['avg_sentiment'] += a['sentiment_score']
            symbol_stats[sym]['avg_market_reaction'] += a['market_reaction_score']
        for sym in symbol_stats:
            n = symbol_stats[sym]['count']
            symbol_stats[sym]['avg_sentiment'] = round(symbol_stats[sym]['avg_sentiment'] / n, 3)
            symbol_stats[sym]['avg_market_reaction'] = round(symbol_stats[sym]['avg_market_reaction'] / n, 2)
        return jsonify({
            "total_articles": total,
            "avg_sentiment": round(avg_sentiment, 3),
            "avg_market_reaction": round(avg_reaction, 2),
            "symbol_stats": symbol_stats,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── FX service ────────────────────────────────────────────────────────────────

def _fetch_usd_sgd_rate() -> Dict:
    try:
        url = "https://query2.finance.yahoo.com/v8/finance/chart/USDSGD=X?interval=1m&range=1d"
        resp = requests.get(url, headers=YF_HEADERS, timeout=10)
        if resp.status_code == 200:
            result = (resp.json().get('chart', {}).get('result') or [None])[0]
            if result:
                price = float(result.get('meta', {}).get('regularMarketPrice') or 0)
                return {'price': price, 'timestamp': datetime.now().isoformat()}
    except Exception:
        pass
    return {'price': 0.0, 'timestamp': datetime.now().isoformat()}


def _append_jsonl(path: Path, record: Dict) -> None:
    try:
        with path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        logger.exception("Failed to append FX record")


def _read_jsonl(path: Path) -> List[Dict]:
    items: List[Dict] = []
    if not path.exists():
        return items
    try:
        with path.open('r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        items.append(json.loads(line))
                    except Exception:
                        continue
    except Exception:
        logger.exception("Failed to read FX records")
    return items


@app.route('/fx/request', methods=['GET', 'POST'])
def fx_request_page():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        direction = (request.form.get('direction') or '').strip()
        try:
            amount = float((request.form.get('amount') or '0').strip())
        except Exception:
            amount = 0.0
        note = (request.form.get('note') or '').strip()
        rate = _fetch_usd_sgd_rate()
        req_id = uuid.uuid4().hex
        record = {
            'id': req_id, 'created_at': datetime.now().isoformat(),
            'name': name, 'email': email, 'direction': direction,
            'amount': amount, 'note': note,
            'reference_rate': rate.get('price', 0.0), 'status': 'pending',
        }
        _append_jsonl(FX_REQUESTS_FILE, record)
        return render_template('fx_request.html', submitted=True, request_id=req_id, rate=rate.get('price', 0.0))
    rate = _fetch_usd_sgd_rate()
    return render_template('fx_request.html', submitted=False, rate=rate.get('price', 0.0))


@app.route('/api/fx/quote', methods=['GET'])
def api_fx_quote():
    return jsonify(_fetch_usd_sgd_rate())


@app.route('/admin/fx', methods=['GET'])
def admin_fx_list():
    token = request.args.get('token') or request.headers.get('X-Admin-Token')
    if token != ADMIN_TOKEN:
        return jsonify({'error': 'unauthorized'}), 401
    items = _read_jsonl(FX_REQUESTS_FILE)
    items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    rate = _fetch_usd_sgd_rate()
    return render_template('fx_admin.html', items=items, rate=rate.get('price', 0.0), token=token)


@app.route('/admin/fx/respond', methods=['POST'])
def admin_fx_respond():
    token = request.form.get('token') or request.headers.get('X-Admin-Token')
    if token != ADMIN_TOKEN:
        return jsonify({'error': 'unauthorized'}), 401
    req_id = (request.form.get('id') or '').strip()
    try:
        offered_rate = float((request.form.get('offered_rate') or '0').strip())
    except Exception:
        offered_rate = 0.0
    message = (request.form.get('message') or '').strip()
    items = _read_jsonl(FX_REQUESTS_FILE)
    found = False
    for item in items:
        if item.get('id') == req_id:
            item['status'] = 'quoted'
            item['quoted_at'] = datetime.now().isoformat()
            item['offered_rate'] = offered_rate
            item['message'] = message
            found = True
    if not found:
        return jsonify({'error': 'not_found'}), 404
    try:
        with FX_REQUESTS_FILE.open('w', encoding='utf-8') as f:
            for rec in items:
                f.write(json.dumps(rec) + "\n")
    except Exception:
        logger.exception("Failed to write FX records")
    return redirect(url_for('admin_fx_list', token=token))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Quantum Capital News — http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
