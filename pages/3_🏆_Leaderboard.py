import streamlit as st
# from utils.Ui_file import UI
from utils.Leaderboard_file import Leaderboard
from utils.Database_file import Database

db = Database()
board = Leaderboard(db)

board.display_leaderboard_page()