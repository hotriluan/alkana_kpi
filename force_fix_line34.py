#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Force fix for line 34 template syntax error.
This script surgically replaces the broken line with the correct syntax.
"""

import sys

template_path = r'C:\dev\alkana_kpi\kpi_app\templates\kpi_app\portal\manager_review.html'

# Read the file
with open(template_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print(f"Line 34 BEFORE: {repr(lines[33])}")

# Fix line 34 (index 33)
lines[33] = '                                <option value="{{ m }}" {% if current_month == m %}selected{% endif %}>\r\n'

print(f"Line 34 AFTER:  {repr(lines[33])}")

# Write back
with open(template_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ File updated successfully!")

# Verify
with open(template_path, 'r', encoding='utf-8') as f:
    verify_lines = f.readlines()
    print(f"\nVERIFICATION - Line 34: {repr(verify_lines[33])}")
    
    if '==' in verify_lines[33] and ' == ' not in verify_lines[33]:
        print("❌ ERROR: Fix did not persist!")
        sys.exit(1)
    elif ' == ' in verify_lines[33]:
        print("✅ SUCCESS: Fix verified!")
        sys.exit(0)
    else:
        print("⚠️  WARNING: Line doesn't contain comparison operator")
        sys.exit(2)
