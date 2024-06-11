import streamlit as st
import random
from pathlib import Path
import os
from PIL import Image

class UI:
    def __init__(self, db):
        """Initialize the UI class with a database instance."""
        self.db = db

    def display_home_page(self):
        """Display the home page with navigation tiles."""
        st.write("Welcome to the Arcade!")

    def display_play_page(self):
        """Display the game play page."""
        player_name = st.text_input("Enter your name to start playing:", "")
        if player_name:
            if 'player_id' not in st.session_state:
                st.session_state.player_id = self.db.add_player(player_name)
            self.start_game()

    def start_game(self):
        """Start the game and handle game logic."""
        if 'level' not in st.session_state:
            st.session_state.level = 1
            st.session_state.score = 0
            st.session_state.timer = 30
        
        real_image, genai_image = self.db.get_random_images()
        images = [(real_image, 1), (genai_image, 0)]
        random.shuffle(images)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select Left Image", key="left"):
                self.check_selection(images[0][1] == 1)
            st.image(images[0][0][4], use_column_width=True)
        with col2:
            if st.button("Select Right Image", key="right"):
                self.check_selection(images[1][1] == 1)
            st.image(images[1][0][4], use_column_width=True)

    def check_selection(self, is_real_image):
        """Check the user's selection and update the game state."""
        if is_real_image:
            st.session_state.score += 1
            st.session_state.level += 1
            st.session_state.timer *= 0.9
            st.write(f"Correct! Your current score: {st.session_state.score}")
            self.start_game()
        else:
            st.write("Wrong! Game Over!")
            st.write(f"Your final score: {st.session_state.score}")
            st.session_state.page = 'home'

    def display_contribute_page(self):
        """Display the contribute page where users can upload images."""
        st.write("Contribute your images to the game!")
        
        contributor_name = st.text_input("Please enter your name to add images to the game:")
        image_type = st.selectbox("Select the type of image:", ["Real", "GenAI"])
        uploaded_files = st.file_uploader("Upload images:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        if st.button("Submit"):
            if contributor_name and image_type and uploaded_files:
                for uploaded_file in uploaded_files:
                    self.save_uploaded_file(uploaded_file, contributor_name, image_type.lower())
                st.write("Images uploaded successfully!")
            else:
                st.write("Please provide your name, select image type, and upload images.")

    def save_uploaded_file(self, uploaded_file, contributor_name, image_type):
        """Save the uploaded file to the appropriate directory."""
        # Ensure the directory exists
        save_dir = Path(f'images/{image_type}')
        save_dir.mkdir(parents=True, exist_ok=True)

        # Determine file extension
        file_extension = os.path.splitext(uploaded_file.name)[1]

        # Construct a unique file name
        existing_files = list(save_dir.glob(f'{contributor_name}_*{file_extension}'))
        file_count = len(existing_files) + 1
        save_path = save_dir / f"{contributor_name}_{file_count}{file_extension}"

        # Save the file
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Add to database
        self.db.add_image(contributor_name, 1 if image_type == "real" else 0, str(save_path).replace('\\', '/'))

    def display_leaderboard_page(self):
        """Display the leaderboard page."""
        st.write("Leaderboard")
        leaderboard_data = self.db.get_leaderboard()
        st.write(leaderboard_data)