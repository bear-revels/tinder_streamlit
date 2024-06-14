import streamlit as st
from utils.Database_file import Database
from utils.Contribute_file import Contribute

db = Database()
contribution = Contribute(db)

contribution.display_contribute_page()