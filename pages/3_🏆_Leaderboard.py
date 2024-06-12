import streamlit as st
from utils.Ui_file import UI
from utils.Database_file import Database

db = Database()
db.refresh_images()
board = UI(db)

board.display_leaderboard_page()