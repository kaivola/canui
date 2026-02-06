import cantools
from cantools.database.can.database import Database


def get_db(path: str) -> Database | None:
    try:
        db = cantools.database.load_file(path)
        if not isinstance(db, Database):
            raise RuntimeError()
        return db
    except Exception as e:
        print(f"ERROR opening DBC file: {type(e).__name__}: {e}")
