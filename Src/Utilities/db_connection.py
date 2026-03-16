import sqlite3
import datetime

class db_connection:
    def __init__(self) -> None:
        connection = sqlite3.connect("mammamia.db")
        self.cursor = connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS kitsu_id (id INTEGER AUTO_INCREMENT PRIMARY KEY, showname TEXT, date TEXT, search_date TEXT)")
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS animeworld_episodes (
            id INTEGER, 
            episode_number INTEGER,
            episode_url TEXT,
            language TEXT,
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
            (kitsu_id, showname, date, datetime.datetime.now(),),
        )
        
    def get_episode_urls(self, kitsu_id, episode_number):
        episode_urls = []
        rows = self.cursor.execute("SELECT episode_url, language FROM animeworld_episodes WHERE id = ? AND episode_number = ?", (kitsu_id, episode_number,)).fetchall()
        for row in rows:
            episode_urls.append(row)
        return episode_urls
            
    def set_episode_url(self, kitsu_id, episode_number, episode_url, language_original):
        self.cursor.execute(
            "INSERT INTO animeworld_episodes VALUES (?, ?, ?, ?, ?)",
            (kitsu_id, episode_number, episode_url, language_original, datetime.datetime.now(),),
        )