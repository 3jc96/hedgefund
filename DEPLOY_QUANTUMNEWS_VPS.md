## Quantum News (PS23) VPS Deployment (Option A)

This guide deploys the Flask app behind gunicorn on port 8082 and a Cloudflare named tunnel, kept alive by systemd.

### 1) Prepare the VPS

```bash
sudo apt update && sudo apt install -y python3-venv python3-pip git cloudflared
sudo useradd -r -m -s /usr/sbin/nologin quantumnews || true
```

### 2) Clone repo and set up venv

```bash
sudo -iu quantumnews bash -lc '
  git clone https://your-repo.git quantum-webscraper || true
  cd quantum-webscraper
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt gunicorn
'
```

Ensure `wsgi.py` exists and `cloudflare-tunnel.yml` points to `localhost:8082` for the quantumnews hostname.

### 3) Cloudflare tunnel credentials

On the VPS, authenticate cloudflared and create/use a named tunnel. Place credentials at `/etc/cloudflared/*.json` and copy your repo `cloudflare-tunnel.yml` to `/etc/cloudflared/config.yml`.

```bash
sudo mkdir -p /etc/cloudflared
sudo cp /home/quantumnews/quantum-webscraper/cloudflare-tunnel.yml /etc/cloudflared/config.yml
sudo chown -R root:root /etc/cloudflared
```

Edit `/etc/cloudflared/config.yml` to reference your actual `tunnel:` and `credentials-file:` paths.

### 4) systemd service: Quantum News

Create `/etc/systemd/system/quantumnews.service`:

```ini
[Unit]
Description=Quantum News (gunicorn)
After=network.target

[Service]
User=quantumnews
Group=quantumnews
WorkingDirectory=/home/quantumnews/quantum-webscraper
Environment=PORT=8082
Environment=FLASK_SECRET_KEY=change-me
ExecStart=/home/quantumnews/quantum-webscraper/.venv/bin/gunicorn -w 2 -k sync -b 0.0.0.0:8082 wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 5) systemd service: cloudflared

Create `/etc/systemd/system/cloudflared-quantumnews.service`:

```ini
[Unit]
Description=cloudflared tunnel for Quantum News
After=network-online.target
Wants=network-online.target

[Service]
User=root
Group=root
ExecStart=/usr/bin/cloudflared tunnel run
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

This assumes `/etc/cloudflared/config.yml` contains the named tunnel config and credentials.

### 6) Enable and start services

```bash
sudo systemctl daemon-reload
sudo systemctl enable quantumnews cloudflared-quantumnews
sudo systemctl start quantumnews cloudflared-quantumnews
sudo systemctl status quantumnews --no-pager
sudo systemctl status cloudflared-quantumnews --no-pager
```

### 7) Verify

```bash
curl -s http://localhost:8082/health | jq
# Then check your Cloudflare hostname /health
```

### Notes

- Keep `cloudflare-tunnel.yml` in sync: `quantumnews-ps23.3jcllc.com -> http://localhost:8082`.
- Use HTTPS at the Cloudflare edge; origin stays HTTP on 8082.
- To deploy updates: pull repo and restart `quantumnews`.















