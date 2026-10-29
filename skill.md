# Workspace Modification Skill

When asked to create, modify, or delete files in a project, you must output your changes as a single JSON code block named `changes.json`. Do not output raw file dumps; use targeted operations to keep changes clean and efficient.

## Supported Operation Types

1. **`write` (or `create`)**: Writes brand new files or completely overwrites existing ones.
   - Keys required: `"type": "write"`, `"path"`, `"content"`
2. **`patch` (or `edit`)**: Finds an exact snippet of text (`search`) and replaces it (`replace`). Use this for insertions, minor code updates, or localized deletions.
   - Keys required: `"type": "patch"`, `"path"`, `"search"`, `"replace"`
3. **`delete`**: Removes a file or directory entirely.
   - Keys required: `"type": "delete"`, `"path"`

## Example JSON Output Structure

```json
{
  "operations": [
    {
      "type": "write",
      "path": "src/logger.py",
      "content": "import logging\n\ndef setup_logger():\n    logging.basicConfig(level=logging.INFO)\n"
    },
    {
      "type": "patch",
      "path": "src/main.py",
      "search": "def main():\n    print('Hello')",
      "replace": "def main():\n    print('Hello, World!')\n    setup_logger()"
    },
    {
      "type": "delete",
      "path": "src/temp_test.py"
    }
  ]
}
