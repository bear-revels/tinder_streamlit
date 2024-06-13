# import sqlite3
# import os
# from pathlib import Path


# class Database:
#     def __init__(self):
#         """Initialize the database and create tables if they don't exist."""
#         base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
#         db_path = os.path.join(base_dir, '..', 'arcade.db')  # Construct the path to the database file
#         self.conn = sqlite3.connect(db_path)  # Connect to the database
#         self.create_tables()
#         self.refresh_images()

#     def create_tables(self):
#         """Create necessary tables for the application."""
#         cursor = self.conn.cursor()
#         cursor.execute(
#             """
#         CREATE TABLE IF NOT EXISTS creators (
#             creator_id INTEGER PRIMARY KEY,
#             creator_name TEXT UNIQUE
#         )
#         """
#         )
#         cursor.execute(
#             """
#         CREATE TABLE IF NOT EXISTS players (
#             player_id INTEGER PRIMARY KEY,
#             player_name TEXT UNIQUE
#         )
#         """
#         )
#         cursor.execute(
#             """
#         CREATE TABLE IF NOT EXISTS images (
#             image_id INTEGER PRIMARY KEY,
#             creator_id INTEGER,
#             is_real INTEGER,
#             is_active INTEGER,
#             filepath TEXT UNIQUE,
#             FOREIGN KEY (creator_id) REFERENCES creators (creator_id)
#         )
#         """
#         )
#         cursor.execute(
#             """
#         CREATE TABLE IF NOT EXISTS scores (
#             game_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             player_id INTEGER,
#             level INTEGER,
#             image1_id INTEGER,
#             image2_id INTEGER,
#             selection INTEGER,
#             FOREIGN KEY (player_id) REFERENCES players (player_id),
#             FOREIGN KEY (image1_id) REFERENCES images (image_id),
#             FOREIGN KEY (image2_id) REFERENCES images (image_id)
#         )
#         """
#         )
#         self.conn.commit()

#     def refresh_images(self):
#         """Refresh image list from directories and update the database."""
#         real_path = Path("images/real")
#         genai_path = Path("images/genai")

#         cursor = self.conn.cursor()

#         # Set all images to inactive before refreshing
#         cursor.execute("UPDATE images SET is_active = 0")
    
#         # Check and update real images
#         for img_path in real_path.glob("*"):
#             if img_path.is_file():
#                 creator_name = img_path.stem.split("_")[0]
#                 cursor.execute(
#                     "INSERT OR IGNORE INTO creators (creator_name) VALUES (?)",
#                     (creator_name,),
#                 )
#                 cursor.execute(
#                     "SELECT creator_id FROM creators WHERE creator_name = ?",
#                     (creator_name,),
#                 )
#                 creator_id = cursor.fetchone()[0]
#                 cursor.execute(
#                     """
#                     INSERT OR IGNORE INTO images (creator_id, is_real, is_active, filepath) 
#                     VALUES (?, 1, 1, ?)
#                     """,
#                     (creator_id, str(img_path).replace("\\", "/")),
#                 )
#                 cursor.execute(
#                     """
#                     UPDATE images SET is_active = 1 
#                     WHERE filepath = ?
#                     """,
#                     (str(img_path).replace("\\", "/"),)
#                 )

#         # Check and update AI images
#         for img_path in genai_path.glob("*"):
#             if img_path.is_file():
#                 creator_name = img_path.stem.split("_")[0]
#                 cursor.execute(
#                     "INSERT OR IGNORE INTO creators (creator_name) VALUES (?)",
#                     (creator_name,),
#                 )
#                 cursor.execute(
#                     "SELECT creator_id FROM creators WHERE creator_name = ?",
#                     (creator_name,),
#                 )
#                 creator_id = cursor.fetchone()[0]
#                 cursor.execute(
#                     """
#                     INSERT OR IGNORE INTO images (creator_id, is_real, is_active, filepath) 
#                     VALUES (?, 0, 1, ?)
#                     """,
#                     (creator_id, str(img_path).replace("\\", "/")),
#                 )
#                 cursor.execute(
#                     """
#                     UPDATE images SET is_active = 1 
#                     WHERE filepath = ?
#                     """,
#                     (str(img_path).replace("\\", "/"),)
#                 )

#         self.conn.commit()

#     def get_random_images(self):
#         """Get a pair of random images (one real and one AI)."""
#         cursor = self.conn.cursor()
#         cursor.execute(
#             "SELECT * FROM images WHERE is_active = 1 AND is_real = 1 ORDER BY RANDOM() LIMIT 1"
#         )
#         real_image = cursor.fetchone()
#         cursor.execute(
#             "SELECT * FROM images WHERE is_active = 1 AND is_real = 0 ORDER BY RANDOM() LIMIT 1"
#         )
#         genai_image = cursor.fetchone()
#         return real_image, genai_image

#     def record_score(self, player_id, level, image1_id, image2_id, selection):
#         """Record the score of a player."""
#         cursor = self.conn.cursor()
#         cursor.execute(
#             "INSERT INTO scores (player_id, level, image1_id, image2_id, selection) VALUES (?, ?, ?, ?, ?)",
#             (player_id, level, image1_id, image2_id, selection),
#         )
#         self.conn.commit()

