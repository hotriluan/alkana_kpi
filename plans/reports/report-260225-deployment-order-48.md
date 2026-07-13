# Deployment Order #48 — Reuse Django Admin Login UI
**Date:** 2026-02-25  
**Commit:** `cb9d33a`  
**Branch:** main → pushed to `origin/main`  
**Status:** ✅ Complete

---

## Objective

Style the login page to look exactly like the default Django Admin login using its built-in template (`admin/login.html`), while keeping the role-based redirection logic from DO #47. Customize branding text to "Alkana KPI".

---

## Files Modified

| File | Action |
|------|--------|
| `kpi_app/views/portal_views.py` | Modified — added `CustomRoleBasedLoginView` CBV |
| `alkana_kpi/urls.py` | Modified — routed both login URLs to new CBV |

---

## Task 1: New Class-Based View (`portal_views.py`)

### Added imports
```python
from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url
```

### New class
```python
class CustomRoleBasedLoginView(LoginView):
    """Uses Django admin login UI with Alkana KPI branding and role-based redirect."""
    template_name = 'admin/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_header'] = 'Alkana KPI System'   # Big header text
        context['site_title'] = 'Alkana KPI'           # Browser tab title
        context['title'] = 'Please Log In'             # Form title
        return context

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return resolve_url('admin:index')           # Superuser → /admin/
        return resolve_url('portal_dashboard')          # All others → /portal/
```

**Design decision:** Used CBV subclass instead of FBV patch — cleaner separation, no duplication with existing `user_login` FBV (KISS + DRY).

---

## Task 2: URL Routing (`alkana_kpi/urls.py`)

### Before
```python
from kpi_app import views

path('admin/login/',    views.user_login),
path('accounts/login/', views.user_login, name='login'),
```

### After
```python
from kpi_app import views
from kpi_app.views.portal_views import CustomRoleBasedLoginView

path('admin/login/',    CustomRoleBasedLoginView.as_view()),
path('accounts/login/', CustomRoleBasedLoginView.as_view(), name='login'),
```

Both login entry points now share the same branded view — DRY.

---

## Result

| URL | UI Rendered | Header Text |
|-----|-------------|-------------|
| `/accounts/login/` | Django Admin login box | **Alkana KPI System** |
| `/admin/login/` | Django Admin login box | **Alkana KPI System** |
| Browser tab | — | **Alkana KPI** |

---

## Redirect Flow (Preserved from DO #47)

```
Login success
    ├── is_superuser = True  →  /admin/
    └── is_superuser = False →  /portal/
```

---

## Verification

| Check | Result |
|-------|--------|
| Django system check | ✅ 0 issues |
| CBV renders admin/login.html | ✅ |
| site_header = "Alkana KPI System" | ✅ |
| Superuser redirects to /admin/ | ✅ |
| Manager/Employee redirects to /portal/ | ✅ |

---

## Compliance

| Principle | Status |
|-----------|--------|
| YAGNI | ✅ No extra features; only branding + routing |
| KISS | ✅ Reused built-in template, minimal code |
| DRY | ✅ Single CBV serves both `/accounts/login/` and `/admin/login/` |

---

*Report: 2026-02-25 | Deployment Order #48*
