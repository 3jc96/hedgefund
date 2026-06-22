# Quantum Capital News

Flask app for multi-source financial news aggregation, sentiment analysis, and live market data.

## Local run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your ALPHA_VANTAGE_API_KEY
python app.py
```

Open http://localhost:8080 — health check at `/health`.

## Deploy to Render

1. Push this folder to GitHub (see below).
2. [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint** → connect the repo.
3. Render reads `render.yaml` and creates the `quantum-news` web service.
4. In the service **Environment** tab, set:
   - `ALPHA_VANTAGE_API_KEY` — your Alpha Vantage key (optional; yfinance fallback works without it)
5. Deploy. Your app URL will be `https://quantum-news.onrender.com` (or similar).

Free tier spins down after inactivity; first request may take ~30s to wake.

## Deploy to GitHub

From this directory:

```bash
git init
git add .
git commit -m "Initial Quantum News deploy (Render-ready)"
git branch -M main
git remote add origin https://github.com/YOUR_USER/quantum-news.git
git push -u origin main
```

Replace `YOUR_USER/quantum-news` with your repo. Create an empty repo on GitHub first (no README).

## API routes

| Route | Description |
|-------|-------------|
| `/` | Main news dashboard |
| `/health` | Render health check |
| `/api/news` | Portfolio news JSON |
| `/api/market-data` | Live market quotes |
| `/api/calendar` | Economic calendar |

## Notes

- `wsgi.py` exposes `application` for gunicorn.
- Secrets belong in environment variables, not in `config.py`.
- VPS + Cloudflare tunnel docs: `DEPLOY_QUANTUMNEWS_VPS.md`.
