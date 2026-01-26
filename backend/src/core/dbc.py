import cantools
from cantools.database.can.database import Database

def get_db(path: str) -> Database:
    try:
        return cantools.database.load_file(path)
    except Exception as e:
        print(f"ERROR opening DBC file: {type(e).__name__}: {e}")

