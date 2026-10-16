import json
from pathlib import Path


def get_lang(scope: str, suffix: str = "es") -> dict:
    current_dir = Path(__file__).resolve().parent
    for i in current_dir.iterdir():
        if i.is_file() and i.suffix == ".json" and i.stem == suffix:
            return dict(json.loads(i.read_text(encoding="utf-8"))).get(scope, {})
    return {}


def get_langs() -> tuple[str, ...]:
    current_dir = Path(__file__).resolve().parent
    langs = set()
    for file in current_dir.iterdir():
        if file.is_file() and file.suffix == ".json":
            parts = file.stem.split(".")
            langs.add(parts[-1])
    return tuple(langs)
