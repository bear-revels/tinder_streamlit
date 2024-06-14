import streamlit as st
from utils.Game_file import GameFacemash
from utils.Database_file import Database

db = Database()
db.refresh_active_status()
db.refresh_images()
facemashgame = GameFacemash()

facemashgame.display_game_page()

