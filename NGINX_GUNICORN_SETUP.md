# Nginx + Gunicorn Setup for Coffee Shop Manager

## 🚀 **Setup Instructions**

### **1. Install Nginx and Gunicorn**
```bash
# Install Nginx (if not already installed)
sudo apt update
sudo apt install nginx

# Gunicorn is already in requirements.txt
pip install gunicorn
```

### **2. Configure Nginx**
1. Copy the `nginx.conf` file to `/etc/nginx/sites-available/teatime.ludwigpfeiffer.com.bd`
2. Create a symbolic link:
   ```bash
   sudo ln -s /etc/nginx/sites-available/teatime.ludwigpfeiffer.com.bd /etc/nginx/sites-enabled/
   ```
3. Test Nginx configuration:
   ```bash
   sudo nginx -t
   ```
4. Restart Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

### **3. Start Gunicorn**
```bash
# Make the startup script executable
chmod +x start_gunicorn.sh

# Start Gunicorn
./start_gunicorn.sh
```

### **4. Set up SSL Certificate**
1. Go to Hostinger control panel
2. Set up SSL certificate for `teatime.ludwigpfeiffer.com.bd`
3. Update the SSL certificate paths in `nginx.conf`

### **5. Create Systemd Service (Optional)**
Create `/etc/systemd/system/coffee-shop.service`:
```ini
[Unit]
Description=Coffee Shop Manager Gunicorn
After=network.target

[Service]
User=u183730229
Group=u183730229
WorkingDirectory=/home/u183730229/domains/ludwigpfeiffer.com.bd/public_html/coffee_shop
Environment="PATH=/home/u183730229/domains/ludwigpfeiffer.com.bd/public_html/coffee_shop/env/bin"
ExecStart=/home/u183730229/domains/ludwigpfeiffer.com.bd/public_html/coffee_shop/env/bin/gunicorn --config gunicorn.conf.py conf.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

Then enable and start the service:
```bash
sudo systemctl enable coffee-shop
sudo systemctl start coffee-shop
```

## 🔧 **Configuration Files**

### **gunicorn.conf.py** - Gunicorn configuration
### **nginx.conf** - Nginx server configuration
### **start_gunicorn.sh** - Startup script

## 📱 **PWA Features**
- **Domain**: `https://teatime.ludwigpfeiffer.com.bd`
- **PWA Installation**: Works on mobile and desktop
- **Offline Support**: Service worker enabled
- **HTTPS**: Required for PWA installation

## 🛠️ **Troubleshooting**

### **Check Gunicorn Status**
```bash
ps aux | grep gunicorn
```

### **Check Nginx Status**
```bash
sudo systemctl status nginx
```

### **View Logs**
```bash
# Gunicorn logs
tail -f /home/u183730229/logs/gunicorn_error.log

# Nginx logs
sudo tail -f /var/log/nginx/error.log
```

### **Test Application**
Visit: `https://teatime.ludwigpfeiffer.com.bd`

## 🎉 **Benefits of Nginx + Gunicorn**
- ✅ **Better Performance**: Nginx handles static files efficiently
- ✅ **Load Balancing**: Can handle multiple Gunicorn workers
- ✅ **SSL Termination**: Nginx handles SSL certificates
- ✅ **Caching**: Nginx provides excellent caching
- ✅ **Security**: Better security with proper headers
- ✅ **Scalability**: Easy to scale horizontally