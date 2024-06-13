import streamlit as st
# from utils.Ui_file import UI
from utils.Game_file import Game
from utils.Database_file import Database

# initializing database instance and refreshing images
# db = Database()
# db.refresh_images()
# game = UI(db)

# game.display_play_page()

db = Database()
db.refresh_images()
game = Game(db)

game.display_play_page()

