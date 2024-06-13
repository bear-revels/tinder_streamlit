import sqlite3
import os
from pathlib import Path


class Database:
    def __init__(self):
        """Initialize the database and create tables if they don't exist."""
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        db_path = os.path.join(base_dir, '..', 'arcade.db')  # Construct the path to the database file
        self.conn = sqlite3.connect(db_path)  # Connect to the database
        self.create_tables()
        self.refresh_images()

    def create_tables(self):
        """Create necessary tables for the application."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS creators (
            creator_id INTEGER PRIMARY KEY,
            creator_name TEXT UNIQUE
        )
        """
        )
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT UNIQUE
        )
        """
        )
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY,
            creator_id INTEGER,
            is_real INTEGER,
            is_active INTEGER,
            filepath TEXT UNIQUE,
            FOREIGN KEY (creator_id) REFERENCES creators (creator_id)
        )
        """
        )
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS scores (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            level INTEGER,
            image1_id INTEGER,
            image2_id INTEGER,
            selection INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (image1_id) REFERENCES images (image_id),
            FOREIGN KEY (image2_id) REFERENCES images (image_id)
        )
        """
        )
        self.conn.commit()

    def refresh_images(self):
        """Refresh image list from directories and update the database."""
        real_path = Path("images/real")
        genai_path = Path("images/genai")

        cursor = self.conn.cursor()

        for img_path in real_path.glob("*"):
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
                "INSERT OR IGNORE INTO images (creator_id, is_real, is_active, filepath) VALUES (?, 1, 1, ?)",
                (creator_id, str(img_path).replace("\\", "/")),
            )

        for img_path in genai_path.glob("*"):
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
                "INSERT OR IGNORE INTO images (creator_id, is_real, is_active, filepath) VALUES (?, 0, 1, ?)",
                (creator_id, str(img_path).replace("\\", "/")),
            )

        self.conn.commit()

    def get_random_images(self):
        """Get a pair of random images (one real and one AI)."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM images WHERE is_active = 1 AND is_real = 1 ORDER BY RANDOM() LIMIT 1"
        )
        real_image = cursor.fetchone()
        cursor.execute(
            "SELECT * FROM images WHERE is_active = 1 AND is_real = 0 ORDER BY RANDOM() LIMIT 1"
        )
        genai_image = cursor.fetchone()
        return real_image, genai_image

    def record_score(self, player_id, level, image1_id, image2_id, selection):
        """Record the score of a player."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO scores (player_id, level, image1_id, image2_id, selection) VALUES (?, ?, ?, ?, ?)",
            (player_id, level, image1_id, image2_id, selection),
        )
        self.conn.commit()

    def add_player(self, player_name):
        """Add a new player to the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO players (player_name) VALUES (?)", (player_name,)
        )
        self.conn.commit()
        cursor.execute(
            "SELECT player_id FROM players WHERE player_name = ?", (player_name,)
        )
        return cursor.fetchone()[0]

    def add_image(self, creator_name, is_real, filepath):
        """Add a new image to the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO creators (creator_name) VALUES (?)", (creator_name,)
        )
        cursor.execute(
            "SELECT creator_id FROM creators WHERE creator_name = ?", (creator_name,)
        )
        creator_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT OR IGNORE INTO images (creator_id, is_real, is_active, filepath) VALUES (?, ?, 1, ?)",
            (creator_id, is_real, filepath.replace("\\", "/")),
        )
        self.conn.commit()

    def get_leaderboard(self):
        """Get the leaderboard data."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
        SELECT players.player_name, COUNT(scores.game_id) AS streak
        FROM scores
        JOIN players ON scores.player_id = players.player_id
        GROUP BY scores.player_id
        ORDER BY streak DESC
        """
        )
        return cursor.fetchall()

    def select_images_real(self):
        """selects the real images from the images table"""
        self.conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM images WHERE is_real = 1
            """
        )
        rows = cursor.fetchall()
        # Convert rows to a list of dictionaries
        dict_rows = [dict(row) for row in rows]
        return dict_rows

    def select_images_ai(self):
        """selects the ai images from the images table"""
        self.conn.row_factory = sqlite3.Row  # Set row_factory to sqlite3.Row
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM images WHERE is_real = 0
            """
        )
        rows = cursor.fetchall()
        # Convert rows to a list of dictionaries
        dict_rows = [dict(row) for row in rows]
        return dict_rows

    def close(self):
        """Close the database connection."""
        self.conn.close()
