# Alkana KPI Management System

A comprehensive Django-based Key Performance Indicator (KPI) tracking and management system designed for organizational performance management across departments, employees, and time periods.

## 🎯 Overview

Alkana KPI enables organizations to:
- **Track KPIs** across semesters and months with automated scoring
- **Manage hierarchies** with departments, groups, and employee levels (0-4)
- **Calculate performance** using configurable min/max thresholds and weights
- **Control access** with role-based permissions based on employee levels
- **Import/Export data** via Excel for bulk operations
- **Generate reports** with filtering, pagination, and Excel export

## 📋 Features

### Core Functionality
- **KPI Result Tracking**: Track employee KPIs across 1st/2nd semesters with 5 months + final period
- **Complex Calculation Engine**: Support for 3 KPI types:
  - Type 1: Bigger is better
  - Type 2: Smaller is better  
  - Type 3: Mistake counting (inverted)
- **Department Management**: Hierarchical organization with departments and groups
- **Multi-level Access Control**: 5 permission levels (0-4) controlling visibility and editing
- **Excel Integration**: Import/export KPI data and results via XLSX files
- **Reporting Dashboard**: Filter by semester, month, department with Excel export

### Admin Features
- Comprehensive Django Admin interface with custom list displays
- Dynamic field permissions based on user level
- Inline editing for related records
- Horizontal scrolling for wide tables
- Import/Export integration with validation

### User Features
- Employee self-service profile updates
- Password change functionality
- View assigned KPIs and results
- Limited editing based on permission level

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+ or MySQL 8.0+
- pip and virtualenv

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd alkana_kpi
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**

Edit `alkana_kpi/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alkana_kpi',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/admin to access the admin interface.

## 📚 Documentation

Comprehensive documentation is available in the `/docs` directory:

### Getting Started
- [Installation Guide](docs/guides/installation-guide.md) - Detailed setup instructions
- [Deployment Guide](docs/guides/deployment-guide.md) - Production deployment on IIS/Windows
- [Configuration Reference](docs/guides/configuration-reference.md) - Settings and environment variables

### Architecture & Design
- [Data Model](docs/guides/data-model.md) - Database schema and model relationships
- [KPI Calculation Logic](docs/guides/kpi-calculation-logic.md) - How KPI scores are computed
- [Permission Matrix](docs/guides/permission-matrix.md) - Access control by user level

### User Guides
- [Admin Guide](docs/guides/admin-guide.md) - Django admin interface operations
- [User Manual](docs/guides/user-manual.md) - End-user instructions
- [Import/Export Guide](docs/guides/import-export-guide.md) - Excel file format specifications

### Developer Resources
- [API Endpoints](docs/api/api-endpoints.md) - URL patterns and view documentation
- [Security Configuration](docs/guides/security-configuration.md) - Production security checklist
- [Troubleshooting](docs/guides/troubleshooting.md) - Common issues and solutions

## 🏗️ Technology Stack

- **Framework**: Django 5.2.1
- **Database**: MySQL (mysqlclient 2.2.7)
- **Import/Export**: django-import-export 4.3.3, openpyxl 3.1.5
- **Reporting**: django-slick-reporting 0.11.0, reportlab 4.4.2
- **Deployment**: IIS with FastCGI (wfastcgi 3.0.0) on Windows Server

## 📊 Database Schema

The application uses 8 core models:

1. **Alk_Dept** - Departments (Finance, HR, Plant Management, etc.)
2. **Alk_Dept_Group** - Department sub-groups
3. **Alk_Job_Title** - Employee job positions
4. **Alk_Objective** - Department objectives
5. **Alk_Perspective** - KPI perspectives (Financial, Customer, etc.)
6. **Alk_Employee** - Employee information with user linkage
7. **Alk_KPI** - KPI definitions with calculation rules
8. **Alk_KPI_Result** - Actual KPI measurements and scores

See [Data Model Documentation](docs/guides/data-model.md) for detailed relationships and field descriptions.

## 🔐 Security Notes

**⚠️ IMPORTANT**: Before deploying to production:

1. **Change SECRET_KEY** in `settings.py` to a unique, random value
2. **Set DEBUG = False** in production
3. **Configure ALLOWED_HOSTS** with your domain names
4. **Use environment variables** for sensitive settings
5. **Enable HTTPS** and configure SSL certificates
6. **Review database credentials** and use strong passwords

See [Security Configuration Guide](docs/guides/security-configuration.md) for complete checklist.

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test kpi_app
```

## 📝 License

[Add your license information here]

## 👥 Contributors

[Add contributor information here]

## 📧 Support

For issues and questions:
- Check [Troubleshooting Guide](docs/guides/troubleshooting.md)
- Review existing issues in the issue tracker
- Contact the development team

## 🔄 Version History

- **Current**: Django 5.2.1 with MySQL backend
- See migration files in `kpi_app/migrations/` for database changes

---

**Last Updated**: December 30, 2025
