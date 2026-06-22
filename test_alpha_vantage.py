#!/usr/bin/env python3
"""
Test Alpha Vantage API with your API key
"""

import requests
import time
import json
from config import ALPHA_VANTAGE_API_KEY, MARKET_SYMBOLS, REQUEST_DELAY

def test_alpha_vantage_api():
    """Test Alpha Vantage API with your key"""
    
    if ALPHA_VANTAGE_API_KEY == "YOUR_API_KEY":
        print("❌ Please update config.py with your actual API key!")
        print("🔗 Get your free key at: https://www.alphavantage.co/support/#api-key")
        return False
    
    print("🚀 Testing Alpha Vantage API...")
    print(f"🔑 Using API Key: {ALPHA_VANTAGE_API_KEY[:8]}...")
    print("=" * 50)
    
    results = {}
    
    for symbol in MARKET_SYMBOLS:
        try:
            print(f"📊 Testing {symbol}...")
            
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': ALPHA_VANTAGE_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'Global Quote' in data and data['Global Quote']:
                    quote = data['Global Quote']
                    price = float(quote.get('05. price', 0))
                    change = float(quote.get('09. change', 0))
                    change_percent = float(quote.get('10. change percent', '0%').replace('%', ''))
                    
                    results[symbol] = {
                        'price': price,
                        'change': change,
                        'changePercent': change_percent,
                        'status': 'success'
                    }
                    
                    print(f"✅ {symbol}: ${price:.2f} ({change:+.2f}, {change_percent:+.2f}%)")
                else:
                    print(f"❌ {symbol}: No data returned")
                    results[symbol] = {'status': 'no_data'}
            else:
                print(f"❌ {symbol}: HTTP {response.status_code}")
                results[symbol] = {'status': f'http_{response.status_code}'}
                
        except Exception as e:
            print(f"❌ {symbol}: Error - {str(e)}")
            results[symbol] = {'status': 'error', 'error': str(e)}
        
        # Rate limiting - wait between requests
        if symbol != MARKET_SYMBOLS[-1]:  # Don't wait after last request
            print(f"⏳ Waiting {REQUEST_DELAY} seconds...")
            time.sleep(REQUEST_DELAY)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 API Test Summary:")
    
    successful = sum(1 for r in results.values() if r.get('status') == 'success')
    total = len(MARKET_SYMBOLS)
    
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    if successful > 0:
        print("\n🎉 Alpha Vantage API is working!")
        print("💡 Your webscraper will now show real market data!")
        return True
    else:
        print("\n❌ Alpha Vantage API test failed")
        print("🔧 Check your API key and try again")
        return False

if __name__ == "__main__":
    test_alpha_vantage_api()















