# Alkana KPI System Documentation

Complete documentation for the Alkana KPI Management System.

## 📚 Documentation Overview

This documentation provides comprehensive guides for installing, configuring, deploying, and using the Alkana KPI tracking system.

## 🚀 Quick Links

### Getting Started
- **[README](../README.md)** - Project overview and quick start
- **[Installation Guide](guides/installation-guide.md)** - Set up development environment
- **[User Manual](guides/user-manual.md)** - End-user guide

### For Developers
- **[Data Model](guides/data-model.md)** - Database schema and relationships
- **[KPI Calculation Logic](guides/kpi-calculation-logic.md)** - How scores are calculated
- **[API Endpoints](api/api-endpoints.md)** - URL patterns and views
- **[Configuration Reference](guides/configuration-reference.md)** - Settings documentation

### For Administrators
- **[Admin Guide](guides/admin-guide.md)** - Django admin operations
- **[Permission Matrix](guides/permission-matrix.md)** - Access control system
- **[Import/Export Guide](guides/import-export-guide.md)** - Bulk data management

### For DevOps
- **[Deployment Guide](guides/deployment-guide.md)** - Production deployment (IIS/Linux)
- **[Security Configuration](guides/security-configuration.md)** - Security hardening
- **[Troubleshooting](guides/troubleshooting.md)** - Common issues and solutions

## 📖 Documentation Structure

```
docs/
├── README.md                          # This file
├── guides/
│   ├── installation-guide.md          # Development setup
│   ├── deployment-guide.md            # Production deployment
│   ├── data-model.md                  # Database documentation
│   ├── kpi-calculation-logic.md       # Calculation formulas
│   ├── admin-guide.md                 # Admin interface guide
│   ├── permission-matrix.md           # Access control
│   ├── import-export-guide.md         # Excel import/export
│   ├── security-configuration.md      # Security hardening
│   ├── configuration-reference.md     # Settings reference
│   ├── user-manual.md                 # End-user guide
│   └── troubleshooting.md             # Problem solving
├── api/
│   └── api-endpoints.md               # API documentation
└── assets/
    └── (diagrams and images)
```

## 📋 Documentation by Role

### I'm a Developer

**Setting up locally:**
1. Read [Installation Guide](guides/installation-guide.md)
2. Review [Data Model](guides/data-model.md)
3. Study [KPI Calculation Logic](guides/kpi-calculation-logic.md)
4. Check [API Endpoints](api/api-endpoints.md)

**Key files to understand:**
- `kpi_app/models.py` - Data models
- `kpi_app/admin.py` - Admin configuration
- `kpi_app/views.py` - View logic
- `alkana_kpi/settings.py` - Configuration

---

### I'm an Administrator

**Managing the system:**
1. Start with [Admin Guide](guides/admin-guide.md)
2. Understand [Permission Matrix](guides/permission-matrix.md)
3. Learn [Import/Export Guide](guides/import-export-guide.md)

