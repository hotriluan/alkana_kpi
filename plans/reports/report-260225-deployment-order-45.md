# Deployment Order #45 — Dynamic Dropdown Filters
**Date:** 2026-02-25  
**Commit:** `cdf2ec0`  
**Branch:** main → pushed to `origin/main`  
**Status:** ✅ Complete

---

## Objective

Replace static `<input type="text">` filter fields in `manager_reports` with dynamic `<select>` dropdowns populated from distinct values in the database.

---

## Files Modified

| File | Action |
|------|--------|
| `kpi_app/views/portal_views.py` | Modified — dynamic DB queries + updated context |
| `kpi_app/templates/kpi_app/portal/manager_reports.html` | Modified — text inputs → select dropdowns |

---

## Task 1: View Changes (`portal_views.py`)

### Removed
- Hardcoded `ALLOWED_SEMESTERS` / `ALLOWED_MONTHS` static lists
- Hardcoded default values (`'2nd SEM'`, `'1st'`, `str(datetime.now().year)`)

### Added
```python
# Distinct options from DB
available_years  = alk_kpi_result.objects.exclude(year__isnull=True)\
    .values_list('year', flat=True).distinct().order_by('-year')

available_sems   = alk_kpi_result.objects.exclude(semester__isnull=True)\
    .exclude(semester__exact='').values_list('semester', flat=True).distinct().order_by('semester')

available_months = alk_kpi_result.objects.exclude(month__isnull=True)\
    .exclude(month__exact='').values_list('month', flat=True).distinct().order_by('month')

# Dynamic defaults from first DB value
default_year  = str(available_years[0])  if available_years  else str(datetime.now().year)
default_sem   = available_sems[0]        if available_sems   else '2nd SEM'
default_month = available_months[0]      if available_months else '1st'
```

### Updated context
```python
context = {
    'current_year': str(current_year),   # force string for template comparison
    'current_sem': current_sem,
    'current_month': current_month,
    'available_years': available_years,
    'available_sems': available_sems,
    'available_months': available_months,
    'ranking_data': processed_ranking,
}
```

---

## Task 2: Template Changes (`manager_reports.html`)

### Before
```html
<input type="text" name="year"     value="{{ current_year }}" class="form-control" style="width: 100px;">
<input type="text" name="semester" value="{{ current_sem }}"  class="form-control" style="width: 120px;">
<input type="text" name="month"    value="{{ current_month }}" class="form-control" style="width: 100px;">
<button type="submit" class="btn btn-primary">Filter</button>
```

### After
```html
<select name="year" class="form-select fw-bold text-primary" style="width: auto;">
    {% for y in available_years %}
        <option value="{{ y }}" {% if y|stringformat:"s" == current_year %}selected{% endif %}>
            {{ y }}
        </option>
    {% endfor %}
</select>

<select name="semester" class="form-select fw-bold text-primary" style="width: auto;">
    {% for s in available_sems %}
        <option value="{{ s }}" {% if s == current_sem %}selected{% endif %}>{{ s }}</option>
    {% endfor %}
</select>

<select name="month" class="form-select fw-bold text-primary" style="width: auto;">
    {% for m in available_months %}
        <option value="{{ m }}" {% if m == current_month %}selected{% endif %}>{{ m }}</option>
    {% endfor %}
</select>

<button type="submit" class="btn btn-primary px-4 shadow-sm">
    <i class="bi bi-funnel-fill me-1"></i> Filter
</button>
```

**Note:** Year uses `|stringformat:"s"` filter for int→string comparison since DB returns integer, context passes string.

---

## Verification

| Check | Result |
|-------|--------|
| Django system check | ✅ 0 issues |
| Dropdowns populated from DB | ✅ Real data, no hardcoded options |
| Selected state preserved on submit | ✅ Via template `{% if %}` comparison |
| Empty DB fallback | ✅ Graceful defaults if no data |

---

## Compliance

| Principle | Status |
|-----------|--------|
| YAGNI | ✅ No extra features added |
| KISS | ✅ Simple queryset + template loop |
| DRY | ✅ Single source of truth (DB) for filter options |

---

*Report: 2026-02-25 | Deployment Order #45*
