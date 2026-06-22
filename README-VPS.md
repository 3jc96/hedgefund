# VPS Deployment Guide for Quantum News Webscraper

This guide will help you deploy your Quantum News Webscraper to a VPS with persistent Cloudflare tunnel.

## Prerequisites

1. **VPS Provider**: DigitalOcean, Linode, Vultr, AWS EC2, etc.
2. **VPS Specs**: 
   - Ubuntu 22.04 LTS
   - 1GB RAM minimum (2GB recommended)
   - 25GB storage minimum
   - Root/sudo access

## Step 1: Get a VPS

### Recommended Providers:
- **DigitalOcean**: $6/month for 1GB RAM, 25GB SSD
- **Linode**: $5/month for 1GB RAM, 25GB SSD  
- **Vultr**: $6/month for 1GB RAM, 25GB SSD

### VPS Setup:
1. Create a new droplet/server
2. Choose Ubuntu 22.04 LTS
3. Select the smallest size (1GB RAM)
4. Add your SSH key or set a root password
5. Note down your VPS IP address

## Step 2: Upload Your Application

1. **Update the upload script**:
   ```bash
   nano upload-to-vps.sh
   # Change YOUR_VPS_IP_HERE to your actual VPS IP
   ```

2. **Run the upload script**:
   ```bash
   chmod +x upload-to-vps.sh
   ./upload-to-vps.sh
   ```

## Step 3: Deploy on VPS

SSH into your VPS and run the deployment scripts:

```bash
# SSH into your VPS
ssh root@YOUR_VPS_IP

# Run the deployment script
cd /opt/quantum-webscraper
chmod +x *.sh
./vps-deploy.sh
```

## Step 4: Set Up Systemd Services

```bash
# Run the systemd setup
sudo ./setup-systemd.sh
```

## Step 5: Install and Configure Cloudflare Tunnel

```bash
# Install cloudflared
sudo ./install-cloudflared.sh

# Login to Cloudflare
cloudflared tunnel login

# Create a new tunnel (or use existing)
cloudflared tunnel create quantumnews

# Route DNS to your domain
cloudflared tunnel route dns quantumnews quantumnews-ps23.3jcllc.com

# Copy tunnel credentials
cp ~/.cloudflared/*.json /etc/cloudflared/

# Update config with your tunnel ID
nano /etc/cloudflared/config.yml
```

## Step 6: Start Services

```bash
# Start the services
sudo systemctl start quantumnews
sudo systemctl start cloudflared

# Enable auto-start on boot
sudo systemctl enable quantumnews
sudo systemctl enable cloudflared

# Check status
sudo systemctl status quantumnews
sudo systemctl status cloudflared
```

## Step 7: Verify Deployment

```bash
# Check if Flask app is running
curl http://127.0.0.1:8082/health

# Check if tunnel is connected
sudo systemctl status cloudflared

# Test your public domain
curl https://quantumnews-ps23.3jcllc.com/health
```

## Monitoring and Maintenance

### Check Service Status:
```bash
sudo systemctl status quantumnews
sudo systemctl status cloudflared
```

### View Logs:
```bash
sudo journalctl -u quantumnews -f
sudo journalctl -u cloudflared -f
```

### Restart Services:
```bash
sudo systemctl restart quantumnews
sudo systemctl restart cloudflared
```

### Update Application:
1. Upload new files using `upload-to-vps.sh`
2. Restart the service: `sudo systemctl restart quantumnews`

## Troubleshooting

### If Flask app won't start:
```bash
# Check logs
sudo journalctl -u quantumnews -f

# Check if port is in use
sudo lsof -i :8082

# Test manually
cd /opt/quantum-webscraper
source .venv/bin/activate
python app.py
```

### If tunnel won't connect:
```bash
# Check tunnel config
cat /etc/cloudflared/config.yml

# Test tunnel manually
cloudflared tunnel --config /etc/cloudflared/config.yml run quantumnews

# Check DNS
dig quantumnews-ps23.3jcllc.com
```

## Security Notes

1. **Firewall**: Consider setting up UFW firewall
2. **SSH**: Use SSH keys instead of passwords
3. **Updates**: Keep your VPS updated
4. **Monitoring**: Set up log monitoring

## Cost Breakdown

- **VPS**: $5-6/month
- **Domain**: Already owned
- **Cloudflare**: Free
- **Total**: ~$6/month for 24/7 hosting

This setup will run your application 24/7 even when your local machine is off!











