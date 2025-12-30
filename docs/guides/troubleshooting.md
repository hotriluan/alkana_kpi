# Troubleshooting Guide - Alkana KPI System

Common issues and solutions for the Alkana KPI Management System.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Login and Authentication](#login-and-authentication)
- [Database Issues](#database-issues)
- [Admin Interface Issues](#admin-interface-issues)
- [Import/Export Issues](#importexport-issues)
- [Calculation Issues](#calculation-issues)
- [Performance Issues](#performance-issues)
- [Deployment Issues](#deployment-issues)

## Installation Issues

### Python Package Installation Failures

**Issue**: `pip install -r requirements.txt` fails

**Common Causes & Solutions**:

**mysqlclient installation fails on Windows**:
```error
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solution 1**: Install Visual C++ Build Tools
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++"
3. Retry: `pip install mysqlclient`

**Solution 2**: Use alternative MySQL connector
```bash
pip install mysql-connector-python
```
Then update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',  # Changed
        # ... rest of config ...
    }
}
```

---

**wfastcgi installation fails**:

**Solution**: Install manually
```bash
python -m pip install --upgrade pip
pip install wfastcgi
wfastcgi-enable
```

---

### Virtual Environment Issues

**Issue**: `ModuleNotFoundError` despite installing packages

**Cause**: Virtual environment not activated or wrong environment

**Solution**:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Verify correct environment
which python  # Should show venv path
pip list  # Should show installed packages
```

**Issue**: Permission denied when creating venv

**Solution**:
```bash
# Windows (as Administrator)
python -m venv venv

# Linux
sudo python3 -m venv venv
sudo chown -R $USER:$USER venv
```

---

### Django Migration Errors

**Issue**: Migration conflicts or errors

**Error**:
```error
django.db.migrations.exceptions.InconsistentMigrationHistory
```

**Solution 1**: Fake migrations (⚠️ Use with caution)
```bash
python manage.py migrate --fake kpi_app zero
python manage.py migrate kpi_app
```

**Solution 2**: Reset database (⚠️ DELETES ALL DATA)
```bash
# Backup first!
python manage.py dumpdata > backup.json

# Drop and recreate database
mysql -u root -p
DROP DATABASE alkana_kpi;
CREATE DATABASE alkana_kpi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Rerun migrations
python manage.py migrate
```

---

## Login and Authentication

### Cannot Login

**Issue**: Valid credentials rejected

**Checklist**:
1. ☑ Username is correct (case-sensitive)
2. ☑ Password is correct (check caps lock)
3. ☑ User account exists in database
4. ☑ User is_active = True
5. ☑ Browser accepts cookies

**Debug Steps**:
```python
python manage.py shell

from django.contrib.auth.models import User

# Check if user exists
user = User.objects.get(username='john.doe')
print(f"Active: {user.is_active}")
print(f"Staff: {user.is_staff}")

# Reset password
user.set_password('newpassword123')
user.save()
```

---

### Account Locked After Failed Attempts

**Issue**: "Account locked due to excessive login attempts"

**Cause**: django-axes brute-force protection (if enabled)

**Solution**:
```python
python manage.py axes_reset
# Or reset specific user:
python manage.py axes_reset_username john.doe
```

---

### Session Expires Too Quickly

**Issue**: Logged out after short period of inactivity

**Cause**: SESSION_COOKIE_AGE too short

**Solution**: Update `settings.py`:
```python
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True  # Reset timer on each request
```

---

### CSRF Verification Failed

**Issue**: "CSRF verification failed. Request aborted."

**Common Causes**:

**1. Missing CSRF Token**:
```django
<!-- Ensure form has CSRF token -->
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

**2. Incorrect CSRF_TRUSTED_ORIGINS**:
```python
# settings.py
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]
```

**3. Cookies blocked by browser**:
- Check browser privacy settings
- Allow cookies for the site
- Clear browser cache/cookies

---

## Database Issues

### Cannot Connect to MySQL

**Error**:
```error
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```

**Solutions**:

**1. Check MySQL is running**:
```bash
# Windows
sc query MySQL80

# Linux
sudo systemctl status mysql

# Start if not running
sudo systemctl start mysql
```

**2. Verify credentials**:
```bash
mysql -u alkana_user -p alkana_kpi
# Enter password
```

**3. Check HOST setting**:
```python
# settings.py
DATABASES = {
    'default': {
        'HOST': 'localhost',  # Try '127.0.0.1' if 'localhost' fails
    }
}
```

**4. Check firewall**:
```bash
# Linux - Allow MySQL
sudo ufw allow 3306/tcp
```

---

### Database Access Denied

**Error**:
```error
OperationalError: (1045, "Access denied for user 'alkana_user'@'localhost'")
```

**Solutions**:

**1. Verify user exists and has permissions**:
```sql
mysql -u root -p

SELECT user, host FROM mysql.user WHERE user='alkana_user';
SHOW GRANTS FOR 'alkana_user'@'localhost';
```

**2. Reset user password**:
```sql
ALTER USER 'alkana_user'@'localhost' IDENTIFIED BY 'newpassword';
FLUSH PRIVILEGES;
```

**3. Grant permissions**:
```sql
GRANT ALL PRIVILEGES ON alkana_kpi.* TO 'alkana_user'@'localhost';
FLUSH PRIVILEGES;
```

---

### Character Encoding Issues

**Issue**: Special characters display as ��� or ?

**Solution**: Ensure UTF-8 everywhere
```sql
-- Database
ALTER DATABASE alkana_kpi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Tables
ALTER TABLE kpi_app_alk_employee CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

```python
# settings.py
DATABASES = {
    'default': {
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

---

## Admin Interface Issues

### Cannot Access Admin Interface

**Issue**: 404 error on /admin/

**Solution**: Check URLs are configured
```python
# alkana_kpi/urls.py
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
]
```

Run server and test:
```bash
python manage.py runserver
# Navigate to http://127.0.0.1:8000/admin/
```

---

### Fields Are Read-Only Unexpectedly

**Issue**: Cannot edit fields in admin

**Cause**: Permission level or KPI configuration

**Debug**:
```python
python manage.py shell

from kpi_app.models import alk_employee
from django.contrib.auth.models import User

user = User.objects.get(username='john.doe')
emp = alk_employee.objects.get(user_id=user)
print(f"Level: {emp.level}")  # Check permission level

# Check KPI flags
from kpi_app.models import alk_kpi
kpi = alk_kpi.objects.get(id=1)
print(f"from_sap: {kpi.from_sap}")
print(f"percentage_cal: {kpi.percentage_cal}")
```

**Solutions**:
- Level 2+ cannot edit `kpi` or `max` fields (expected)
- `from_sap=True` makes `achievement` read-only (expected)
- `percentage_cal=False` makes `target_input` read-only (expected)

See [Permission Matrix](permission-matrix.md) for details.

---

### Static Files Not Loading

**Issue**: Admin interface has no styling (plain HTML)

**Cause**: Static files not collected or not served

**Solution 1**: Collect static files
```bash
python manage.py collectstatic --noinput
```

**Solution 2**: Check STATIC_ROOT setting
```python
# settings.py
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**Solution 3**: For development, ensure DEBUG=True
```python
# settings.py
DEBUG = True  # Auto-serves static files in development
```

**Solution 4**: For production, configure web server to serve static files

---

## Import/Export Issues

### Import Fails with Validation Errors

**Issue**: Rows rejected during import

**Common Errors**:

**"Employee with emp_code 'XXX' does not exist"**:
- Solution: Ensure referenced employee exists or create employee first

**"Invalid choice for semester: 1st Sem"**:
- Solution: Use exact value: `1st SEM` (with space, uppercase)

**"Invalid value for kpi_type"**:
- Solution: Use integer values: `1`, `2`, or `3`

**"This field cannot be null"**:
- Solution: Fill all required fields (see [Import/Export Guide](import-export-guide.md))

**Debug Tips**:
1. Export existing records to get template
2. Compare your import file to exported format
3. Import small batches (10-20 rows) to isolate errors
4. Check error line numbers in preview

---

### Export Button Not Visible

**Issue**: Export button missing from admin

**Cause**: Not enough permissions or import-export not installed

**Solution 1**: Verify import-export installed
```bash
pip show django-import-export
# If not found:
pip install django-import-export
```

**Solution 2**: Check INSTALLED_APPS
```python
# settings.py
INSTALLED_APPS = [
    # ...
    'import_export',
    'kpi_app',
]
```

**Solution 3**: Check user permissions
- Superuser: Can import and export
- Others: Can export only

---

### Excel File Won't Open

**Issue**: Downloaded file corrupted or won't open

**Solutions**:
1. Try different browser
2. Clear browser cache
3. Re-export the file
4. Try opening with Google Sheets instead of Excel
5. Check file extension is `.xlsx`

---

## Calculation Issues

### Final Result is Zero

**Issue**: `final_result` shows 0 despite achievement

**Possible Causes**:

**1. Below minimum threshold**:
```python
# Example
achievement = 350,000
target_input = 1,000,000
ratio = 350,000 / 1,000,000 = 0.35  # 35%
min = 0.4  # 40%
→ 0.35 < 0.4 → Score = 0
```
**Solution**: Achieve at least 40% of target (or adjust min threshold)

**2. get_1_is_zero flag enabled**:
```python
if kpi.get_1_is_zero and achievement > 0:
    return 0  # Any achievement → 0 score
```
**Solution**: This is expected for zero-tolerance KPIs

**3. Missing data**:
```python
if target_input is None or achievement is None:
    return 0
```
**Solution**: Enter both target and achievement values

---

### Final Result Seems Wrong

**Issue**: Calculated score doesn't match expectations

**Debug Steps**:

```python
python manage.py shell

from kpi_app.models import alk_kpi_result

result = alk_kpi_result.objects.get(id=1)

# Check input values
print(f"Achievement: {result.achivement}")
print(f"Target Input: {result.target_input}")
print(f"Target Set: {result.target_set}")
print(f"Weight: {result.weigth}")
print(f"Min: {result.min}, Max: {result.max}")

# Check KPI configuration
print(f"KPI Type: {result.kpi.kpi_type}")
print(f"Percentage Cal: {result.kpi.percentage_cal}")
print(f"Get 1 is Zero: {result.kpi.get_1_is_zero}")

# Manually calculate
score = result.calculate_final_result()
print(f"Calculated Score: {score}")
print(f"Saved Final Result: {result.final_result}")
```

**Reference**: See [KPI Calculation Logic](kpi-calculation-logic.md) for formulas

---

### Target Input Won't Update

**Issue**: Cannot edit `target_input` field

**Cause**: KPI has `percentage_cal = False`

**Explanation**: This is expected behavior. When `percentage_cal = False`, the system auto-sets `target_input = target_set` on save.

**Solution**: If you need to edit target_input:
1. Change KPI's `percentage_cal` to `True`
2. Or edit `target_set` instead

---

## Performance Issues

### Slow Page Load

**Issue**: Admin pages take long to load

**Solutions**:

**1. Database query optimization**:
```python
# Use select_related for foreign keys
results = alk_kpi_result.objects.select_related('employee', 'kpi')

# Use prefetch_related for reverse relations
employees = alk_employee.objects.prefetch_related('alk_kpi_result_set')
```

**2. Add database indexes**:
```python
# models.py
class alk_kpi_result(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['year', 'semester']),
            models.Index(fields=['employee', 'year']),
        ]
```

**3. Enable caching**:
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

**4. Use pagination**:
Already implemented (20 results per page in home view)

---

### High Memory Usage

**Issue**: Server using excessive memory

**Solutions**:

**1. Limit query results**:
```python
# Instead of
results = alk_kpi_result.objects.all()  # Loads everything

# Use
results = alk_kpi_result.objects.filter(year=2025)  # Filter first
```

**2. Use iterator() for large datasets**:
```python
for result in alk_kpi_result.objects.iterator():
    # Process one at a time
```

**3. Close database connections**:
```python
# settings.py
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,  # Close after 10 minutes
    }
}
```

---

## Deployment Issues

### IIS Configuration Errors

**Issue**: 500 error on IIS deployment

**Solutions**:

**1. Check web.config**:
```xml
<!-- Verify Python path is correct -->
<add key="PYTHONPATH" value="C:\inetpub\wwwroot\alkana_kpi" />
<add key="WSGI_HANDLER" value="alkana_kpi.wsgi.application" />
```

**2. Check IIS permissions**:
```powershell
icacls "C:\inetpub\wwwroot\alkana_kpi" /grant "IIS_IUSRS:(OI)(CI)F" /T
```

**3. Enable detailed errors**:
```xml
<system.webServer>
    <httpErrors errorMode="Detailed" />
</system.webServer>
```

**4. Check logs**:
- `C:\inetpub\logs\alkana_kpi.log`
- Windows Event Viewer

---

### Static Files Not Served on Production

**Issue**: CSS/JS missing on production

**Solution**:

**For IIS**: Create `staticfiles/web.config`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <clear />
      <add name="StaticFile" path="*" verb="*" 
           modules="StaticFileModule" 
           resourceType="File" requireAccess="Read" />
    </handlers>
  </system.webServer>
</configuration>
```

**For Nginx**: Configure static file serving:
```nginx
location /static/ {
    alias /var/www/alkana_kpi/staticfiles/;
    expires 30d;
}
```

---

### SSL Certificate Errors

**Issue**: HTTPS not working or certificate errors

**Solutions**:

**1. Install valid SSL certificate**:
- Obtain from Let's Encrypt, commercial CA, or IT department
- Install in IIS or web server

**2. Configure HTTPS redirect**:
```python
# settings.py
SECURE_SSL_REDIRECT = True  # Force HTTPS
```

**3. Update CSRF_TRUSTED_ORIGINS**:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',  # Use https://
]
```

---

## Getting Help

### Enable Debug Mode (Development Only)

⚠️ **NEVER use DEBUG=True in production!**

```python
# settings.py (development only)
DEBUG = True
```

This shows detailed error pages with:
- Full stack trace
- Variable values
- SQL queries

---

### Check Django System

```bash
python manage.py check --deploy
```

Shows security warnings and configuration issues.

---

### View Django Logs

```bash
# Development server console output
python manage.py runserver

# Production logs
# Linux: /var/www/alkana_kpi/logs/django.log
# Windows: C:\inetpub\logs\alkana_kpi.log
```

---

### Contact Support

If issue persists:
1. Gather error messages and logs
2. Document steps to reproduce
3. Note your environment (OS, Python version, etc.)
4. Contact IT support or project administrator

---

**Last Updated**: December 30, 2025

For additional help, see:
- [Installation Guide](installation-guide.md)
- [Deployment Guide](deployment-guide.md)
- [Admin Guide](admin-guide.md)
- [Permission Matrix](permission-matrix.md)
