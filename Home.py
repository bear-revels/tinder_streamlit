import streamlit as st
from utils.Database_file import Database
from archive.Elo_file import Elo
from utils.Home_file import Home


def main():
    st.title("ARCADE")
    
    db = Database()
    # db.refresh_images()
    # --> not doing above here as it makes more sense to do it only when a new game is initialized
    home = Home(db)

    home.display_home_page()

if __name__ == "__main__":
    main()
