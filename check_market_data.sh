#!/bin/bash

echo "📊 Quantum News PS23 - Market Data Accuracy Check"
echo ""

echo "🔍 Checking current market data sources..."
echo ""

# Function to check a single symbol
check_symbol() {
    local symbol=$1
    local name=$2
    
    echo -n "Checking $name ($symbol)... "
    
    # Try to get current data with a delay
    sleep 2
    
    # Use curl with proper headers and timeout
    response=$(curl -s -m 10 \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
        -H "Accept: application/json" \
        "https://query1.finance.yahoo.com/v7/finance/quote?symbols=$symbol" 2>/dev/null)
    
    if [[ $response == *"Too Many Requests"* ]]; then
        echo "❌ Rate limited"
        return 1
    elif [[ $response == *"regularMarketPrice"* ]]; then
        # Extract price using grep and sed
        price=$(echo "$response" | grep -o '"regularMarketPrice":[0-9.]*' | sed 's/.*://')
        change=$(echo "$response" | grep -o '"regularMarketChange":[0-9.-]*' | sed 's/.*://')
        changePercent=$(echo "$response" | grep -o '"regularMarketChangePercent":[0-9.-]*' | sed 's/.*://')
        
        if [[ -n "$price" ]]; then
            echo "✅ $${price} (${change:+$change} ${changePercent:+$changePercent}%)"
            return 0
        else
            echo "❌ No data"
            return 1
        fi
    else
        echo "❌ Failed"
        return 1
    fi
}

echo "📈 Current Market Data:"
echo ""

# Check major indices and commodities
check_symbol "^GSPC" "S&P 500"
check_symbol "^IXIC" "NASDAQ"
check_symbol "^DJI" "DOW"
check_symbol "CL=F" "WTI Crude"
check_symbol "BZ=F" "Brent Crude"
check_symbol "NG=F" "Natural Gas"
check_symbol "^VIX" "VIX"
check_symbol "^TNX" "10Y Treasury"

echo ""
echo "🔧 Market Data Issues & Solutions:"
echo ""
echo "❌ Problem: Yahoo Finance API rate limiting"
echo "✅ Solution: Implemented multiple fallbacks:"
echo "   • Multiple API endpoints"
echo "   • Longer delays between requests"
echo "   • Client-side caching (5 minutes)"
echo "   • Fallback data for offline mode"
echo "   • Manual refresh button"
echo ""
echo "📊 Current Fallback Data (used when API fails):"
echo "   • S&P 500: $6,300.00 (+50.00 +0.80%)"
echo "   • NASDAQ: $20,400.00 (+150.00 +0.74%)"
echo "   • DOW: $42,400.00 (+300.00 +0.71%)"
echo "   • WTI Crude: $62.00 (-1.50 -2.36%)"
echo "   • Brent Crude: $66.00 (-1.25 -1.86%)"
echo "   • Natural Gas: $2.20 (+0.10 +4.76%)"
echo "   • VIX: 15.00 (-0.50 -3.23%)"
echo "   • 10Y Treasury: 4.40% (+0.05 +1.15%)"
echo ""
echo "🌐 Your webscraper: https://quantumnews-ps23.3jcllc.com"
echo "📱 Mobile access: https://quantumnews-ps23.3jcllc.com"
echo ""
echo "💡 Tips:"
echo "   • Use the 'Refresh' button to get fresh data"
echo "   • Data updates every 5 minutes automatically"
echo "   • '(live)' = real-time data from API"
echo "   • '(cached)' = cached data (within 5 minutes)"
echo "   • '(offline)' = fallback data (when API fails)"
