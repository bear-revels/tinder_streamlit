import streamlit as st
import os

# Initialize session state
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'upload_mode' not in st.session_state:
    st.session_state.upload_mode = None
if 'last_image_number' not in st.session_state:
    st.session_state.last_image_number = 0

def main():
    if not st.session_state.name:
        st.title("Enter your name")
        name = st.text_input("Name")
        if st.button("Submit"):
            if name:
                st.session_state.name = name
                st.experimental_rerun()
            else:
                st.error("Please enter your name.")
    elif not st.session_state.authenticated:
        st.title("Authentication Required")
        password = st.text_input("Enter Password", type="password")
        if st.button("Submit"):
            if password == password:
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Invalid password. Please try again.")
    else:
        if st.session_state.upload_mode is None:
            select_image_type()
        elif st.session_state.show_upload:
            st.title(f"Upload {st.session_state.upload_mode} Images")
            uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            if uploaded_files:
                if st.button("Submit image(s)"):
                    save_uploaded_files(uploaded_files, st.session_state.upload_mode, st.session_state.name)
                    st.success("Thank you! Your image(s) have been uploaded!")
                    st.session_state.show_upload = False  # Hide the parts used before
                    st.session_state.upload_mode = None  # Reset upload mode
                    st.session_state.last_image_number = 0  # Reset last image number
                    st.experimental_rerun()  # Rerun the app to show initial screen
        else:
            st.title("Upload in progress...")

def select_image_type():
    st.session_state.show_upload = True
    st.title("Select Image Type")
    if st.button("genAI"):
        st.session_state.upload_mode = "genAI"
        st.experimental_rerun()
    if st.button("Real"):
        st.session_state.upload_mode = "Real"
        st.experimental_rerun()

def save_uploaded_files(uploaded_files, label, username):
    # Define the directory path based on the label
    dir_path = f"./images/{label.lower()}"
    
    # Ensure the directory exists
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for uploaded_file in uploaded_files:
        st.session_state.last_image_number += 1
        
        # Extract the file name without extension and the extension itself
        file_name_without_ext, file_extension = os.path.splitext(uploaded_file.name)
        file_extension = file_extension.lower()  # Ensure the extension is in lowercase
        
        # Construct the new file name
        new_file_name = f"{label.lower()}_{username}_{file_name_without_ext}{file_extension}"
        file_path = os.path.join(dir_path, new_file_name)
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Saved file: {new_file_name} in {dir_path}")

if __name__ == "__main__":
    main()
