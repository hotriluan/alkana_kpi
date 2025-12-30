# Deployment Guide - Alkana KPI System

This guide covers deploying the Alkana KPI Management System to production environments, with specific focus on Windows Server with IIS and FastCGI.

## Table of Contents
- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Windows Server + IIS Deployment](#windows-server--iis-deployment)
- [Linux Deployment](#linux-deployment)
- [Database Configuration](#database-configuration)
- [Security Hardening](#security-hardening)
- [Performance Optimization](#performance-optimization)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Pre-Deployment Checklist

### Security Configuration
- [ ] Generate new `SECRET_KEY` (never use development key)
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use environment variables for sensitive data
- [ ] Review database credentials
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up database backups

### Application Preparation
- [ ] Run all tests: `python manage.py test`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Run database migrations: `python manage.py migrate`
- [ ] Create superuser account
- [ ] Document any custom configurations
- [ ] Prepare import data files

### Infrastructure
- [ ] Verify server specifications (4GB RAM minimum)
- [ ] Install required software (Python, MySQL, IIS/Apache/Nginx)
- [ ] Set up domain and DNS
- [ ] Obtain SSL certificates
- [ ] Configure backup storage

## Windows Server + IIS Deployment

This is the primary deployment method based on the existing `web.config` file.

### Prerequisites

- Windows Server 2016 or later
- IIS 10.0 or later with CGI module
- Python 3.8+ installed
- MySQL 8.0 installed

### Step 1: Install IIS and Required Components

```powershell
# Run PowerShell as Administrator
# Install IIS
Install-WindowsFeature -name Web-Server -IncludeManagementTools

# Install CGI module
Install-WindowsFeature Web-CGI
```

Alternatively, use Server Manager:
1. Open Server Manager
2. Add Roles and Features
3. Select Web Server (IIS)
4. Under Application Development, check:
   - CGI
   - ISAPI Extensions
   - ISAPI Filters

### Step 2: Install Python

1. Download Python from https://www.python.org/downloads/
2. Run installer with options:
   - **Add Python to PATH** ✓
   - Install for all users
   - Custom installation location: `C:\Python3\` (recommended)

3. Verify installation:
```cmd
C:\Python3\python.exe --version
```

### Step 3: Install wfastcgi

```cmd
C:\Python3\python.exe -m pip install wfastcgi
C:\Python3\Scripts\wfastcgi-enable
```

Note the output path (e.g., `C:\Python3\Scripts\wfastcgi.py`)

### Step 4: Prepare Application Directory

```powershell
# Create application directory
New-Item -ItemType Directory -Path C:\inetpub\wwwroot\alkana_kpi

# Copy application files
Copy-Item -Path .\* -Destination C:\inetpub\wwwroot\alkana_kpi\ -Recurse

# Navigate to application directory
cd C:\inetpub\wwwroot\alkana_kpi
```

### Step 5: Install Python Dependencies

```cmd
# Create virtual environment (optional but recommended)
C:\Python3\python.exe -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install wfastcgi
```

### Step 6: Configure Environment Variables

Create `.env` file in project root:
```ini
# .env file (DO NOT commit to version control)
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=alkana_kpi
DB_USER=alkana_user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306
```

Update `settings.py` to use environment variables:
```python
import os
from pathlib import Path

# Load environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-key-for-dev')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'alkana_kpi'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
```

### Step 7: Configure web.config

The existing `web.config` should be updated for your environment:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="Python FastCGI" 
           path="*" 
           verb="*" 
           modules="FastCgiModule" 
           scriptProcessor="C:\Python3\python.exe|C:\Python3\Scripts\wfastcgi.py" 
           resourceType="Unspecified" 
           requireAccess="Script" />
    </handlers>
  </system.webServer>
  
  <appSettings>
    <!-- Django settings -->
    <add key="PYTHONPATH" value="C:\inetpub\wwwroot\alkana_kpi" />
    <add key="WSGI_HANDLER" value="alkana_kpi.wsgi.application" />
    <add key="DJANGO_SETTINGS_MODULE" value="alkana_kpi.settings" />
    
    <!-- Environment -->
    <add key="WSGI_LOG" value="C:\inetpub\logs\alkana_kpi.log" />
  </appSettings>
</configuration>
```

**Static files web.config** (place in `staticfiles/web.config`):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <clear />
      <add name="StaticFile" 
           path="*" 
           verb="*" 
           modules="StaticFileModule" 
           resourceType="File" 
           requireAccess="Read" />
    </handlers>
  </system.webServer>
</configuration>
```

### Step 8: Create IIS Site

```powershell
# Import IIS module
Import-Module WebAdministration

# Create application pool
New-WebAppPool -Name "AlkanaKPIPool"
Set-ItemProperty IIS:\AppPools\AlkanaKPIPool -Name managedRuntimeVersion -Value ""

# Create IIS site
New-Website -Name "AlkanaKPI" `
            -Port 80 `
            -PhysicalPath "C:\inetpub\wwwroot\alkana_kpi" `
            -ApplicationPool "AlkanaKPIPool"

# Set permissions
icacls "C:\inetpub\wwwroot\alkana_kpi" /grant "IIS_IUSRS:(OI)(CI)F" /T
icacls "C:\inetpub\wwwroot\alkana_kpi" /grant "IUSR:(OI)(CI)F" /T
```

**Or use IIS Manager GUI:**
1. Open IIS Manager
2. Right-click Sites → Add Website
3. Site name: `AlkanaKPI`
4. Physical path: `C:\inetpub\wwwroot\alkana_kpi`
5. Port: `80` (or `443` for HTTPS)
6. Click OK

### Step 9: Configure FastCGI

```powershell
# Add FastCGI application
$appConfig = Get-WebConfiguration system.webServer/fastCgi
$app = $appConfig.Collection | Where-Object { $_.fullPath -eq 'C:\Python3\python.exe' }
if ($app -eq $null) {
    Add-WebConfiguration system.webServer/fastCgi -Value @{
        fullPath='C:\Python3\python.exe'
        arguments='C:\Python3\Scripts\wfastcgi.py'
        maxInstances=4
        instanceMaxRequests=10000
        activityTimeout=300
        requestTimeout=300
    }
}
```

### Step 10: Run Database Migrations

```cmd
cd C:\inetpub\wwwroot\alkana_kpi
C:\Python3\python.exe manage.py migrate
C:\Python3\python.exe manage.py collectstatic --noinput
C:\Python3\python.exe manage.py createsuperuser
```

### Step 11: Configure SSL (Recommended)

1. Obtain SSL certificate (Let's Encrypt, commercial CA, or self-signed)
2. In IIS Manager:
   - Select your site
   - Bindings → Add
   - Type: https
   - Port: 443
   - SSL certificate: Select your certificate
   - Click OK

3. Force HTTPS in `settings.py`:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Step 12: Test Deployment

1. Restart IIS:
```powershell
iisreset
```

2. Open browser and navigate to:
   - http://yourdomain.com/admin
   - https://yourdomain.com/admin (if SSL configured)

3. Check logs if issues occur:
   - `C:\inetpub\logs\alkana_kpi.log`
   - Windows Event Viewer

## Linux Deployment

### Using Gunicorn + Nginx (Ubuntu/Debian)

#### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install python3 python3-venv python3-dev
sudo apt install mysql-server libmysqlclient-dev
sudo apt install nginx
```

#### 2. Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/alkana_kpi
sudo chown $USER:$USER /var/www/alkana_kpi
cd /var/www/alkana_kpi

# Clone/copy application
git clone <repository-url> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

#### 3. Configure Gunicorn

Create `/etc/systemd/system/alkana-kpi.service`:

```ini
[Unit]
Description=Alkana KPI Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/alkana_kpi
Environment="PATH=/var/www/alkana_kpi/venv/bin"
ExecStart=/var/www/alkana_kpi/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/alkana_kpi/alkana_kpi.sock \
          alkana_kpi.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start alkana-kpi
sudo systemctl enable alkana-kpi
```

#### 4. Configure Nginx

Create `/etc/nginx/sites-available/alkana_kpi`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/alkana_kpi/staticfiles/;
    }

    location / {
        proxy_pass http://unix:/var/www/alkana_kpi/alkana_kpi.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/alkana_kpi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Database Configuration

### Production MySQL Settings

```sql
-- Create production database with proper encoding
CREATE DATABASE alkana_kpi 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Create dedicated user with limited privileges
CREATE USER 'alkana_prod'@'localhost' IDENTIFIED BY 'strong_random_password';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, INDEX, ALTER 
ON alkana_kpi.* TO 'alkana_prod'@'localhost';
FLUSH PRIVILEGES;

-- Configure MySQL for performance
SET GLOBAL innodb_buffer_pool_size = 1G;
SET GLOBAL max_connections = 200;
```

### Backup Strategy

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/mysql"
mysqldump -u alkana_prod -p alkana_kpi | gzip > $BACKUP_DIR/alkana_kpi_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "alkana_kpi_*.sql.gz" -mtime +30 -delete
```

## Security Hardening

### Django Settings (settings.py)

```python
# Production security settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security middleware
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Cookie security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']
```

### File Permissions (Linux)

```bash
# Set proper ownership
sudo chown -R www-data:www-data /var/www/alkana_kpi

# Secure permissions
find /var/www/alkana_kpi -type d -exec chmod 755 {} \;
find /var/www/alkana_kpi -type f -exec chmod 644 {} \;
chmod 600 /var/www/alkana_kpi/.env
```

## Performance Optimization

### Django Caching

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

### Database Optimization

```python
# Enable persistent connections
DATABASES = {
    'default': {
        # ... other settings ...
        'CONN_MAX_AGE': 600,  # 10 minutes
    }
}
```

### Static File Compression

```bash
# Compress static files
python manage.py collectstatic --noinput
gzip -r staticfiles/
```

## Monitoring and Maintenance

### Log Locations

**Windows:**
- Application logs: `C:\inetpub\logs\alkana_kpi.log`
- IIS logs: `C:\inetpub\logs\LogFiles\`
- Django logs: Configure in settings.py

**Linux:**
- Gunicorn: `journalctl -u alkana-kpi`
- Nginx: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- Django: `/var/www/alkana_kpi/logs/django.log`

### Health Checks

Create `healthcheck.py` management command:
```python
# management/commands/healthcheck.py
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            connection.ensure_connection()
            self.stdout.write('OK')
        except Exception as e:
            self.stdout.write(f'FAIL: {e}')
```

### Automated Monitoring

Set up cron job (Linux) or Scheduled Task (Windows):
```bash
# Check health every 5 minutes
*/5 * * * * /var/www/alkana_kpi/venv/bin/python /var/www/alkana_kpi/manage.py healthcheck
```

## Troubleshooting

See [Troubleshooting Guide](troubleshooting.md) for common deployment issues.

---

**Last Updated**: December 30, 2025
