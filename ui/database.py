import sqlite3

class Database:
    def __init__(self, db_name="filemanager.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    md5sum TEXT NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_file(self, path, md5sum):
        try:
            self.cursor.execute("INSERT INTO files (path, md5sum) VALUES (?, ?)", (path, md5sum))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting file: {e}")

    def query_file(self, path):
        try:
            self.cursor.execute("SELECT md5sum FROM files WHERE path = ?", (path,))
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Error querying file: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()
