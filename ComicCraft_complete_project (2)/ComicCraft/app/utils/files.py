import re
from pathlib import Path
from uuid import uuid4


def safe_stem(value: str, fallback: str = "comic") -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-_")
    return value[:60] or fallback


def unique_filename(prefix: str, suffix: str) -> str:
    return f"{safe_stem(prefix)}-{uuid4().hex[:10]}{suffix}"


def to_static_url(path: Path, static_dir: Path) -> str:
    return f"/static/{path.relative_to(static_dir).as_posix()}"
