# 🌐 Current Cloudflare Tunnel URL

## ✅ Status: ACTIVE

Your Quantum Webscraper is accessible via Cloudflare Tunnel!

## 🔗 Current Access URLs

### Primary URL (Quick Tunnel)
```
https://[auto-generated-subdomain].trycloudflare.com
```

**Note:** The URL changes each time you restart the tunnel. Use the script below to find the current URL.

### Local Access
```
http://192.168.0.4:8081
http://localhost:8081
```

## 🚀 Quick Start Commands

### Start the Tunnel
```bash
cloudflared tunnel --url http://localhost:5002
```

### Start the Webscraper
```bash
python start_server.py
```

### Find Current URL
```bash
./get_tunnel_url.sh
```

### Start the Webscraper
```bash
python app.py
```

### Stop All Tunnels
```bash
pkill -f "cloudflared tunnel"
```

## 📱 Mobile Access

1. **Get the current URL** from the tunnel output
2. **Open your phone's browser**
3. **Enter the URL** (starts with `https://` and ends with `.trycloudflare.com`)
4. **Enjoy your webscraper from anywhere!** 🌍

## 🔄 URL Changes

The auto-generated URL changes each time you restart the tunnel. To get a consistent URL, you can:

1. **Use the named tunnel** (more complex setup)
2. **Use your own domain** (requires Cloudflare domain)
3. **Keep the current setup** (simple, works great)

## 🛠️ Troubleshooting

### Can't Access?
1. Make sure the tunnel is running: `ps aux | grep cloudflared`
2. Check the webscraper is running: `curl http://localhost:8081/health`
3. Restart the tunnel if needed

### Want to Stop?
```bash
pkill -f "cloudflared tunnel"
```

---

**Your webscraper is globally accessible!** 🚀
