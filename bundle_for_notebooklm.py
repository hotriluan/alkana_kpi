import os

IGNORE_DIRS = {
    '.git', '.venv', '.opencode', '__pycache__', 'staticfiles', 'migrations', 'media', 'node_modules', '.gemini', '.idea', '.vscode'
}

IGNORE_FILES = {
    '.DS_Store', 'db.sqlite3', 'package-lock.json', 'yarn.lock'
}

EXTENSIONS = {
    '.py', '.html', '.css', '.js', '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.csv'
}

def is_text_file(filepath):
    """Simple check if file is likely text based on extension or content attempt."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in EXTENSIONS:
        return True
    return False

def bundle_project(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 1. Add DB Schema if it exists
        db_schema_path = os.path.join(root_dir, 'db_schema.md')
        if os.path.exists(db_schema_path):
            outfile.write(f"# File: db_schema.md\n\n")
            outfile.write("```markdown\n")
            with open(db_schema_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
            outfile.write("\n```\n\n")
            print("Included: db_schema.md")

        # 2. Walk directory
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Modify dirnames in-place to filter directories
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
            
            for filename in filenames:
                if filename in IGNORE_FILES:
                    continue
                if filename == 'db_schema.md': 
                    continue # Already added
                if filename == os.path.basename(output_file):
                    continue # Don't bundle the bundle itself
                if filename == 'generate_db_docs.py' or filename == 'bundle_for_notebooklm.py':
                    continue # Skip scripts used for generation

                filepath = os.path.join(dirpath, filename)
                relpath = os.path.relpath(filepath, root_dir)

                if is_text_file(filepath):
                    ext = os.path.splitext(filename)[1].lower().replace('.', '')
                    if not ext: ext = 'txt'
                    
                    # Create markdown header for file
                    outfile.write(f"# File: {relpath}\n\n")
                    outfile.write(f"```{ext}\n")
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                            content = infile.read()
                            if len(content) > 100000: # Skip very large files
                                outfile.write(f"... File content too large ({len(content)} chars) ...\n")
                            else:
                                outfile.write(content)
                    except Exception as e:
                        outfile.write(f"Error reading file: {e}\n")
                    
                    outfile.write("\n```\n\n")
                    print(f"Included: {relpath}")

    print(f"Bundle created: {output_file}")

if __name__ == '__main__':
    root = os.getcwd()
    output = 'alkana_kpi_bundle.md'
    bundle_project(root, output)