#     def add_player(self, player_name):
#         """Add a new player to the database."""
#         cursor = self.conn.cursor()
#         cursor.execute(
#             "INSERT OR IGNORE INTO players (player_name) VALUES (?)", (player_name,)
#         )
#         self.conn.commit()
#         cursor.execute(
#             "SELECT player_id FROM players WHERE player_name = ?", (player_name,)
#         )
#         return cursor.fetchone()[0]

#     def add_image(self, creator_name, is_real, filepath):
#         """Add a new image to the database."""
#         cursor = self.conn.cursor()
#         cursor.execute(
#             "INSERT OR IGNORE INTO creators (creator_name) VALUES (?)", (creator_name,)
#         )
#         cursor.execute(
#             "SELECT creator_id FROM creators WHERE creator_name = ?", (creator_name,)
#         )
#         creator_id = cursor.fetchone()[0]
#         cursor.execute(
#             "INSERT OR IGNORE INTO images (creator_id, is_real, is_active, filepath) VALUES (?, ?, 1, ?)",
#             (creator_id, is_real, filepath.replace("\\", "/")),
#         )
#         self.conn.commit()

#     def get_leaderboard(self):
#         """Get the leaderboard data."""
#         cursor = self.conn.cursor()
#         cursor.execute(
#             """
#         SELECT players.player_name, COUNT(scores.game_id) AS streak
#         FROM scores
#         JOIN players ON scores.player_id = players.player_id
#         GROUP BY scores.player_id
#         ORDER BY streak DESC
#         """
#         )
#         return cursor.fetchall()

#     def select_images_real(self):
#         """selects the real images from the images table"""
#         self.conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row
#         cursor = self.conn.cursor()
#         cursor.execute(
#             """
#             SELECT * FROM images WHERE is_real = 1
#             """
#         )
#         rows = cursor.fetchall()
#         # Convert rows to a list of dictionaries
#         dict_rows = [dict(row) for row in rows]
#         return dict_rows

#     def select_images_ai(self):
#         """selects the ai images from the images table"""
#         self.conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row
#         cursor = self.conn.cursor()
#         cursor.execute(
#             """
#             SELECT * FROM images WHERE is_real = 0
#             """
#         )
#         rows = cursor.fetchall()
#         # Convert rows to a list of dictionaries
#         dict_rows = [dict(row) for row in rows]
#         return dict_rows

#     def close(self):
#         """Close the database connection."""
#         self.conn.close()

# Utils/Database_file.py
import sqlite3
import pandas as pd
import os
from pathlib import Path

