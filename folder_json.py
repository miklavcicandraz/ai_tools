import json
from pathlib import Path

# Define maximum file size in bytes (10 MB = 10 * 1024 * 1024)
MAX_FILE_SIZE = 10 * 1024 * 1024 

def folder_to_dict(path: Path) -> dict:
    """Recursively converts a directory structure into a nested dictionary, with a 10MB limit."""
    result = {}
    
    for item in sorted(path.iterdir()):
        # Skip hidden files/folders and Python caches
        if item.name.startswith('.') or item.name == '__pycache__':
            continue
            
        if item.is_dir():
            result[item.name] = folder_to_dict(item)
        elif item.is_file():
            try:
                # Check file size before reading
                file_size = item.stat().st_size
                if file_size > MAX_FILE_SIZE:
                    result[item.name] = f"[File too large - {file_size / 1024 / 1024:.1f} MB - content omitted]"
                    continue

                # Read text content
                result[item.name] = item.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # Fallback for binary files
                result[item.name] = "[Binary file - content omitted]"
                
    return result

def main():
    target_dir = Path(".") 
    output_filename = "structure.json"
    
    print(f"🔍 Scanning directory: {target_dir.resolve().name} (Max file size: {MAX_FILE_SIZE / 1024 / 1024:.1f} MB)...")
    
    structure = {
        target_dir.resolve().name: folder_to_dict(target_dir.resolve())
    }
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=4)
        
    print(f"✨ Successfully exported structure and contents to '{output_filename}'!")

if __name__ == "__main__":
    main()
