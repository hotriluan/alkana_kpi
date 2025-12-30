# Security Configuration Guide - Alkana KPI System

This guide covers security hardening and configuration for production deployment.

## Table of Contents
- [Pre-Production Security Checklist](#pre-production-security-checklist)
- [Django Settings Security](#django-settings-security)
- [Database Security](#database-security)
- [Web Server Security](#web-server-security)
- [Application Security](#application-security)
- [Monitoring and Auditing](#monitoring-and-auditing)
- [Incident Response](#incident-response)

## Pre-Production Security Checklist

### Critical Items ⚠️

- [ ] **Generate new SECRET_KEY** (never use development key)
- [ ] **Set DEBUG = False** in production
- [ ] **Configure ALLOWED_HOSTS** with actual domain(s)
- [ ] **Use environment variables** for sensitive settings
- [ ] **Enable HTTPS** and obtain SSL certificate
- [ ] **Change default database password**
- [ ] **Review file/directory permissions**
- [ ] **Disable directory listing** on web server
- [ ] **Configure firewall** rules
- [ ] **Set up database backups**
- [ ] **Enable security headers**
- [ ] **Configure CSRF protection**
- [ ] **Set secure cookie flags**
- [ ] **Review user permissions** and limit superusers

### Important Items

- [ ] Configure logging for security events
- [ ] Set up monitoring and alerts
- [ ] Document admin credentials securely
- [ ] Configure rate limiting
- [ ] Enable brute-force protection
- [ ] Set up WAF (Web Application Firewall) if available
- [ ] Configure session timeout
- [ ] Review and minimize installed packages

## Django Settings Security

### Current Insecure Settings (Development)

**⚠️ SECURITY ISSUES** in [alkana_kpi/settings.py](../../alkana_kpi/settings.py):

```python
# LINE 22-24 - CRITICAL SECURITY ISSUES
SECRET_KEY = 'django-insecure-719rxan^3gb4s-v1b5ha8nl68hlqm8jb8*t*+-r2=0gj%q7urf'
DEBUG = True
ALLOWED_HOSTS = []
```

**NEVER deploy to production with these settings!**

---

### Secure Production Settings

Create `.env` file in project root (DO NOT commit to version control):

```ini
# .env file - Add to .gitignore
SECRET_KEY=<your-generated-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_PASSWORD=<strong-database-password>
DB_HOST=localhost
DB_PORT=3306
```

Update `settings.py`:

```python
import os
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-for-development-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
```

Install python-dotenv:
```bash
pip install python-dotenv
```

---

### Generate Secure SECRET_KEY

**Option 1: Using Django**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

**Option 2: Using Python**
```python
import secrets
print(secrets.token_urlsafe(50))
```

**Option 3: Using Command Line (Linux/Mac)**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output to your `.env` file.

---

### Security Headers Configuration

Add to `settings.py`:

```python
# Security Headers (Production Only)
if not DEBUG:
    # HTTPS Security
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Security Headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Cookie Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Lax'
```

---

### CSRF Protection

Configure trusted origins:

```python
# CSRF Protection
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]

# If using IIS with specific port
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://yourdomain.com:8000',
]
```

---

### Session Security

Configure secure session handling:

```python
# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
SESSION_COOKIE_NAME = 'alkana_sessionid'  # Custom name
```

---

### Password Validation

Enforce strong passwords:

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Increased from default 8
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

---

### Logging Configuration

Add security logging:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'maxBytes': 1024*1024*15,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
```

Create logs directory:
```bash
mkdir logs
```

---

## Database Security

### MySQL User Permissions

Create dedicated user with minimal privileges:

```sql
-- Connect as root
mysql -u root -p

-- Create production database
CREATE DATABASE alkana_kpi 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Create production user with strong password
CREATE USER 'alkana_prod'@'localhost' 
IDENTIFIED BY 'StrongP@ssw0rd#2025!';

-- Grant only necessary privileges (NOT ALL PRIVILEGES)
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, INDEX, ALTER 
ON alkana_kpi.* 
TO 'alkana_prod'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;

-- Verify permissions
SHOW GRANTS FOR 'alkana_prod'@'localhost';
```

**Do NOT grant**:
- DROP (prevents accidental table deletion)
- FILE (prevents file system access)
- SUPER (administrative privilege)

---

### Database Connection Security

Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'alkana_kpi'),
        'USER': os.getenv('DB_USER', 'alkana_prod'),
        'PASSWORD': os.getenv('DB_PASSWORD'),  # From .env
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'ssl': {
                'ca': '/path/to/ca-cert.pem',  # If using SSL
            },
        },
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

---

### Database Backup Strategy

**Daily Automated Backup Script** (Linux/Windows):

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/mysql"
DB_NAME="alkana_kpi"
DB_USER="alkana_prod"
DB_PASS="<password>"

# Create backup
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/alkana_kpi_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "alkana_kpi_*.sql.gz" -mtime +30 -delete

# Upload to remote storage (optional)
# aws s3 cp $BACKUP_DIR/alkana_kpi_$DATE.sql.gz s3://your-bucket/backups/
```

**Windows PowerShell Version**:

```powershell
# backup.ps1
$Date = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupDir = "C:\backup\mysql"
$DbName = "alkana_kpi"

# Create backup
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" -u alkana_prod -p alkana_kpi | `
  & "C:\Program Files\7-Zip\7z.exe" a -si "$BackupDir\alkana_kpi_$Date.sql.gz"

# Keep only last 30 days
Get-ChildItem $BackupDir -Filter "alkana_kpi_*.sql.gz" | `
  Where-Object { $_.CreationTime -lt (Get-Date).AddDays(-30) } | `
  Remove-Item
```

**Schedule with Cron (Linux)**:
```bash
crontab -e
# Add: Run daily at 2 AM
0 2 * * * /path/to/backup.sh
```

**Schedule with Task Scheduler (Windows)**:
1. Open Task Scheduler
2. Create Basic Task
3. Schedule: Daily at 2:00 AM
4. Action: Start a program
5. Program: `powershell.exe`
6. Arguments: `-ExecutionPolicy Bypass -File C:\path\to\backup.ps1`

---

## Web Server Security

### IIS Security (Windows)

#### Remove Server Header

Edit `web.config`:

```xml
<configuration>
  <system.webServer>
    <security>
      <requestFiltering removeServerHeader="true" />
    </security>
    
    <httpProtocol>
      <customHeaders>
        <remove name="X-Powered-By" />
        <add name="X-Content-Type-Options" value="nosniff" />
        <add name="X-Frame-Options" value="DENY" />
        <add name="X-XSS-Protection" value="1; mode=block" />
      </customHeaders>
    </httpProtocol>
  </system.webServer>
</configuration>
```

#### Disable Directory Browsing

```xml
<configuration>
  <system.webServer>
    <directoryBrowse enabled="false" />
  </system.webServer>
</configuration>
```

#### Configure SSL/TLS

1. Open IIS Manager
2. Select server → Server Certificates
3. Import/Request SSL certificate
4. Select site → Bindings
5. Add HTTPS binding on port 443
6. Select SSL certificate

**Force HTTPS Redirect**:
```xml
<configuration>
  <system.webServer>
    <rewrite>
      <rules>
        <rule name="HTTP to HTTPS redirect" stopProcessing="true">
          <match url="(.*)" />
          <conditions>
            <add input="{HTTPS}" pattern="off" ignoreCase="true" />
          </conditions>
          <action type="Redirect" url="https://{HTTP_HOST}/{R:1}" redirectType="Permanent" />
        </rule>
      </rules>
    </rewrite>
  </system.webServer>
</configuration>
```

---

### Nginx Security (Linux)

#### Security Headers

Edit `/etc/nginx/sites-available/alkana_kpi`:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Hide Nginx version
    server_tokens off;
    
    # Rate limiting
    limit_req zone=one burst=10 nodelay;
    
    location / {
        proxy_pass http://unix:/var/www/alkana_kpi/alkana_kpi.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /var/www/alkana_kpi/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# Rate limiting zone
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;
```

---

## Application Security

### File Permissions (Linux)

```bash
# Set ownership
sudo chown -R www-data:www-data /var/www/alkana_kpi

# Directories: 755 (rwxr-xr-x)
find /var/www/alkana_kpi -type d -exec chmod 755 {} \;

# Files: 644 (rw-r--r--)
find /var/www/alkana_kpi -type f -exec chmod 644 {} \;

# Sensitive files: 600 (rw-------)
chmod 600 /var/www/alkana_kpi/.env
chmod 600 /var/www/alkana_kpi/db.sqlite3  # If using SQLite

# Python files executable if needed
find /var/www/alkana_kpi -name "*.py" -exec chmod 644 {} \;
chmod +x /var/www/alkana_kpi/manage.py
```

---

### File Permissions (Windows/IIS)

```powershell
# Set permissions for IIS_IUSRS
icacls "C:\inetpub\wwwroot\alkana_kpi" /grant "IIS_IUSRS:(OI)(CI)RX" /T

# Set permissions for IUSR
icacls "C:\inetpub\wwwroot\alkana_kpi" /grant "IUSR:(OI)(CI)RX" /T

# Restrict write access to specific folders only
icacls "C:\inetpub\wwwroot\alkana_kpi\media" /grant "IIS_IUSRS:(OI)(CI)F" /T
icacls "C:\inetpub\wwwroot\alkana_kpi\logs" /grant "IIS_IUSRS:(OI)(CI)F" /T

# Protect sensitive files
icacls "C:\inetpub\wwwroot\alkana_kpi\.env" /inheritance:r /grant "Administrators:F"
```

---

### Input Validation

Django provides automatic protection, but verify:

1. **SQL Injection**: Use Django ORM (no raw SQL without parameterization)
2. **XSS**: Templates auto-escape by default
3. **CSRF**: CSRF middleware enabled
4. **File Uploads**: Validate file types and sizes

**Custom Validation Example**:

```python
# In models.py
from django.core.exceptions import ValidationError

class Alk_KPI_Result(models.Model):
    # ... fields ...
    
    def clean(self):
        # Validate weight between 0 and 1
        if self.weigth and (self.weigth < 0 or self.weigth > 1):
            raise ValidationError({'weigth': 'Weight must be between 0 and 1'})
        
        # Validate min < max
        if self.min and self.max and self.min >= self.max:
            raise ValidationError('Min threshold must be less than max threshold')
        
        # Validate achievement is positive
        if self.achivement and self.achivement < 0:
            raise ValidationError({'achivement': 'Achievement cannot be negative'})
```

---

## Monitoring and Auditing

### Django Admin Logging

Enable admin action logging (built-in):

```python
# Django automatically logs admin actions to django_admin_log table
# Query logs:
from django.contrib.admin.models import LogEntry

# View recent changes
recent_changes = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:100]

for entry in recent_changes:
    print(f"{entry.action_time}: {entry.user} {entry.get_action_flag_display()} {entry}")
```

### Custom Audit Trail

Create audit model:

```python
# models.py
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)  # CREATE, UPDATE, DELETE
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField()
    changes = models.JSONField()
    ip_address = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
```

### Failed Login Monitoring

Install django-axes for brute-force protection:

```bash
pip install django-axes
```

Configure in `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps ...
    'axes',
]

MIDDLEWARE = [
    # ... other middleware ...
    'axes.middleware.AxesMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Axes configuration
AXES_FAILURE_LIMIT = 5  # Lock after 5 failed attempts
AXES_COOLOFF_TIME = 1  # 1 hour lockout
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
```

---

## Incident Response

### Security Incident Checklist

If security breach detected:

1. **Immediate Actions**:
   - [ ] Take affected server offline if necessary
   - [ ] Change all passwords (Django admin, database, server)
   - [ ] Rotate SECRET_KEY
   - [ ] Review access logs for unauthorized access
   - [ ] Check database for unauthorized changes

2. **Investigation**:
   - [ ] Review security logs (`logs/security.log`)
   - [ ] Check Django admin log (`django_admin_log` table)
   - [ ] Review web server access logs
   - [ ] Identify breach entry point
   - [ ] Document timeline of events

3. **Recovery**:
   - [ ] Restore from clean backup if data compromised
   - [ ] Patch security vulnerability
   - [ ] Update all dependencies
   - [ ] Re-deploy with hardened security
   - [ ] Monitor for continued suspicious activity

4. **Post-Incident**:
   - [ ] Document lessons learned
   - [ ] Update security procedures
   - [ ] Notify affected users if required
   - [ ] Consider security audit

### Emergency Contacts

Document contacts for security incidents:
- **IT Security Team**: [contact info]
- **Database Administrator**: [contact info]
- **Server Administrator**: [contact info]
- **Management**: [contact info]

---

## Security Hardening Commands

### Generate New SECRET_KEY and Update Settings

```python
# Step 1: Generate new key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Step 2: Update .env file
echo "SECRET_KEY=<generated-key>" >> .env
echo "DEBUG=False" >> .env
echo "ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com" >> .env

# Step 3: Restart application
# IIS: iisreset
# Systemd: sudo systemctl restart alkana-kpi
```

### Check for Security Issues

```bash
# Django security check
python manage.py check --deploy

# Expected warnings if DEBUG=True or SECRET_KEY exposed
# Fix all WARNINGS before production deployment
```

---

**Last Updated**: December 30, 2025

For deployment details, see [Deployment Guide](deployment-guide.md).
