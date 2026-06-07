import os
import zipfile


ROOT = os.path.dirname(os.path.abspath(__file__))
ZIP_NAME = os.path.join(ROOT, "django_streaming_submission.zip")

EXCLUDE_DIRS = {".git", ".venv", "venv", "__pycache__", "media", "staticfiles", "_release"}
EXCLUDE_FILES = {"db.sqlite3", "django_streaming_submission.zip"}


def should_exclude(rel_path: str) -> bool:
    parts = rel_path.split(os.sep)
    if any(p in EXCLUDE_DIRS for p in parts):
        return True
    if os.path.basename(rel_path) in EXCLUDE_FILES:
        return True
    if rel_path.endswith((".pyc", ".pyo", ".pyd")):
        return True
    return False


def main() -> None:
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)

    with zipfile.ZipFile(ZIP_NAME, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for base, dirs, files in os.walk(ROOT):
            rel_base = os.path.relpath(base, ROOT)
            if rel_base == ".":
                rel_base = ""

            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(rel_base, d))]

            for filename in files:
                rel_path = os.path.join(rel_base, filename) if rel_base else filename
                if should_exclude(rel_path):
                    continue
                abs_path = os.path.join(base, filename)
                zf.write(abs_path, arcname=rel_path)

    print(ZIP_NAME)


if __name__ == "__main__":
    main()
