# KPI Calculation Logic - Alkana KPI System

This document provides a comprehensive explanation of how KPI scores are calculated in the `Alk_KPI_Result` model.

## Table of Contents
- [Overview](#overview)
- [Calculation Method](#calculation-method)
- [Step-by-Step Algorithm](#step-by-step-algorithm)
- [Calculation Examples](#calculation-examples)
- [Edge Cases](#edge-cases)
- [Testing Calculations](#testing-calculations)

## Overview

The KPI calculation engine in `Alk_KPI_Result.calculate_final_result()` implements a sophisticated scoring system that:

1. Supports **3 different calculation types** (bigger better, smaller better, mistake counting)
2. Applies **configurable thresholds** (min/max) to cap scores
3. Uses **weighted scoring** to combine multiple KPIs
4. Handles **percentage-based** and **absolute value** calculations
5. Implements **special rules** (get_1_is_zero flag)

**Location**: [kpi_app/models.py](../../kpi_app/models.py#L134-L174) - `calculate_final_result()` method

## Calculation Method

### Input Variables

| Variable | Source | Type | Description |
|----------|--------|------|-------------|
| `achievement` | `self.achivement` | Decimal | Actual achieved value |
| `target_input` | `self.target_input` | Decimal | Target value (absolute) |
| `target_set` | `self.target_set` | Decimal | Target ratio/percentage |
| `weight` | `self.weigth` | Decimal | KPI weight (importance) |
| `min` | `self.min` | Decimal | Minimum threshold (default 0.4) |
| `max` | `self.max` | Decimal | Maximum threshold (default 1.4) |
| `kpi_type` | `self.kpi.kpi_type` | Integer | Calculation type (1, 2, or 3) |
| `percentage_cal` | `self.kpi.percentage_cal` | Boolean | Use percentage calculation mode |
| `get_1_is_zero` | `self.kpi.get_1_is_zero` | Boolean | Special rule: achievement>0 → 0 |

### Output

- **`final_result`**: Decimal(20, 3) - The weighted KPI score

## Step-by-Step Algorithm

### Phase 1: Null Check

```python
if self.target_input is None or self.achivement is None:
    return 0
```

**Rule**: If either target or achievement is missing, return score of 0.

---

### Phase 2: Special Rule - get_1_is_zero

```python
if get_1_is_zero:
    if achivement > 0:
        return 0
    else:
        return weigth * max_val
```

**Purpose**: Used for KPIs where ANY occurrence is a failure (e.g., safety incidents).

**Logic**:
- If achievement > 0 (any incidents occurred) → Score = 0
- If achievement = 0 (no incidents) → Score = max × weight (perfect score)

**Use Case Example**: Safety incidents, compliance violations, critical errors

---

### Phase 3: Standard Calculation

If `get_1_is_zero = False`, proceed with standard calculation based on `kpi_type`:

#### **Type 3: Mistake Counting (Inverted)**

```python
if kpi_type == 3:
    if achivement == 0:
        temp_result = max_val
    else:
        temp_result = target_set / achivement
```

**Logic**:
- Zero mistakes → Maximum score (max_val, typically 1.4)
- Non-zero mistakes → Inverted ratio (target_set / achievement)
  - More mistakes = lower ratio = lower score

**Example**: 
- Target: 5 mistakes allowed, Achievement: 10 mistakes
- temp_result = 5 / 10 = 0.5

---

#### **Type 1 & 2: Percentage Calculation Mode**

If `percentage_cal = True`:

```python
# Step 1: Calculate achievement percentage
temp_achive = achivement / target_input

# Step 2: Calculate ratio against target
if kpi_type == 1:  # Bigger better
    temp_result = temp_achive / target_set
elif kpi_type == 2:  # Smaller better
    temp_result = target_set / temp_achive
```

**Logic**:
1. First, calculate what % of target was achieved: `achievement / target_input`
2. Then, compare this % to the target_set ratio

**Use Case**: When you want to track "% of target achieved" first, then score it

**Example (Type 1, Bigger Better)**:
- target_input = $1,000,000 (target amount)
- achievement = $1,200,000 (actual amount)
- target_set = 1.0 (100% expected)
- Step 1: temp_achive = 1,200,000 / 1,000,000 = 1.2 (120%)
- Step 2: temp_result = 1.2 / 1.0 = 1.2

---

#### **Type 1 & 2: Direct Calculation Mode**

If `percentage_cal = False`:

```python
if kpi_type == 1:  # Bigger better
    temp_result = achivement / target_input
elif kpi_type == 2:  # Smaller better
    temp_result = target_input / achivement
```

**Logic**:
- Directly compare achievement to target_input
- No intermediate percentage calculation

**Use Case**: When you want direct ratio comparison

**Example (Type 1, Bigger Better)**:
- target_input = 1,000,000 (auto-set from target_set)
- achievement = 1,200,000
- temp_result = 1,200,000 / 1,000,000 = 1.2

**Note**: When `percentage_cal = False`, the system auto-sets `target_input = target_set` on save.

---

### Phase 4: Apply Thresholds

```python
# Below minimum threshold → 0 score
if temp_result < min_val:
    return 0

# Above maximum threshold → capped at max
if temp_result > max_val:
    return max_val * weigth

# Within range → apply weight
return temp_result * weigth
```

**Threshold Logic**:
- **Below min** (default 0.4 = 40%): Performance too low, no points awarded
- **Above max** (default 1.4 = 140%): Performance capped at maximum to prevent outliers
- **Within range**: Score proportional to performance, multiplied by weight

---

## Calculation Examples

### Example 1: Revenue Growth (Type 1, Bigger Better, Percentage Mode)

**KPI Configuration**:
```python
kpi_type = 1  # Bigger better
percentage_cal = True
get_1_is_zero = False
```

**KPI Result Data**:
```python
weight = 0.25  # 25% of total score
min = 0.4      # 40% minimum
max = 1.4      # 140% maximum
target_set = 1.0       # 100% target
target_input = 1000000 # $1M revenue target
achievement = 1300000  # $1.3M achieved
```

**Calculation Steps**:
```python
# Step 1: Calculate achievement percentage
temp_achive = 1300000 / 1000000 = 1.3  # 130%

# Step 2: Calculate ratio vs target_set
temp_result = 1.3 / 1.0 = 1.3

# Step 3: Check thresholds
# 1.3 is between min (0.4) and max (1.4) → within range

# Step 4: Apply weight
final_result = 1.3 * 0.25 = 0.325
```

**Result**: 0.325 points (out of 0.25 max if achievement was at 100%)

---

### Example 2: Cost Reduction (Type 2, Smaller Better, Direct Mode)

**KPI Configuration**:
```python
kpi_type = 2  # Smaller better
percentage_cal = False
get_1_is_zero = False
```

**KPI Result Data**:
```python
weight = 0.20  # 20% of total score
min = 0.4
max = 1.4
target_set = 800000        # $800K cost target
target_input = 800000      # Auto-set from target_set
achievement = 700000       # $700K actual cost (good!)
```

**Calculation Steps**:
```python
# Direct calculation (percentage_cal = False)
temp_result = target_input / achievement
temp_result = 800000 / 700000 = 1.143

# Check thresholds
# 1.143 is between 0.4 and 1.4 → within range

# Apply weight
final_result = 1.143 * 0.20 = 0.229
```

**Result**: 0.229 points

**Interpretation**: Achieved 14.3% better than target (spent $700K vs $800K target), resulting in 114.3% performance.

---

### Example 3: Safety Incidents (Type 3, Mistake Counting)

**KPI Configuration**:
```python
kpi_type = 3  # Mistake counting
percentage_cal = False
get_1_is_zero = False
```

**KPI Result Data**:
```python
weight = 0.15  # 15% of total score
min = 0.4
max = 1.4
target_set = 2.0           # Max 2 incidents allowed
achievement = 5            # 5 incidents occurred (bad!)
```

**Calculation Steps**:
```python
# Type 3 logic
if achievement == 0:
    temp_result = max_val  # Would be 1.4 if 0 incidents
else:
    temp_result = target_set / achievement
    temp_result = 2.0 / 5 = 0.4

# Check thresholds
# 0.4 equals min → borderline, gets 0 points
if temp_result < min_val:
    return 0

final_result = 0
```

**Result**: 0 points (performance at minimum threshold)

---

### Example 4: Special Rule - Zero Tolerance (get_1_is_zero)

**KPI Configuration**:
```python
kpi_type = 1  # Doesn't matter with get_1_is_zero
percentage_cal = False
get_1_is_zero = True  # ← Special rule enabled
```

**KPI Result Data**:
```python
weight = 0.10
max = 1.4
achievement = 0  # No violations
```

**Calculation Steps**:
```python
# Special rule takes precedence
if get_1_is_zero:
    if achievement > 0:
        return 0  # Any violation = 0 points
    else:
        return weight * max_val
        return 0.10 * 1.4 = 0.14
```

**Result**: 0.14 points (full credit for zero violations)

**Alternative Scenario** (1 violation):
```python
achievement = 1  # One violation

if achievement > 0:
    return 0  # Zero points
```
**Result**: 0 points

---

### Example 5: Below Minimum Threshold

**KPI Configuration**:
```python
kpi_type = 1
percentage_cal = False
```

**KPI Result Data**:
```python
weight = 0.30
min = 0.4      # 40% minimum
target_input = 1000000
achievement = 350000  # Only 35% achieved (bad!)
```

**Calculation Steps**:
```python
# Calculate ratio
temp_result = 350000 / 1000000 = 0.35

# Check thresholds
if temp_result < min_val:  # 0.35 < 0.4
    return 0

final_result = 0
```

**Result**: 0 points (below minimum threshold)

---

### Example 6: Above Maximum Threshold

**KPI Configuration**:
```python
kpi_type = 1
percentage_cal = False
```

**KPI Result Data**:
```python
weight = 0.20
max = 1.4      # 140% maximum
target_input = 1000000
achievement = 2000000  # 200% achieved (excellent!)
```

**Calculation Steps**:
```python
# Calculate ratio
temp_result = 2000000 / 1000000 = 2.0

# Check thresholds
if temp_result > max_val:  # 2.0 > 1.4
    return max_val * weight
    return 1.4 * 0.20 = 0.28

final_result = 0.28
```

**Result**: 0.28 points (capped at maximum)

**Note**: Even though performance was 200%, score is capped at 140% to prevent extreme outliers from skewing total scores.

---

## Edge Cases

### Edge Case 1: Division by Zero

**Scenario**: `target_input = 0` or `achievement = 0` in division

**Handling**:
```python
temp_result = achivement / target_input if target_input else 0
```

The code uses conditional checks to prevent division by zero, defaulting to 0.

---

### Edge Case 2: Null/None Values

**Scenario**: Missing data (target_input or achievement not entered)

**Handling**:
```python
if self.target_input is None or self.achivement is None:
    return 0
```

Returns 0 if any required value is missing.

---

### Edge Case 3: Type 3 with Zero Achievement

**Scenario**: No mistakes (achievement = 0) in mistake counting

**Handling**:
```python
if kpi_type == 3:
    if achivement == 0:
        temp_result = max_val  # Full credit
```

Zero mistakes = maximum performance ratio (before applying weight).

---

### Edge Case 4: Negative Values

**Scenario**: What if achievement or target is negative?

**Current Handling**: Not explicitly validated in calculation logic

**Recommendation**: Add validation in model clean() method:
```python
def clean(self):
    if self.achivement and self.achivement < 0:
        raise ValidationError('Achievement cannot be negative')
    if self.target_input and self.target_input < 0:
        raise ValidationError('Target cannot be negative')
```

---

## Testing Calculations

### Manual Testing in Django Shell

```python
python manage.py shell
```

```python
from kpi_app.models import Alk_KPI, Alk_KPI_Result, Alk_Employee
from decimal import Decimal

# Get or create test data
kpi = Alk_KPI.objects.get(id=1)
employee = Alk_Employee.objects.get(id=1)

# Create test result
result = Alk_KPI_Result(
    year=2025,
    semester='1st SEM',
    month='1st',
    employee=employee,
    kpi=kpi,
    weigth=Decimal('0.25'),
    min=Decimal('0.4'),
    max=Decimal('1.4'),
    target_set=Decimal('1.0'),
    target_input=Decimal('1000000'),
    achivement=Decimal('1200000'),
)

# Test calculation (don't save yet)
score = result.calculate_final_result()
print(f"Calculated score: {score}")

# Save to database (will recalculate)
result.save()
print(f"Saved final_result: {result.final_result}")
```

### Unit Test Example

```python
# kpi_app/tests.py
from django.test import TestCase
from decimal import Decimal
from kpi_app.models import Alk_KPI_Result, Alk_KPI, Alk_Employee

class KPICalculationTestCase(TestCase):
    def setUp(self):
        # Create test KPI and employee
        self.kpi = Alk_KPI.objects.create(
            kpi_name='Test KPI',
            kpi_type=1,
            percentage_cal=False,
            get_1_is_zero=False
        )
        self.employee = Alk_Employee.objects.create(...)
    
    def test_type1_within_range(self):
        """Test Type 1 calculation within min-max range"""
        result = Alk_KPI_Result(
            kpi=self.kpi,
            employee=self.employee,
            weigth=Decimal('0.25'),
            min=Decimal('0.4'),
            max=Decimal('1.4'),
            target_input=Decimal('1000000'),
            achivement=Decimal('1200000'),
        )
        score = result.calculate_final_result()
        expected = Decimal('0.300')  # 1.2 * 0.25 = 0.30
        self.assertEqual(score, expected)
    
    def test_below_minimum_threshold(self):
        """Test score when below minimum threshold"""
        result = Alk_KPI_Result(
            kpi=self.kpi,
            employee=self.employee,
            weigth=Decimal('0.25'),
            min=Decimal('0.4'),
            target_input=Decimal('1000000'),
            achivement=Decimal('350000'),  # Only 35%
        )
        score = result.calculate_final_result()
        self.assertEqual(score, Decimal('0'))
    
    def test_get_1_is_zero_with_achievement(self):
        """Test get_1_is_zero flag with non-zero achievement"""
        self.kpi.get_1_is_zero = True
        self.kpi.save()
        
        result = Alk_KPI_Result(
            kpi=self.kpi,
            employee=self.employee,
            weigth=Decimal('0.10'),
            max=Decimal('1.4'),
            achivement=Decimal('1'),  # Any achievement
        )
        score = result.calculate_final_result()
        self.assertEqual(score, Decimal('0'))  # Should be 0
```

Run tests:
```bash
python manage.py test kpi_app.tests.KPICalculationTestCase
```

---

## Summary Table

| Scenario | kpi_type | percentage_cal | get_1_is_zero | Formula |
|----------|----------|----------------|---------------|---------|
| Revenue growth (%) | 1 | True | False | `(achievement/target_input) / target_set * weight` |
| Revenue growth (direct) | 1 | False | False | `achievement / target_input * weight` |
| Cost reduction | 2 | False | False | `target_input / achievement * weight` |
| Cycle time reduction (%) | 2 | True | False | `target_set / (achievement/target_input) * weight` |
| Mistakes counting | 3 | - | False | `target_set / achievement * weight` (if ach≠0) |
| Zero tolerance violations | - | - | True | `0` if ach>0, else `max * weight` |

**All formulas subject to threshold checks**: Below min → 0, Above max → capped at max × weight

---

**Last Updated**: December 30, 2025

For data model details, see [Data Model Documentation](data-model.md).
