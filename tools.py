from pathlib import Path
from config import CODEBASE_ROOT, IGNORE_DIRS

MAX_FILE_LINES = 200
MAX_MATCHES = 50


def _safe_resolve(path: Path) -> Path:
    resolved = path.resolve()
    if not str(resolved).startswith(str(CODEBASE_ROOT)):
        raise ValueError("Access outside allowed root")
    return resolved


def list_files(root_path: str = ".", recursive: bool = False):
    base = _safe_resolve(CODEBASE_ROOT / root_path)

    directories = []
    files = []
    total_files = 0

    for entry in base.iterdir():
        if entry.name in IGNORE_DIRS:
            continue

        if entry.is_dir():
            directories.append(entry.name)
            if recursive:
                for f in entry.rglob("*"):
                    if f.is_file():
                        total_files += 1
        elif entry.is_file():
            files.append({
                "path": str(entry.relative_to(CODEBASE_ROOT)),
                "size_bytes": entry.stat().st_size,
            })
            total_files += 1

    return {
        "path": str(base.relative_to(CODEBASE_ROOT)),
        "directories": sorted(directories),
        "files": sorted(files, key=lambda x: x["path"]),
        "total_files": total_files,
    }


def get_file(path: str, start_line: int = 1, end_line: int = MAX_FILE_LINES):
    file_path = _safe_resolve(CODEBASE_ROOT / path)

    if not file_path.is_file():
        raise ValueError("Not a file")

    if start_line < 1 or end_line < start_line:
        raise ValueError("Invalid line range")

    lines = file_path.read_text(errors="ignore").splitlines()

    total_lines = len(lines)
    end_line = min(end_line, start_line + MAX_FILE_LINES - 1, total_lines)

    selected = lines[start_line - 1 : end_line]

    return {
        "path": path,
        "start_line": start_line,
        "end_line": end_line,
        "total_lines": total_lines,
        "truncated": end_line < total_lines,
        "content": selected,
    }


def search_code(query: str, path: str = "."):
    base = _safe_resolve(CODEBASE_ROOT / path)

    matches = []

    for file in base.rglob("*"):
        if len(matches) >= MAX_MATCHES:
            break

        if not file.is_file():
            continue

        if file.name in IGNORE_DIRS:
            continue

        try:
            for lineno, line in enumerate(
                file.read_text(errors="ignore").splitlines(), start=1
            ):
                if query in line:
                    matches.append({
                        "path": str(file.relative_to(CODEBASE_ROOT)),
                        "line": lineno,
                        "snippet": line.strip(),
                    })
                    if len(matches) >= MAX_MATCHES:
                        break
        except Exception:
            continue

    return {
        "query": query,
        "count": len(matches),
        "matches": matches,
        "truncated": len(matches) >= MAX_MATCHES,
    }
