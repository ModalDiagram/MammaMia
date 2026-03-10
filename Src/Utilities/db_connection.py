import sqlite3
import datetime

class db_connection:
    def __init__(self) -> None:
        connection = sqlite3.connect("mammamia.db")
        self.cursor = connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS kitsu_id (id INTEGER AUTO_INCREMENT PRIMARY KEY, showname TEXT, date TEXT, search_date TEXT)")
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS animeworld_urls (
            id INTEGER, 
            anime_url TEXT, 
            search_date TEXT, 
            FOREIGN KEY(id) REFERENCES kitsu_id(id))''')
    
    def get_animeworld_showname(self, kitsu_id):
        rows = self.cursor.execute("SELECT showname, date FROM kitsu_id WHERE id = ?", (kitsu_id,)).fetchall()
        for row in rows:
            return row[0], row[1]
        return None
    
    def set_animeworld_showname(self, kitsu_id, showname, date):
        self.cursor.execute(
            "INSERT INTO kitsu_id VALUES (?, ?, ?, ?)",
            (kitsu_id, showname, date, datetime.datetime.now()),
        )
    
    def get_animeworld_urls(self, showname, date):
        anime_urls = []
        rows = self.cursor.execute("SELECT anime_url FROM kitsu_id JOIN animeworld_url WHERE showname = ? AND date = ?", (showname, date,)).fetchall()
        for row in rows:
            anime_urls.append(row[0])
        return anime_urls
        
    def set_animeworld_urls(self, showname, date, anime_urls):
        for anime_url in anime_urls:
            self.cursor.execute(
                "INSERT INTO animeworld_url (id, anime_url, search_date) SELECT id, ?, ? FROM kitsu_id WHERE showname = ? AND date = ?",
                (anime_url, datetime.datetime.now(), showname, date),
            )