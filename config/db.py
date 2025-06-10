from psycopg2 import connect, sql
from dotenv import load_dotenv
import os

try:
    load_dotenv()
    url = os.getenv("DB_URL")
    pgsqlConn = connect(url)
except ValueError as e:
    print(f"Error connecting to database: {e}")
