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

    def display_play_page(self):
        """Display the game play page."""
        player_name = st.text_input("Enter your name to start playing:", "")
        if player_name:
            if "player_id" not in st.session_state:
                st.session_state.player_id = self.db.add_player(player_name)
            self.start_game()

    def start_game(self):
        """Start the game and handle game logic."""
        if "level" not in st.session_state:
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
            st.session_state.page = "home"

    def display_contribute_page(self):
        """Display the contribute page where users can upload images."""
        st.write("Contribute your images to the game!")

        if not self.check_password():
            st.stop()

        contributor_name = st.text_input(
            "Please enter your name to add images to the game:"
        )
        image_type = st.selectbox("Select the type of image:", ["Real", "GenAI"])
        uploaded_files = st.file_uploader(
            "Upload images:", type=["jpg", "jpeg", "png"], accept_multiple_files=True
        )

        if st.button("Submit"):
            if contributor_name and image_type and uploaded_files:
                for uploaded_file in uploaded_files:
                    self.save_uploaded_file(
                        uploaded_file, contributor_name, image_type.lower()
                    )
                st.write("Images uploaded successfully!")
            else:
                st.write(
                    "Please provide your name, select image type, and upload images."
                )

    def save_uploaded_file(self, uploaded_file, contributor_name, image_type, target_height=(800)):
        """Save the uploaded file to the appropriate directory and resize it."""
        # Ensure the directory exists
        save_dir = Path(f"images/{image_type}")
        save_dir.mkdir(parents=True, exist_ok=True)

        # Determine file extension
        file_extension = os.path.splitext(uploaded_file.name)[1]

        # Construct a unique file name
        existing_files = list(save_dir.glob(f"{contributor_name}_*{file_extension}"))
        file_count = len(existing_files) + 1
        save_path = save_dir / f"{contributor_name}_{file_count}{file_extension}"

        # Save the file temporarily
        temp_path = save_dir / f"temp_{contributor_name}_{file_count}{file_extension}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Open the saved image and resize it to the target height while maintaining aspect ratio
        with Image.open(temp_path) as img:
        # Calculate the new width based on the target height and original aspect ratio
            aspect_ratio = img.width / img.height
            new_width = int(target_height * aspect_ratio)
            img = img.resize((new_width, target_height), Image.LANCZOS)
            img.save(save_path)

        # Remove the temporary file
        os.remove(temp_path)

        # Add to database
        self.db.add_image(
            contributor_name,
            1 if image_type == "real" else 0,
            str(save_path).replace("\\", "/"),
        )

    def display_leaderboard_page(self):
        """Display the leaderboard page."""
        st.write("Leaderboard")
        leaderboard_data = self.db.get_leaderboard()
        st.write(leaderboard_data)
