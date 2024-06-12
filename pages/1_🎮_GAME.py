import streamlit as st
from utils.Ui_file import UI
from utils.Database_file import Database

db = Database()
db.refresh_images()
game = UI(db)

game.display_play_page()

