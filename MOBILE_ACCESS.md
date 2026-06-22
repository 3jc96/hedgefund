# 📱 Mobile Access Guide

## Quick Access URLs

### From Your Phone (Same WiFi Network)
```
http://192.168.0.4:8081
```

### From Your Computer
```
http://localhost:8081
```

## How to Access from Your Phone

1. **Make sure your phone is on the same WiFi network as your computer**
2. **Open your phone's web browser** (Safari, Chrome, etc.)
3. **Enter the URL:** `http://192.168.0.4:8081`
4. **Enjoy your news webscraper!** 📰

## Features Available on Mobile

✅ **Portfolio Management** - Add/remove stocks and commodities
✅ **Real-time News** - Live scraping from multiple sources
✅ **Clickable Articles** - Tap headlines to read full articles
✅ **Sentiment Analysis** - See market sentiment scores
✅ **Mobile-Responsive Design** - Optimized for phone screens

## Article Links

- **Headlines are clickable** - Tap any article headline to open the full article
- **"Read Full Article" buttons** - Clear call-to-action buttons
- **Opens in new tab** - Articles open in a new browser tab

## Troubleshooting

### Can't Access from Phone?
1. Check that both devices are on the same WiFi network
2. Make sure the server is running (`python app.py`)
3. Try the IP address: `192.168.0.4:8081`

### Want Internet Access?
For access from anywhere (not just your WiFi), you can:
1. Use ngrok: `ngrok http 8081`
2. Deploy to a cloud service
3. Set up port forwarding on your router

## Quick Start Commands

```bash
# Start the server
python app.py

# Or use the auto-port finder
python start_server.py

# Check if server is running
curl http://localhost:8081/health
```

## News Sources Included

- 📈 Yahoo Finance (stocks)
- 📊 Bloomberg Markets
- 📰 Reuters Business
- ⚡ MarketWatch
- 🔋 Bloomberg Energy
- 🌾 Bloomberg Commodities

---

**Happy News Scraping!** 🚀


