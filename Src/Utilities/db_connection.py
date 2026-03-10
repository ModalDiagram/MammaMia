import sqlite3
import datetime

class db_connection:
    def __init__(self) -> None:
        connection = sqlite3.connect("mammamia.db")
        self.cursor = connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS kitsu_id (id INTEGER, showname TEXT, date TEXT, search_date TEXT)"
        )
    
    def get_animeworld_showname(self, kitsu_id):
        rows = self.cursor.execute("SELECT * FROM kitsu_id WHERE id = ?", (kitsu_id,)).fetchall()
        for row in rows:
            return row[1], row[2]
        return None
    
    def set_animeworld_showname(self, kitsu_id, showname, date):
        self.cursor.execute(
            "INSERT INTO kitsu_id VALUES (?, ?, ?, ?)",
            (kitsu_id, showname, date, datetime.datetime.now()),
        )