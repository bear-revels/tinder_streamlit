import streamlit as st

class Leaderboard:
    def __init__(self, db):
        """Initialize the UI class with a database instance."""
        self.db = db

    def display_leaderboard_page(self):
        """Display the leaderboard page."""
        st.write("Leaderboard")
        leaderboard_data = self.db.get_leaderboard()
        st.write(leaderboard_data)