import sqlite3
import datetime

class db_connection:
    def __init__(self) -> None:
        connection = sqlite3.connect("mammamia.db")
        self.cursor = connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS animeworld_episodes (
            id INTEGER, 
            episode_number INTEGER,
            episode_url TEXT,
            language TEXT,
            search_date TEXT
            )''')
        
    async def get_episode_urls(self, kitsu_id, episode_number, client):
        episode_urls = []
        rows = self.cursor.execute("SELECT episode_url, language FROM animeworld_episodes WHERE id = ? AND episode_number = ?", (kitsu_id, episode_number,)).fetchall()
        for row in rows:
            response = await client.head(row[0])
            if response.status_code == 404:
                self.cursor.execute("DELETE FROM animeworld_episodes WHERE id = ? AND episode_number = ?", (kitsu_id, episode_number,))
            else:
                episode_urls.append(row)
        return episode_urls
            
    def set_episode_url(self, kitsu_id, episode_number, episode_url, language_original):
        self.cursor.execute(
            "INSERT INTO animeworld_episodes VALUES (?, ?, ?, ?, ?)",
            (kitsu_id, episode_number, episode_url, language_original, datetime.datetime.now(),),
        )