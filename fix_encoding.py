"""
Fix Vietnamese encoding in existing output files
"""
from pathlib import Path
import sys

def fix_file_encoding(file_path: Path):
    """Re-save file with correct UTF-8-BOM encoding"""
    try: 
        # Read with UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Write back with UTF-8-BOM
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        
        print(f"✅ Fixed:  {file_path. name}")
        return True
    except Exception as e:
        print(f"❌ Error fixing {file_path.name}: {e}")
        return False

def main():
    output_folder = Path("output")
    
    if not output_folder.exists():
        print("❌ Output folder not found")
        return
    
    # Find all .txt files
    txt_files = list(output_folder. glob("*.txt"))
    
    if not txt_files: 
        print("⚠️ No .txt files found in output folder")
        return
    
    print(f"Found {len(txt_files)} files to fix\n")
    
    fixed = 0
    for file_path in txt_files: 
        if fix_file_encoding(file_path):
            fixed += 1
    
    print(f"\n✅ Fixed {fixed}/{len(txt_files)} files")
    print("\nNow open the files with Notepad or VS Code")

if __name__ == "__main__":
    main()