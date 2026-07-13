# Installation Guide - Alkana KPI System

This guide covers setting up the Alkana KPI Management System for local development and testing.

## Table of Contents
- [Prerequisites](#prerequisites)
- [System Requirements](#system-requirements)
- [Installation Steps](#installation-steps)
- [Database Setup](#database-setup)
- [Initial Configuration](#initial-configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software
- **Python 3.8 or higher** (tested with Python 3.10+)
- **MySQL 5.7+ or MySQL 8.0+**
- **pip** (Python package manager)
- **virtualenv** or **venv** (for virtual environments)
- **Git** (for cloning repository)

### Optional Tools
- **MySQL Workbench** - GUI for database management
- **VS Code** or **PyCharm** - IDE for development
- **Postman** - API testing

## System Requirements

### Windows
- Windows 10/11 or Windows Server 2016+
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space (more for data storage)

### Linux
- Ubuntu 20.04+ / Debian 10+ / CentOS 8+
- 4GB RAM minimum
- 500MB free disk space

### macOS
- macOS 10.14+ (Mojave or later)
- 4GB RAM minimum
- 500MB free disk space

## Installation Steps

### 1. Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd alkana_kpi
```

### 2. Create Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**Linux/macOS:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` prefix in your command prompt.

### 3. Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Key packages installed:**
- Django 5.2.1
- mysqlclient 2.2.7
- django-import-export 4.3.3
- django-slick-reporting 0.11.0
- openpyxl 3.1.5
- reportlab 4.4.2

### 4. Install MySQL (if not already installed)

**Windows:**
1. Download MySQL Installer from https://dev.mysql.com/downloads/installer/
2. Run installer and choose "Developer Default"
3. Set root password during installation
4. Complete installation wizard

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mysql-server mysql-client
sudo mysql_secure_installation
```

**macOS (using Homebrew):**
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

## Database Setup

### 1. Create Database

Log into MySQL as root:
```bash
mysql -u root -p
```

Create database and user:
```sql
-- Create database
CREATE DATABASE alkana_kpi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (change password)
CREATE USER 'alkana_user'@'localhost' IDENTIFIED BY 'strong_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON alkana_kpi.* TO 'alkana_user'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

### 2. Test Database Connection

```bash
mysql -u alkana_user -p alkana_kpi
```

If successful, you'll see the MySQL prompt. Type `EXIT;` to quit.

## Initial Configuration

### 1. Configure Database Settings

Edit `alkana_kpi/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alkana_kpi',
        'USER': 'alkana_user',
        'PASSWORD': 'strong_password_here',  # Change this!
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### 2. Configure Secret Key (Development)

For development, you can use the existing secret key, but for production, generate a new one:

```python
# In settings.py
import secrets

# Generate new secret key
SECRET_KEY = secrets.token_urlsafe(50)
```

### 3. Set Debug Mode

For development:
```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

**⚠️ WARNING**: Never set `DEBUG = True` in production!

### 4. Run Database Migrations

```bash
# Check for migration issues
python manage.py check

# Show pending migrations
python manage.py showmigrations

# Run migrations
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, kpi_app, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying kpi_app.0027_alter_alk_dept_group... OK
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

Enter the requested information:
- Username: `admin` (or your preferred username)
- Email: your email address
- Password: strong password (won't be visible while typing)

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This copies all static files to `staticfiles/` directory.

## Verification

### 1. Run Development Server

```bash
python manage.py runserver
```

Expected output:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 30, 2025 - 10:00:00
Django version 5.2.1, using settings 'alkana_kpi.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 2. Access Admin Interface

Open browser and navigate to:
```
http://127.0.0.1:8000/admin
```

Log in with your superuser credentials.

### 3. Verify Models

In the admin interface, you should see:
- **KPI_APP**
  - Alk Depts
  - Alk Dept Groups
  - Alk Employees
  - Alk Job Titles
  - Alk KPIs
  - Alk KPI Results
  - Alk Objectives
  - Alk Perspectives

### 4. Test Database Connection

```bash
python manage.py dbshell
```

This should open a MySQL prompt connected to your database. Type `EXIT;` to quit.

## Loading Sample Data (Optional)

### Option 1: Using Django Admin
1. Navigate to each model in admin interface
2. Click "Import" button
3. Upload Excel files with sample data

### Option 2: Using Django Shell
```bash
python manage.py shell
```

```python
from kpi_app.models import Alk_Dept, Alk_Perspective

# Create sample department
dept = Alk_Dept.objects.create(
    dept_name='Finance',
    dept_abbrev='FIN',
    dept_group='Finance - 410'
)

# Create sample perspective
perspective = Alk_Perspective.objects.create(
    perspective_name='Financial',
    perspective_abbrev='FIN'
)

print(f"Created department: {dept}")
print(f"Created perspective: {perspective}")
```

Type `exit()` to leave the shell.

## Troubleshooting

### Error: "mysqlclient not found"

**Windows Solution:**
```bash
pip install mysqlclient
# If fails, install Visual C++ Build Tools
# Then try: pip install mysqlclient
```

Alternative for Windows:
```bash
pip install mysql-connector-python
# Then update ENGINE in settings.py to 'mysql.connector.django'
```

### Error: "Access denied for user"

Check database credentials in `settings.py` match MySQL user:
```bash
mysql -u alkana_user -p
# Enter password to verify
```

### Error: "Can't connect to MySQL server"

Ensure MySQL is running:

**Windows:**
```bash
# Check if MySQL service is running
sc query MySQL80  # or MySQL57
```

**Linux:**
```bash
sudo systemctl status mysql
sudo systemctl start mysql
```

**macOS:**
```bash
brew services list
brew services start mysql
```

### Port 8000 Already in Use

Use a different port:
```bash
python manage.py runserver 8080
```

### Migration Errors

Reset migrations (⚠️ **CAUTION**: Deletes all data):
```bash
# Drop and recreate database
mysql -u root -p
DROP DATABASE alkana_kpi;
CREATE DATABASE alkana_kpi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Delete migration files (keep __init__.py)
# Then run migrations again
python manage.py migrate
```

### Import Errors

Ensure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Reinstall requirements:
```bash
pip install -r requirements.txt --force-reinstall
```

## Next Steps

After successful installation:

1. **Review [Configuration Reference](configuration-reference.md)** for advanced settings
2. **Read [Admin Guide](admin-guide.md)** to learn the admin interface
3. **Check [Data Model](data-model.md)** to understand the database structure
4. **See [Import/Export Guide](import-export-guide.md)** for bulk data operations

For production deployment, see [Deployment Guide](deployment-guide.md).

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- MySQL Documentation: https://dev.mysql.com/doc/
- django-import-export: https://django-import-export.readthedocs.io/

---

**Last Updated**: December 30, 2025
