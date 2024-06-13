import streamlit as st
from utils.Game_file import GameFacemash
from utils.Database_file import Database

# initializing database instance and refreshing images
# db = Database()
# db.refresh_images()
# game = UI(db)

# game.display_play_page()

db = Database()
db.refresh_active_status()
game = GameFacemash()

game.display_game_page()

