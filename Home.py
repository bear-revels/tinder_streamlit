import streamlit as st
from utils.Database_file import Database
from archive.Elo_file import Elo
# from utils.Game_file import Game
# from utils.Ui_file import UI
from utils.Home_file import Home


def main():
    st.title("ARCADE")

    # db = Database()
    # db.refresh_images()
    # ui = UI(db)
    # ui.display_home_page(db)
    
    db = Database()
    home = Home(db)

    home.display_home_page()

    # pages = {
    #     "Home": ui.display_home_page,
    #     "Play": ui.display_play_page,
    #     "Contribute": ui.display_contribute_page,
    #     "Leaderboard": ui.display_leaderboard_page,
    # }

    # st.sidebar.title("Navigation")
    # selection = st.sidebar.radio("Go to", list(pages.keys()))

    # page = pages[selection]

    # if page:
    #     page()


if __name__ == "__main__":
    main()
