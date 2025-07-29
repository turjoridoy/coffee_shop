# Troubleshooting 403 Forbidden Error

## 🔍 **Common Causes & Solutions**

### **1. File Permissions**
```bash
# Set proper permissions
chmod 755 /home/u183730229/domains/ludwigpfeiffer.com.bd/public_html/coffee_shop
chmod 644 /home/u183730229/domains/ludwigpfeiffer.com.bd/public_html/coffee_shop/.htaccess
chmod 755 /home/u183730229/domains/ludwigpfeiffer.com.bd/public_html/coffee_shop/passenger_wsgi.py
```

### **2. Python Version**
- Go to Hostinger control panel
- Set Python version to 3.8 or higher
- Restart the application

### **3. File Structure**
Make sure your files are in the correct location:
```
public_html/
├── coffee_shop/
│   ├── passenger_wsgi.py
│   ├── .htaccess
│   ├── manage.py
│   └── ... (all Django files)
└── index.html
```

### **4. Test Steps**

#### **Step 1: Test Basic Access**
Visit: `https://ludwigpfeiffer.com.bd/test.html`
- Should show "Server is working!"

#### **Step 2: Test Python**
Visit: `https://ludwigpfeiffer.com.bd/coffee_shop/test_wsgi.py`
- Should show "Django application is working!"

#### **Step 3: Test Django**
Visit: `https://ludwigpfeiffer.com.bd/coffee_shop/`
- Should show your Django application

### **5. Alternative .htaccess**
If the current .htaccess doesn't work, try this simpler version:

```apache
RewriteEngine On
AddHandler wsgi-script .py
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ passenger_wsgi.py/$1 [QSA,L]
```

### **6. Check Error Logs**
- Go to Hostinger control panel
- Check error logs for specific error messages
- Look for Python or Apache errors

### **7. Contact Hostinger Support**
If nothing works:
1. Contact Hostinger support
2. Ask them to enable Python applications
3. Verify Python version is set correctly
4. Check if mod_rewrite is enabled

## 🚀 **Quick Fix**
Try uploading these files in this order:
1. `passenger_wsgi.py`
2. `.htaccess`
3. `test.html`
4. Rest of Django files