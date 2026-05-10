from app import app, db
import os

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()
    print("Recreating all tables...")
    db.create_all()
    print("Done.")

# Also delete the SQLite DB if it exists, just in case
sqlite_db = os.path.join("instance", "users.db")
if os.path.exists(sqlite_db):
    print(f"Deleting {sqlite_db}...")
    os.remove(sqlite_db)
