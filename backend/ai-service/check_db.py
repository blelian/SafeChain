# check_db.py
from app.db import engine

# Connect and list tables
with engine.connect() as conn:
    result = conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='public';")
    print("Tables in the database:")
    for row in result:
        print(row[0])