class Database:
    """Class to handle database interactions."""
    
    def __init__(self):
        """Initialize the database connection."""
        self.conn = sqlite3.connect('arcade.db')
        self.create_tables()
        self.update_schema()

    def create_tables(self):
        """Create required tables in the database if they do not exist."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS creators (
                    creator_id INTEGER PRIMARY KEY,
                    creator_name TEXT UNIQUE
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    image_id INTEGER PRIMARY KEY,
                    creator_id INTEGER,
                    is_real TEXT,
                    is_active INTEGER,
                    filepath TEXT UNIQUE,
                    score REAL DEFAULT 2500,  -- Initial ELO score
                    FOREIGN KEY (creator_id) REFERENCES creators (creator_id)
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    player_id INTEGER PRIMARY KEY,
                    player_name TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                    image_id INTEGER,
                    score REAL,
                    FOREIGN KEY (image_id) REFERENCES images (image_id)
                )
            """)

    def update_schema(self):
        """Update the database schema to ensure all required tables and columns exist."""
        with self.conn:
            # Check and add missing columns for the 'images' table
            self.ensure_column_exists('images', 'score', 'REAL', '2500')
            self.ensure_column_exists('images', 'is_active', 'INTEGER', '1')

            # Check and add missing columns for the 'creators' table
            self.ensure_column_exists('creators', 'creator_id', 'INTEGER PRIMARY KEY')
            self.ensure_column_exists('creators', 'creator_name', 'TEXT UNIQUE')

            # Check and add missing columns for the 'players' table
            self.ensure_column_exists('players', 'player_id', 'INTEGER PRIMARY KEY')
            self.ensure_column_exists('players', 'player_name', 'TEXT')

            # Check and add missing columns for the 'scores' table
            self.ensure_column_exists('scores', 'image_id', 'INTEGER')
            self.ensure_column_exists('scores', 'score', 'REAL')

    def ensure_column_exists(self, table_name, column_name, column_type, default_value=None):
        """Ensure a specific column exists in the table."""
        cursor = self.conn.execute(f"PRAGMA table_info({table_name})")
        columns = [info[1] for info in cursor.fetchall()]
        if column_name not in columns:
            if default_value is not None:
                self.conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT {default_value}")
            else:
                self.conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

    def add_creator(self, name):
        """Add a new creator to the database and return the creator ID."""
        with self.conn:
            cursor = self.conn.execute("INSERT INTO creators (creator_name) VALUES (?)", (name,))
        return cursor.lastrowid

    def get_or_create_creator(self, name):
        """Get a creator ID by name, or create a new creator if it doesn't exist."""
        cursor = self.conn.execute("SELECT creator_id FROM creators WHERE creator_name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return row[0]
        return self.add_creator(name)
    
    def add_image(self, creator_id, is_real, filepath):
        """Add a new image to the database."""
        if not self.image_exists(filepath):
            with self.conn:
                self.conn.execute("""
                    INSERT INTO images (creator_id, is_real, is_active, filepath)
                    VALUES (?, ?, 1, ?)
                """, (creator_id, is_real, filepath))
    
    def image_exists(self, filepath):
        """Check if an image already exists in the database."""
        cursor = self.conn.execute("SELECT 1 FROM images WHERE filepath = ?", (filepath,))
        return cursor.fetchone() is not None
    
    def get_highest_index(self, creator_id):
        """Get the highest index number for images by the given creator."""
        cursor = self.conn.execute("""
            SELECT MAX(CAST(SUBSTR(filepath, INSTR(filepath, '_') + 1, INSTR(filepath, '.') - INSTR(filepath, '_') - 1) AS INTEGER))
            FROM images
            WHERE creator_id = ?
        """, (creator_id,))
        row = cursor.fetchone()
        if row and row[0]:
            return row[0]
        return 0

    def get_active_images(self):
        """Retrieve all active images from the database."""
        cursor = self.conn.execute("SELECT image_id, creator_id, is_real, is_active, filepath, score FROM images WHERE is_active = 1")
        images = cursor.fetchall()
        return [{"image_id": row[0], "creator_id": row[1], "is_real": row[2], "is_active": row[3], "filepath": row[4], "score": row[5]} for row in images]
    
    def refresh_active_status(self):
        """Refresh the is_active status of images based on their existence in the filesystem."""
        cursor = self.conn.execute("SELECT image_id, filepath FROM images")
        images = cursor.fetchall()
        
        for image_id, filepath in images:
            is_active = os.path.exists(filepath)
            with self.conn:
                self.conn.execute("UPDATE images SET is_active = ? WHERE image_id = ?", (is_active, image_id))
    
    def update_score(self, image_id, new_score):
        """Update the ELO score for an image."""
        with self.conn:
            self.conn.execute("UPDATE images SET score = ? WHERE image_id = ?", (new_score, image_id))

    def get_scores(self):
        """Retrieve all scores from the database."""
        cursor = self.conn.execute("SELECT * FROM scores")
        scores = cursor.fetchall()
        return pd.DataFrame(scores, columns=["Image ID", "Score"])

    def get_leaderboard_data(self):
        """Retrieve all necessary data for the leaderboard."""
        cursor = self.conn.execute("""
            SELECT images.image_id, images.filepath, images.score, creators.creator_name
            FROM images
            JOIN creators ON images.creator_id = creators.creator_id
            WHERE images.is_active = 1
            ORDER BY images.score DESC
        """)
        data = cursor.fetchall()
        return [{"image_id": row[0], "filepath": row[1], "score": row[2], "creator_name": row[3]} for row in data]
    
    def refresh_images(self):
        """Refresh image list from directories and update the database."""
        real_path = Path("images/real")
        genai_path = Path("images/genai")

        cursor = self.conn.cursor()

        # Set all images to inactive before refreshing
        cursor.execute("UPDATE images SET is_active = 0")
    
        # Check and update real images
        for img_path in real_path.glob("*"):
            if img_path.is_file():
                creator_name = img_path.stem.split("_")[0]
                cursor.execute(
                    "INSERT OR IGNORE INTO creators (creator_name) VALUES (?)",
                    (creator_name,),
                )
                cursor.execute(
                    "SELECT creator_id FROM creators WHERE creator_name = ?",
                    (creator_name,),
                )
                creator_id = cursor.fetchone()[0]
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO images (creator_id, is_real, is_active, filepath) 
                    VALUES (?, 1, 1, ?)
                    """,
                    (creator_id, str(img_path).replace("\\", "/")),
                )
                cursor.execute(
                    """
                    UPDATE images SET is_active = 1 
                    WHERE filepath = ?
                    """,
                    (str(img_path).replace("\\", "/"),)
                )

        #Check and update AI images
        for img_path in genai_path.glob("*"):
            if img_path.is_file():
                creator_name = img_path.stem.split("_")[0]
                cursor.execute(
                    "INSERT OR IGNORE INTO creators (creator_name) VALUES (?)",
                    (creator_name,),
                )
                cursor.execute(
                    "SELECT creator_id FROM creators WHERE creator_name = ?",
                    (creator_name,),
                )
                creator_id = cursor.fetchone()[0]
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO images (creator_id, is_real, is_active, filepath) 
                    VALUES (?, 0, 1, ?)
                    """,
                    (creator_id, str(img_path).replace("\\", "/")),
                )
                cursor.execute(
                    """
                    UPDATE images SET is_active = 1 
                    WHERE filepath = ?
                    """,
                    (str(img_path).replace("\\", "/"),)
                )

        self.conn.commit()
