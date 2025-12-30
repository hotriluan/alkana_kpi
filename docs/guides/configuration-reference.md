# Configuration Reference - Alkana KPI System

Complete reference for all configuration settings in the Django project.

## Table of Contents
- [Environment Variables](#environment-variables)
- [Django Settings](#django-settings)
- [Database Configuration](#database-configuration)
- [Static Files](#static-files)
- [Import/Export Configuration](#importexport-configuration)
- [Logging Configuration](#logging-configuration)
- [Email Configuration](#email-configuration)

## Environment Variables

### Recommended .env File

Create `.env` in project root (add to `.gitignore`):

```ini
# Security
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=alkana_kpi
DB_USER=alkana_prod
DB_PASSWORD=your-strong-password
DB_HOST=localhost
DB_PORT=3306

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@company.com
EMAIL_HOST_PASSWORD=your-email-password

# Timezone
TIME_ZONE=Asia/Bangkok
```

### Loading Environment Variables

Install and configure python-dotenv:

```bash
pip install python-dotenv
```

In `settings.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

---

## Django Settings

### Core Settings

**File**: [alkana_kpi/settings.py](../../alkana_kpi/settings.py)

#### SECRET_KEY

**Default**: `'django-insecure-...'` (⚠️ CHANGE IN PRODUCTION)  
**Type**: String  
**Required**: Yes

```python
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-key-for-dev')
```

**Generate new key**:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

#### DEBUG

**Default**: `True` (⚠️ SET False IN PRODUCTION)  
**Type**: Boolean  
**Required**: Yes

```python
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

**Impact**:
- `True`: Shows detailed error pages, serves static files
- `False`: Shows generic error pages, requires proper static file serving

---

#### ALLOWED_HOSTS

**Default**: `[]` (⚠️ CONFIGURE IN PRODUCTION)  
**Type**: List of strings  
**Required**: Yes (when DEBUG=False)

```python
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
```

**Example**:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', '192.168.1.100']
```

---

#### INSTALLED_APPS

**Type**: List of strings  
**Required**: Yes

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',           # Excel import/export
    'slick_reporting',         # Reporting framework
    'kpi_app',                 # Main application
]
```

---

#### MIDDLEWARE

**Type**: List of strings  
**Required**: Yes

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

#### ROOT_URLCONF

**Default**: `'alkana_kpi.urls'`  
**Type**: String  
**Required**: Yes

```python
ROOT_URLCONF = 'alkana_kpi.urls'
```

---

#### WSGI_APPLICATION

**Default**: `'alkana_kpi.wsgi.application'`  
**Type**: String  
**Required**: Yes (for WSGI deployment)

```python
WSGI_APPLICATION = 'alkana_kpi.wsgi.application'
```

---

### Template Configuration

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

---

### Internationalization

```python
LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
# Common values:
# - 'UTC'
# - 'Asia/Bangkok'
# - 'America/New_York'

USE_I18N = True

USE_TZ = True
```

---

## Database Configuration

### MySQL Configuration

**File**: [alkana_kpi/settings.py](../../alkana_kpi/settings.py#L80-L89)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'alkana_kpi'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 600,  # Connection pooling (10 minutes)
    }
}
```

### Database Options

| Option | Description | Default |
|--------|-------------|---------|
| `ENGINE` | Database backend | `django.db.backends.mysql` |
| `NAME` | Database name | `alkana_kpi` |
| `USER` | Database user | `root` |
| `PASSWORD` | Database password | Empty string |
| `HOST` | Database host | `localhost` |
| `PORT` | Database port | `3306` |
| `init_command` | SQL commands to run on connect | SET sql_mode |
| `charset` | Character set | `utf8mb4` |
| `CONN_MAX_AGE` | Connection lifetime (seconds) | `600` |

### Database Connection Pooling

**CONN_MAX_AGE**:
- `0`: Close connection after each request (default, no pooling)
- `600`: Keep connections for 10 minutes
- `None`: Persistent connections (not recommended)

**Recommendation**: Use `600` for production

---

## Static Files

### Static File Settings

```python
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'kpi_app' / 'static',
]
```

### Static File Locations

| Setting | Value | Purpose |
|---------|-------|---------|
| `STATIC_URL` | `/static/` | URL prefix for static files |
| `STATIC_ROOT` | `<BASE_DIR>/staticfiles/` | Collected static files location |
| `STATICFILES_DIRS` | `[<BASE_DIR>/kpi_app/static/]` | Additional static file locations |

### Collecting Static Files

```bash
python manage.py collectstatic --noinput
```

Collects all static files to `STATIC_ROOT` for production serving.

---

## Import/Export Configuration

### Settings

**File**: [alkana_kpi/settings.py](../../alkana_kpi/settings.py#L144-L146)

```python
IMPORT_EXPORT_USE_TRANSACTIONS = True

IMPORT_EXPORT_FORMATS = [
    'import_export.formats.base_formats.XLSX',
    'import_export.formats.base_formats.CSV',
]
```

### Configuration Options

| Setting | Value | Description |
|---------|-------|-------------|
| `IMPORT_EXPORT_USE_TRANSACTIONS` | `True` | Wrap imports in database transactions (rollback on error) |
| `IMPORT_EXPORT_FORMATS` | List | Allowed import/export formats |

### Supported Formats

- **XLSX**: Excel 2007+ (recommended)
- **CSV**: Comma-separated values
- **XLS**: Excel 97-2003 (requires xlrd)
- **JSON**: JSON format
- **YAML**: YAML format

---

## Logging Configuration

### Basic Logging Setup

```python
import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### Log Levels

| Level | When to Use |
|-------|-------------|
| `DEBUG` | Detailed diagnostic information |
| `INFO` | General informational messages |
| `WARNING` | Warning messages (default) |
| `ERROR` | Error messages |
| `CRITICAL` | Critical errors |

---

## Email Configuration

### Gmail SMTP Example

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@yourdomain.com')
```

### Email Backends

| Backend | Use Case |
|---------|----------|
| `smtp.EmailBackend` | Production (real emails) |
| `console.EmailBackend` | Development (print to console) |
| `filebased.EmailBackend` | Testing (save to file) |
| `locmem.EmailBackend` | Testing (in-memory) |

### Development Email Backend

```python
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## Security Settings

### Production Security Configuration

```python
# HTTPS/SSL
SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG

# Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Cookies
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]
```

See [Security Configuration Guide](../guides/security-configuration.md) for details.

---

## Authentication Settings

### Password Validators

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### Login/Logout URLs

```python
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/login/'
```

---

## Custom Application Settings

### KPI App Settings

Add custom settings for KPI calculations:

```python
# KPI Configuration
KPI_DEFAULT_MIN_THRESHOLD = 0.4
KPI_DEFAULT_MAX_THRESHOLD = 1.4
KPI_DEFAULT_WEIGHT = 0.25
KPI_RESULTS_PER_PAGE = 20
```

Usage in views:
```python
from django.conf import settings

min_threshold = settings.KPI_DEFAULT_MIN_THRESHOLD
```

---

## Performance Settings

### Caching (Optional)

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

### Database Connection Pooling

```python
DATABASES = {
    'default': {
        # ... other settings ...
        'CONN_MAX_AGE': 600,  # 10 minutes
    }
}
```

---

## Complete Example Configuration

### settings.py (Production-Ready)

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Application
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'slick_reporting',
    'kpi_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alkana_kpi.urls'
WSGI_APPLICATION = 'alkana_kpi.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'alkana_kpi'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 600,
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Bangkok')
USE_I18N = True
USE_TZ = True

# Security (Production only)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000

# Import/Export
IMPORT_EXPORT_USE_TRANSACTIONS = True
```

---

**Last Updated**: December 30, 2025

For security-specific configuration, see [Security Configuration Guide](../guides/security-configuration.md).
