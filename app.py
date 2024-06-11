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

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Play!"):
            st.session_state.page = "play"
        st.write("Start a new game")
    with col2:
        if st.button("Contribute"):
            st.session_state.page = "contribute"
        st.write("Add your photos to the game")
    with col3:
        if st.button("Leaderboard"):
            st.session_state.page = "leaderboard"
        st.write("Take a peek at your competition")

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "play":
        ui.display_play_page()
    elif st.session_state.page == "contribute":
        ui.display_contribute_page()
    elif st.session_state.page == "leaderboard":
        ui.display_leaderboard_page()
    else:
        ui.display_home_page()


if __name__ == "__main__":
    main()
