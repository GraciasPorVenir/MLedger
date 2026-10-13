import json
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "MLedger"
DATA_DIR = Path.home() / ".local" / "share" / "MLedger"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class Config:
    db_path: Path = field(default_factory=lambda: DATA_DIR / "mledger.sqlite")

    def __post_init__(self) -> None:
        if not CONFIG_FILE.exists():
            self.save()
            return

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                d: dict = json.load(f)
                self.db_path = Path(d.get("db_path", self.db_path))
        except json.JSONDecodeError, KeyError:
            self.save()

    def save(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            d: dict = {"db_path": str(self.db_path)}
            json.dump(d, f, indent=4)
