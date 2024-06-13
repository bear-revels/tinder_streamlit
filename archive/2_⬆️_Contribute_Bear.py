import streamlit as st
from utils.Game_file import Game
from utils.Database_file import Database
from archive.Contribute_file import Contribute

db = Database()
contribution = Contribute(db)

contribution.display_contribute_page()