**Common tasks:**
- Adding employees: [Admin Guide - Managing Employees](guides/admin-guide.md#managing-employees)
- Bulk data import: [Import/Export Guide](guides/import-export-guide.md)
- Managing users: [Admin Guide - User Roles](guides/admin-guide.md#user-roles-and-permissions)

---

### I'm a DevOps Engineer

**Deploying to production:**
1. Follow [Deployment Guide](guides/deployment-guide.md)
2. Apply [Security Configuration](guides/security-configuration.md)
3. Reference [Configuration Reference](guides/configuration-reference.md)
4. Keep [Troubleshooting Guide](guides/troubleshooting.md) handy

**Critical steps:**
- ⚠️ Change SECRET_KEY
- ⚠️ Set DEBUG=False
- ⚠️ Configure ALLOWED_HOSTS
- ⚠️ Set up SSL/HTTPS
- ⚠️ Configure database backups

---

### I'm an End User

**Using the system:**
1. Read [User Manual](guides/user-manual.md)
2. Check [Troubleshooting Guide](guides/troubleshooting.md) for issues

**Common questions:**
- How to log in: [User Manual - Logging In](guides/user-manual.md#logging-in)
- Viewing KPIs: [User Manual - Viewing Your KPIs](guides/user-manual.md#viewing-your-kpis)
- Understanding scores: [User Manual - Understanding Scores](guides/user-manual.md#understanding-your-kpi-scores)
- FAQ: [User Manual - FAQ](guides/user-manual.md#frequently-asked-questions)

---

## 🔍 Find What You Need

### Installation & Setup
- Local development setup → [Installation Guide](guides/installation-guide.md)
- Production deployment → [Deployment Guide](guides/deployment-guide.md)
- Configuration options → [Configuration Reference](guides/configuration-reference.md)

### Understanding the System
- How data is structured → [Data Model](guides/data-model.md)
- How scores are calculated → [KPI Calculation Logic](guides/kpi-calculation-logic.md)
- Who can access what → [Permission Matrix](guides/permission-matrix.md)

### Using the System
- Admin operations → [Admin Guide](guides/admin-guide.md)
- End-user operations → [User Manual](guides/user-manual.md)
- Bulk data operations → [Import/Export Guide](guides/import-export-guide.md)

### Advanced Topics
- URL routing and views → [API Endpoints](api/api-endpoints.md)
- Security hardening → [Security Configuration](guides/security-configuration.md)
- Troubleshooting → [Troubleshooting Guide](guides/troubleshooting.md)

---

## 🎯 Common Use Cases

### "I want to install the system locally"
→ [Installation Guide](guides/installation-guide.md)

### "I want to deploy to Windows Server with IIS"
→ [Deployment Guide - Windows/IIS](guides/deployment-guide.md#windows-server--iis-deployment)

### "I want to deploy to Linux with Nginx"
→ [Deployment Guide - Linux](guides/deployment-guide.md#linux-deployment)

### "I want to understand how KPI scores are calculated"
→ [KPI Calculation Logic](guides/kpi-calculation-logic.md)

### "I want to import 100 employee records from Excel"
→ [Import/Export Guide - Bulk Add Employees](guides/import-export-guide.md#scenario-1-bulk-add-new-employees)

### "I want to know what permissions each user level has"
→ [Permission Matrix](guides/permission-matrix.md)

### "I'm getting an error and need help"
→ [Troubleshooting Guide](guides/troubleshooting.md)

### "I want to secure the system for production"
→ [Security Configuration](guides/security-configuration.md)

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────┐
│              Alkana KPI System                      │
│  ─────────────────────────────────────────────────  │
│                                                      │
│  ┌──────────────┐    ┌──────────────┐              │
│  │  Web Server  │────│   FastCGI/   │              │
│  │  (IIS/Nginx) │    │   Gunicorn   │              │
│  └──────────────┘    └──────────────┘              │
│                             │                        │
│                      ┌──────▼──────┐                │
│                      │   Django    │                │
│                      │   5.2.1     │                │
│                      └──────┬──────┘                │
│                             │                        │
│          ┌──────────────────┼──────────────────┐    │
│          │                  │                  │    │
│    ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼────┐
│    │   Admin   │     │   Views   │     │  Models  │
│    │ Interface │     │ (Reports) │     │  (8 DB)  │
│    └───────────┘     └───────────┘     └─────┬────┘
│                                                │    │
│                                         ┌──────▼────┐
│                                         │  MySQL    │
│                                         │ Database  │
│                                         └───────────┘
│                                                      │
└─────────────────────────────────────────────────────┘

Features:
• Multi-level access control (Levels 0-4)
• KPI calculation engine (3 types)
• Excel import/export
• Semester-based tracking
• Department hierarchy
```

---

## 🔑 Key Concepts

### KPI Types
1. **Type 1 (Bigger Better)**: Higher achievement = higher score (e.g., revenue)
2. **Type 2 (Smaller Better)**: Lower achievement = higher score (e.g., costs)
3. **Type 3 (Mistake Counting)**: Zero mistakes = maximum score

### Permission Levels
- **Level 0**: Group Manager (cross-department)
- **Level 1**: Department Manager
- **Level 2**: Regular Employee (default)
- **Level 3/4**: Restricted/Read-only

### Time Periods
- **Year**: Calendar year (e.g., 2025)
- **Semester**: 1st SEM (Jan-Jun), 2nd SEM (Jul-Dec)
- **Month**: 5 months + final period

### Calculation Thresholds
- **Min** (default 0.4): Below this → 0 score
- **Max** (default 1.4): Above this → capped

---

## 📝 Documentation Standards

### Document Metadata
All documentation includes:
- Last updated date
- Related document links
- Version information (where applicable)

### Code Examples
Code examples are tested and include:
- Full context (imports, setup)
- Expected output
- Error handling

### Cross-References
Documents link to related content:
- Internal links use relative paths
- External links use full URLs
- All links are verified

---

## 🤝 Contributing to Documentation

### Reporting Issues
Found an error or unclear section?
1. Note the document and section
2. Describe the issue
3. Suggest improvement
4. Contact project maintainers

### Updating Documentation
When updating code, update related docs:
- Model changes → Update [Data Model](guides/data-model.md)
- Calculation changes → Update [KPI Calculation Logic](guides/kpi-calculation-logic.md)
- New features → Update [User Manual](guides/user-manual.md) and [Admin Guide](guides/admin-guide.md)
- Configuration changes → Update [Configuration Reference](guides/configuration-reference.md)

---

## 📞 Support

### Documentation Support
- Review relevant guide for your task
- Check [Troubleshooting Guide](guides/troubleshooting.md)
- Search within documents (Ctrl+F)

### Technical Support
- Email: [support email]
- Phone: [support phone]
- Hours: Monday-Friday, 8:00 AM - 5:00 PM

### Report Documentation Issues
- Missing information
- Outdated content
- Broken links
- Unclear explanations

---

## 📅 Version History

- **December 30, 2025**: Initial complete documentation suite created
  - 13 comprehensive guides covering all aspects
  - Installation, deployment, security, and user documentation
  - API reference and troubleshooting guides

---

**Last Updated**: December 30, 2025

**Documentation Version**: 1.0

**Application Version**: Django 5.2.1
