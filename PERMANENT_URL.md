# 🌐 Quantum Webscraper - Permanent URL

## 📡 **Your Permanent URL:**
```
https://quantumnews-ps23.trycloudflare.com.3jcllc.com
```

## 🚀 **Quick Start:**

### Option 1: Use the Permanent Tunnel Script (Recommended)
```bash
./start_permanent_quantumnews.sh
```

### Option 2: Manual Start
```bash
# Terminal 1: Start the webscraper
python start_server.py

# Terminal 2: Start the tunnel
cloudflared tunnel --config cloudflare-tunnel.yml run quantum-webscraper
```

## ✅ **Features:**
- **Permanent URL** - Same URL every time you restart
- **Mobile Access** - Works on phones and tablets
- **Live Market Data** - Real-time S&P 500, NASDAQ, DOW, WTI, Brent, etc.
- **News Scraping** - Latest financial news with sentiment analysis
- **Portfolio Management** - Track your investments
- **Mobile Optimized** - Perfect for reading on the go

## 📱 **Mobile Access:**
Open this URL on your phone: `https://quantumnews-ps23.trycloudflare.com.3jcllc.com`

## 🔧 **Troubleshooting:**
- If the permanent URL doesn't work, try the quick tunnel: `cloudflared tunnel --url http://localhost:5004`
- Make sure the webscraper is running: `curl http://localhost:5004/health`
- Check tunnel status: `ps aux | grep cloudflared`

## 🌍 **Global Access:**
This URL works from anywhere in the world - no VPN needed!

## 🔗 **URL Setup:**
The permanent URL is already configured. To verify:
```bash
cloudflared tunnel route dns f78a95c2-e669-4884-a90e-6ea49a609fa9 quantumnews-ps23.trycloudflare.com
```

## 📊 **Current Status:**
- ✅ Named tunnel configured
- ✅ DNS route established
- ✅ Server running on port 5004
- ✅ Permanent URL: `quantumnews-ps23.trycloudflare.com.3jcllc.com`
