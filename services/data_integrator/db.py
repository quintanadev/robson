import sqlite3
from pathlib import Path

def get_db():
  global db
  db = sqlite3.connect(Path.cwd() / 'db.sqlite3')
  db.row_factory = sqlite3.Row
  return db
