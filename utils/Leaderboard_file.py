# import streamlit as st

# class Leaderboard:
#     def __init__(self, db):
#         """Initialize the Leaderboard class with a database instance."""
#         self.db = db

#     def display_leaderboard_page(self):
#         """Display the leaderboard page."""
#         st.write("Leaderboard")
#         leaderboard_data = self.db.get_leaderboard()
#         st.write(leaderboard_data)





# Utils/Leaderboard_file.py
import streamlit as st
from utils.Database_file import Database

K = 10

class Elo:
    """ELO ranking system implementation."""
    
    @staticmethod
    def calculate_elo(winner_score, loser_score):
        """Calculate new ELO scores for winner and loser."""
        r1 = max(min(loser_score - winner_score, 400), -400)
        r2 = max(min(winner_score - loser_score, 400), -400)
        e1 = 1.0 / (1 + 10**(r1 / 400))
        e2 = 1.0 / (1 + 10**(r2 / 400))
        
        new_winner_score = round(winner_score + K * (1 - e1))
        new_loser_score = round(loser_score + K * (0 - e2))
        
        return new_winner_score, new_loser_score

class Leaderboard:
    """Class to handle the leaderboard functionality."""
    
    @staticmethod
    def display_leaderboard_page():
        """Displays the leaderboard page with top scores."""
        st.title("Leaderboard")
        db = Database()
        scores = db.get_leaderboard_data()
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)  # Sort by score
        
        for index, entry in enumerate(scores):
            st.write(f"Rank {index + 1}")
            col1, col2, col3 = st.columns([1, 3, 2])
            col1.image(entry['filepath'], width=100)
            col2.write(f"Score: {entry['score']}")
            col3.write(f"Creator: {entry['creator_name']}")
            st.write("---")
    
    @staticmethod
    def update_elo(winner_id, loser_id):
        """Update ELO scores for winner and loser images."""
        db = Database()
        winner = db.conn.execute("SELECT score FROM images WHERE image_id = ?", (winner_id,)).fetchone()
        loser = db.conn.execute("SELECT score FROM images WHERE image_id = ?", (loser_id,)).fetchone()
        
        if winner and loser:
            new_winner_score, new_loser_score = Elo.calculate_elo(winner[0], loser[0])
            db.update_score(winner_id, new_winner_score)
            db.update_score(loser_id, new_loser_score)