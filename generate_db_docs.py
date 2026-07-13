import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alkana_kpi.settings')
django.setup()

from django.apps import apps
from django.db import connection

def get_field_type(field):
    return field.get_internal_type()

def generate_db_docs():
    output_lines = ["# Database Schema Documentation\n\n"]
    output_lines.append("Generated from Django models with sample data.\n\n")

    app_config = apps.get_app_config('kpi_app')
    models = app_config.get_models()

    for model in models:
        model_name = model.__name__
        table_name = model._meta.db_table
        docstring = model.__doc__ or "No description available."
        
        output_lines.append(f"## Table: {model_name} (`{table_name}`)\n")
        output_lines.append(f"- **Description**: {docstring.strip()}\n")
        
        # Columns
        output_lines.append(f"- **Columns**:\n")
        fields = model._meta.get_fields()
        columns = []
        for field in fields:
            if field.is_relation and field.many_to_many:
                continue # Skip M2M for now to keep it simple, or handle differently
            if field.is_relation and field.one_to_many:
                continue # Skip reverse relations
            
            try:
                name = field.name
                field_type = get_field_type(field)
                attrs = []
                if hasattr(field, 'primary_key') and field.primary_key:
                    attrs.append('PK')
                if hasattr(field, 'unique') and field.unique:
                    attrs.append('Unique')
                if hasattr(field, 'null') and field.null:
                    attrs.append('Null')
                if hasattr(field, 'default') and field.default is not django.db.models.fields.NOT_PROVIDED:
                    attrs.append(f'Default: {field.default}')
                
                attr_str = ", ".join(attrs)
                output_lines.append(f"    - `{name}` ({field_type}): {attr_str}\n")
                columns.append(name)
            except Exception as e:
                pass # Skip fields that cause issues
        
        # Sample Data
        output_lines.append(f"\n- **Sample Data** (First 5 rows):\n")
        try:
            objects = model.objects.all()[:5]
            if objects.exists():
                # Header
                header = "| " + " | ".join(columns) + " |"
                separator = "| " + " | ".join(["---"] * len(columns)) + " |"
                output_lines.append(header + "\n")
                output_lines.append(separator + "\n")
                
                for obj in objects:
                    row_data = []
                    for col in columns:
                        val = getattr(obj, col)
                        # Truncate long strings for readability
                        str_val = str(val)
                        if len(str_val) > 50:
                            str_val = str_val[:47] + "..."
                        row_data.append(str_val.replace("\n", " "))
                    output_lines.append("| " + " | ".join(row_data) + " |\n")
            else:
                output_lines.append("\n*No data available.*\n")
        except Exception as e:
             output_lines.append(f"\n*Error fetching sample data: {e}*\n")

        output_lines.append("\n---\n")

    with open('db_schema.md', 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print("Database documentation generated: db_schema.md")

if __name__ == '__main__':
    generate_db_docs()
