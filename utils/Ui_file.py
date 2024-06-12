import streamlit as st
import random
from pathlib import Path
import os
from PIL import Image
import hmac


class UI:
    def __init__(self, db):
        """Initialize the UI class with a database instance."""
        self.db = db

    def check_password(self):
        """Returns `True` if the user had the correct password."""

        def password_entered():
            """Checks whether a password entered by the user is correct."""
            if hmac.compare_digest(
                st.session_state["password"], st.secrets["password"]
            ):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the password.
            else:
                st.session_state["password_correct"] = False

        # Return True if the password is validated.
        if st.session_state.get("password_correct", False):
            return True

        # Show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        if "password_correct" in st.session_state:
            st.error("😕 Password incorrect")
        return False

    def display_home_page(self):
        """Display the home page with navigation tiles."""
        st.write("Welcome to the Arcade!")
        st.write(
            "🚀 Welcome to the cutting-edge intersection of AI creativity and interactive gaming! Get ready to embark on an electrifying journey through a digital realm where imagination knows no bounds and excitement knows no limits."
        )
        st.write(
            "🎨 Dive into a mesmerizing universe where every pixel pulsates with the brilliance of AI-generated imagery. Immerse yourself in a symphony of colors, shapes, and textures, each crafted by the boundless creativity of artificial intelligence."
        )
        st.write(
            "🌟 But wait, there's more! Prepare to put your discerning eye to the test in our exhilarating game of visual mastery. Your mission? To sift through a stunning array of AI-generated images and select the true masterpieces from the crowd. With each astute choice, you'll earn points, climb the ranks, and solidify your status as a connoisseur of digital art."
        )
        st.write(
            "🏆 And that's not all – once you've conquered the game, take your place among the elite on our prestigious leaderboard. Flaunt your achievements, bask in the glory of victory, and inspire others to follow in your footsteps."
        )
        st.write(
            "🔥 So, what are you waiting for? Step into the future of gaming, where innovation thrives, creativity reigns supreme, and every click brings you closer to greatness. Join us now and unleash your inner visionary on an adventure like no other!"
        )

        # display animation at specific place via COLUMNS
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Play")
            st.page_link("app.py", label="Game", icon="🎮")
        with col2:
            st.write("Contribute")
            st.page_link("./pages/2_⬆️_Contribute.py", label="upload", icon="⬆️")
        with col3:
            st.write("Leaderboard")
            st.page_link("app.py", label="board", icon="🏆")
