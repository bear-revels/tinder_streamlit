import streamlit as st
from utils.Leaderboard_file import Leaderboard
from utils.Database_file import Database

db = Database()
db.refresh_active_status()
db.refresh_images()
board = Leaderboard()
board.display_leaderboard_page()
