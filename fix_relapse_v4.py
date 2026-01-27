
import os

file_path = r'C:\dev\alkana_kpi\kpi_app\templates\kpi_app\portal\manager_review.html'

def fix_relapse():
    print(f"Reading {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # --- VERIFICATION CHECKS (Ensure Dep 17-22 are present) ---
    errors = []
    
    # Dep 21/22 Check (HTMX Inputs)
    if 'hx-post="{% url \'manager_save_kpi\' result.id %}"' not in content:
        errors.append("Deployment #21/22 (Smart Inline Editing) seems missing.")

    # Dep 19 Check (Lock Icon)
    if 'bi-lock-fill text-success' not in content:
        errors.append("Deployment #19 (Lock Icon/Checkbox) seems missing.")

    if errors:
        print("CRITICAL VALIDATION ERRORS FOUND. SKIPPING FIX TO AVOID CORRUPTION:")
        for e in errors:
            print(f"  - {e}")
        return

    # --- SURGICAL FIX ---
    target_bad = "{% if current_month==m %}"
    target_good = "{% if current_month == m %}"
    
    if target_bad in content:
        print(f"Found broken syntax: '{target_bad}'. Fixing...")
        new_content = content.replace(target_bad, target_good)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Successfully WROTE fixed content to file.")
            
            # Double Check
            with open(file_path, 'r', encoding='utf-8') as f:
                re_read = f.read()
                if target_good in re_read and target_bad not in re_read:
                    print("VERIFICATION: SUCCESS. File fixed.")
                else:
                    print("VERIFICATION: FAILED. Write might have failed.")
        except Exception as e:
            print(f"Error writing file: {e}")
            
    elif target_good in content:
        print("File ALREADY contains the correct syntax. No changes needed.")
    else:
        print(f"Could not find exact string '{target_bad}' to replace.")

if __name__ == "__main__":
    fix_relapse()
