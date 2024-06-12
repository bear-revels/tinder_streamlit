import streamlit as st
from utils.Database_file import Database
from utils.Elo_file import Elo
from utils.Game_file import Game
from utils.Ui_file import UI


def main():
    st.title("ARCADE")

    db = Database()
    db.refresh_images()
    ui = UI(db)

    ui.display_home_page()


if __name__ == "__main__":
    main()
