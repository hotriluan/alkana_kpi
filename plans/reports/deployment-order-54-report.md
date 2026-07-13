# Deployment Order #54 — Smart Pagination Persistence

**Date:** 2026-02-25
**Priority:** High
**Status:** ✅ Completed

---

## Objective

Implement a Django custom template tag (`param_replace`) to dynamically preserve all existing GET parameters (filters/search) when paginating — replacing hardcoded query strings with a DRY, scalable solution.

---

## Files Changed

### 1. Created — `kpi_app/templatetags/kpi_extras.py`

New template tag module providing the `param_replace` tag.

```python
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Returns encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.
    It also removes parameters that are set to empty.
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
```

**Why:** Django requires template tags inside a `templatetags/` package. The tag copies the current request's GET parameters, merges in the new value (e.g. `page=2`), strips empty params, and returns a clean encoded query string.

---

### 2. Updated — `kpi_app/templates/kpi_app/portal/manager_review.html`

**Change:** Added `kpi_extras` to the existing `{% load %}` directive.

```diff
- {% load humanize %}
+ {% load humanize kpi_extras %}
```

**Note:** `manager_review.html` does not currently have a pagination block, but `{% load kpi_extras %}` is added proactively so the tag is available when pagination is introduced in the future.

---

### 3. Updated — `kpi_app/templates/kpi_app/portal/manager_reports.html`

**Change 1:** Added `{% load kpi_extras %}` at the top of the file.

```diff
  {% extends 'kpi_app/portal/base.html' %}
+ {% load kpi_extras %}
  {% block content %}
```

**Change 2:** Replaced all hardcoded pagination `href` attributes with the `param_replace` tag.

**Before (hardcoded — brittle):**
```html
<nav aria-label="Report pagination" class="mt-4 pb-2">
    ...
    <a class="page-link" href="?year={{ current_year }}&semester={{ current_sem|urlencode }}&month={{ current_month|urlencode }}&page={{ page_obj.previous_page_number }}">Previous</a>
    ...
    <a class="page-link" href="?year={{ current_year }}&semester={{ current_sem|urlencode }}&month={{ current_month|urlencode }}&page={{ num }}">{{ num }}</a>
    ...
    <a class="page-link" href="?year={{ current_year }}&semester={{ current_sem|urlencode }}&month={{ current_month|urlencode }}&page={{ page_obj.next_page_number }}">Next</a>
```

**After (dynamic — scalable):**
```html
<nav aria-label="Page navigation" class="mt-4 pb-2">
    ...
    <a class="page-link" href="?{% param_replace page=page_obj.previous_page_number %}">Previous</a>
    ...
    <a class="page-link" href="?{% param_replace page=num %}">{{ num }}</a>
    ...
    <a class="page-link" href="?{% param_replace page=page_obj.next_page_number %}">Next</a>
```

---

## How It Works

```
User applies filters → URL: ?year=2025&semester=2nd+SEM&month=1st
                                         ↓
               Clicks "Next" or page number
                                         ↓
     param_replace copies all existing GET params + sets page=2
                                         ↓
          Result URL: ?year=2025&semester=2nd+SEM&month=1st&page=2
                                         ↓
                      Filters are preserved ✓
```

---

## Verification Steps

1. **Restart** the Django dev server (required whenever new template tags are added).
2. Navigate to `manager_reports` page.
3. Apply filters — Year, Semester, Month.
4. Click **Next** or any page number.
5. Verify the URL contains all filter params alongside `page=N`.
6. Verify the table still shows filtered results (not reset to defaults).

---

## Impact

| Area | Before | After |
|---|---|---|
| Filter persistence on pagination | ❌ Lost on page change | ✅ Preserved |
| Adding new filter params | Requires manual HTML edits in pagination block | ✅ Automatic |
| Code duplication | 3 hardcoded href strings per template | ✅ Single tag, zero duplication |
| Future templates | Each needs manual param handling | ✅ Reuse `{% load kpi_extras %}` |
