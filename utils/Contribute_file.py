import streamlit as st
from pathlib import Path
import os
from PIL import Image
import hmac

class Contribute:
    def __init__(self, db):
        """Initialize the Contribute class with a database instance."""
        self.db = db
        # Initialize session state
        if 'name' not in st.session_state:
            st.session_state.name = ""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'upload_mode' not in st.session_state:
            st.session_state.upload_mode = None
        if 'last_image_number' not in st.session_state:
            st.session_state.last_image_number = 0
        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = []

    def display_contribute_page(self):
        """Display the contribute page where users can upload images."""
        st.write("Contribute your images to the game!")

        if not self.check_password():
            st.stop()

        if not st.session_state.name:
            st.title("Enter your name")
            name = st.text_input("Name")
            if st.button("Submit"):
                if name:
                    st.session_state.name = name
                    st.experimental_rerun()
                else:
                    st.error("Please enter your name.")
        else:
            if st.session_state.upload_mode is None:
                self.select_image_type()
            elif st.session_state.show_upload:
                st.title(f"Upload {st.session_state.upload_mode} Images")
                uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
                if uploaded_files:
                    st.session_state.uploaded_files = uploaded_files
                    for uploaded_file in uploaded_files:
                        st.write(uploaded_file.name)

                    if st.button("Submit image(s)"):
                        for uploaded_file in st.session_state.uploaded_files:
                            self.save_uploaded_file(uploaded_file, st.session_state.name, st.session_state.upload_mode.lower())
                        st.success("Thank you! Your image(s) have been uploaded!")
                        st.session_state.show_upload = False  # Hide the parts used before
                        st.session_state.upload_mode = None  # Reset upload mode
                        st.session_state.last_image_number = 0  # Reset last image number
                        st.experimental_rerun()  # Rerun the app to show initial screen
            else:
                st.title("Upload in progress...")

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

    def select_image_type(self):
        st.session_state.show_upload = True
        st.title("Select Image Type")
        if st.button("GenAI"):
            st.session_state.upload_mode = "GenAI"
            st.experimental_rerun()
        if st.button("Real"):
            st.session_state.upload_mode = "Real"
            st.experimental_rerun()

    def save_uploaded_file(self, uploaded_file, contributor_name, image_type, target_height=800):
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
