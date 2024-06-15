import streamlit as st
from utils.Game_file import GameTinder
from utils.Database_file import Database

db = Database()
db.refresh_active_status()
db.refresh_images()
tindergame = GameTinder()

tindergame.display_play_page()

