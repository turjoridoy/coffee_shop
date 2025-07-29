# Coffee Shop Manager - Hostinger Deployment Guide

## 🚀 Quick Setup for Hostinger

### 1. Upload Files
- Upload all project files to your Hostinger domain directory
- Make sure to include all files and folders

### 2. Create Virtual Environment
```bash
cd /home/u183730229/domains/yourdomain.com/public_html
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
- Create MySQL database: `u183730229_coffee_shop`
- Database credentials are already configured in `conf/settings.py`

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Load Initial Data
```bash
python manage.py seed_data
```

### 8. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 9. Configure Hostinger
- Set Python version to 3.8+ in Hostinger control panel
- Configure domain to point to your Django app
- Set up SSL certificate

### 10. Configure Hostinger Settings
- Set Python version to 3.8+ in Hostinger control panel
- Configure domain to point to your Django app
- Set up SSL certificate

### 11. File Structure
Your files should be organized like this:
```
public_html/
├── coffee_shop/          # Your Django project
│   ├── manage.py
│   ├── passenger_wsgi.py
│   ├── .htaccess
│   └── ... (all Django files)
├── index.html            # Redirect to Django app
└── .htaccess            # Main domain .htaccess
```

### 12. Test Your Setup
1. Visit: `https://ludwigpfeiffer.com.bd/coffee_shop/`
2. Should redirect to your Django application
3. Check if static files load properly

## 🔧 Configuration Files

### Database Settings
Already configured in `conf/settings.py`:
- Database: `u183730229_coffee_shop`
- User: `u183730229_root`
- Password: `NtZYc@cuCz6@`

### Static Files
- Static files will be collected to `staticfiles/` directory
- Configure your web server to serve from this directory

## 📱 PWA Features
- Progressive Web App ready
- Installable on mobile devices
- Offline capabilities
- Native app-like experience

## 🛠️ Troubleshooting

### Common Issues:
1. **Import Error**: Make sure PyMySQL is installed
2. **Database Connection**: Verify MySQL credentials
3. **Static Files**: Run `collectstatic` command
4. **Permissions**: Ensure proper file permissions

### Logs:
- Check error logs in Hostinger control panel
- Django logs will be in your application directory

## 🌐 Access Your App
- Main app: `https://yourdomain.com`
- Admin panel: `https://yourdomain.com/admin`

## 📞 Support
For issues with deployment, check:
1. Hostinger documentation
2. Django deployment guide
3. Error logs in Hostinger control panel