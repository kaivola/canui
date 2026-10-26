import json
import cantools
from pathlib import Path
from cantools.database.can.database import Database

from schemas.settings import Settings
from schemas.metadata import Metadata

settings = Settings()


def get_dbc_files() -> list[str]:
    dir_path = Path(settings.dbc_dir)
    if not dir_path.exists() or not dir_path.is_dir():
        return []

    return [file.name for file in dir_path.glob("*.dbc") if file.is_file()]


def read_dbc_file(filename: str) -> Database | None:
    file_path = Path(settings.dbc_dir, filename)
    try:
        db = cantools.database.load_file(file_path)
        if not isinstance(db, Database):
            raise RuntimeError()
        return db
    except Exception as e:
        print(f"ERROR opening DBC file: {type(e).__name__}: {e}")


def get_metadata(filename: str) -> Metadata | None:
    json_file = filename.replace(".dbc", ".json")
    file_path = Path(settings.dbc_dir, json_file)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        metadata = Metadata.model_validate(raw_data)
        return metadata

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
