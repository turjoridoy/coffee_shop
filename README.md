# ☕ Tea Time

A Progressive Web App (PWA) for managing coffee shop sales, built with Django and modern web technologies.

## 🚀 Features

- **📱 PWA Support**: Install as native app
- **🔐 User Authentication**: Phone-based login system
- **💰 Sales Management**: Add and track sales
- **📊 Dashboard**: Real-time sales analytics
- **📋 Reports**: Generate and copy sales summaries
- **🎨 Modern UI**: Responsive design with beautiful interface
- **⚡ Offline Support**: Works without internet connection

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7
- **API**: Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development)
- **PWA**: Service Worker, Web App Manifest
- **Authentication**: Custom phone-based user system

## 📱 PWA Features

- ✅ **Installable**: Add to home screen
- ✅ **Offline Support**: Works without internet
- ✅ **App Shortcuts**: Quick access to key features
- ✅ **Native Feel**: Standalone app experience
- ✅ **Push Ready**: Ready for notifications

## 🚀 Live Demo

**Deployed on Render**: [Your App URL will be here]

## 📦 Installation

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd coffee_shop
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Create superuser**
```bash
python manage.py createsuperuser
```

5. **Seed sample data**
```bash
python manage.py seed_data
```

6. **Run development server**
```bash
python manage.py runserver
```

7. **Access the app**
   - Open: `http://localhost:8000`
   - Login with your superuser credentials

## 🌐 Deployment

### Render (Free)

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Sign up/Login with GitHub
   - Click "New Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - **Name**: `coffee-shop-manager`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn conf.wsgi:application`
   - **Plan**: Free

4. **Environment Variables**
   - `DEBUG`: `False`
   - `SECRET_KEY`: Generate a new secret key

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)

## 📱 PWA Testing

### Chrome Desktop
1. Open Chrome DevTools (F12)
2. Go to Application tab
3. Check Manifest and Service Workers
4. Look for install button in address bar

### Mobile Testing
1. Open Chrome on mobile
2. Visit your deployed URL
3. Tap "Add to Home Screen"
4. App will install like a native app

## 🔧 Configuration

### Environment Variables
- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Your domain

### Database
- **Development**: SQLite
- **Production**: PostgreSQL (recommended)

## 📊 Features Overview

### Dashboard
- Today's sales total
- Transaction count
- Monthly revenue
- Recent sales list

### Sales Management
- Add new sales
- Quick action buttons
- Category and payment method selection
- Customer information

### Reports
- Today's summary
- Category breakdown
- Payment method analysis
- Copy summary feature

### User Management
- Phone-based authentication
- User active/inactive status
- Admin panel access

## 🎯 Quick Start

1. **Access the app**: Visit your deployed URL
2. **Login**: Use your superuser credentials
3. **Add sales**: Use the "Add Sale" tab
4. **View reports**: Check the "Reports" tab
5. **Install PWA**: Click install button for app-like experience

## 📞 Support

For issues or questions:
- Check the deployment logs on Render
- Verify environment variables
- Test PWA features in Chrome DevTools

## 🔄 Updates

The app automatically deploys when you push changes to GitHub.

---

**Built with ❤️ using Django and PWA technologies**