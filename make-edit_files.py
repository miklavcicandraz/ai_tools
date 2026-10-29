import json
import shutil
from pathlib import Path

def apply_workspace_changes(json_path: str = "changes.json"):
    path = Path(json_path)
    if not path.exists():
        print(f"Error: Could not find transaction file '{json_path}'.")
        return
        
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{json_path}': {e}")
        return
        
    operations = data.get("operations", [])
    print(f"🚀 Processing {len(operations)} workspace operation(s)...\n")
    
    for i, op in enumerate(operations, 1):
        op_type = op.get("type")
        file_path = Path(op.get("path"))
        
        if op_type in ["write", "create"]:
            # Creates a new file or completely overwrites an existing one
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(op.get("content", ""), encoding="utf-8")
            print(f"[{i}] 📄 [WRITE] Created/Overwrote: {file_path}")
            
        elif op_type in ["patch", "edit"]:
            # Performs targeted search-and-replace (handles insertions, updates, and deletions)
            if not file_path.exists():
                print(f"[{i}] ❌ [PATCH ERROR] File not found: {file_path}")
                continue
                
            content = file_path.read_text(encoding="utf-8")
            search_text = op.get("search", "")
            replace_text = op.get("replace", "")
            
            if search_text not in content:
                print(f"[{i}] ❌ [PATCH ERROR] Search block not found in {file_path}. Skipping.")
                continue
                
            updated_content = content.replace(search_text, replace_text, 1)
            file_path.write_text(updated_content, encoding="utf-8")
            print(f"[{i}] ✏️ [PATCH] Successfully updated: {file_path}")
            
        elif op_type == "delete":
            # Deletes a file or directory
            if file_path.exists():
                if file_path.is_file():
                    file_path.unlink()
                    print(f"[{i}] 🗑️ [DELETE] Removed file: {file_path}")
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                    print(f"[{i}] 🗑️ [DELETE] Removed directory: {file_path}")
            else:
                print(f"[{i}] ⚠️ [DELETE WARNING] Path already missing: {file_path}")
        else:
            print(f"[{i}] ❓ [UNKNOWN] Unrecognized operation type: '{op_type}'")

    print("\n✨ All workspace operations completed successfully!")

if __name__ == "__main__":
    apply_workspace_changes()
