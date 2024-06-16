import streamlit as st
from utils.Database_file import Database
from utils.Home_file import Home

st.set_page_config(layout="wide")

def main():
    st.title("Welcome to the Arcade!")
    
    db = Database()
    # db.refresh_images()
    # --> not doing above here as it makes more sense to do it only when a new game is initialized
    home = Home(db)

    home.display_home_page()

if __name__ == "__main__":
    main()
